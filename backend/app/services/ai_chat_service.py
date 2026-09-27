"""Provider abstraction for BOVIMED LLM-powered chat (Gemini / OpenAI)."""

from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

MEDICAL_SYSTEM_PROMPT = """You are BOVIMED AI Assistant — a dairy cattle health screening guide for Indian farmers.

CRITICAL SAFETY RULES (never break these):
1. NEVER provide a definitive veterinary diagnosis.
2. NEVER prescribe medicines, antibiotics, injections, or specific dosages.
3. If asked about medication or antibiotics, explain that only a qualified veterinarian can decide treatment.
4. NEVER invent veterinarian names, phone numbers, clinics, or addresses.
5. For severe or emergency symptoms, urge prompt veterinary care.
6. Answer in the user's requested language. If you cannot answer reliably in that language, say so clearly in that language.
7. Keep answers practical, empathetic, and farmer-friendly (2–6 short paragraphs max).
8. BOVIMED provides AI-assisted screening only — not a substitute for a veterinarian."""


@dataclass
class AIChatResult:
    text: str
    provider: str
    model: str


@dataclass
class AIConfigStatus:
    enabled: bool
    configured: bool
    provider: str | None
    message: str


def get_ai_config_status() -> AIConfigStatus:
    enabled = os.getenv("BOVIMED_LLM_ENABLED", "false").lower() in ("true", "1", "yes")
    provider = _resolve_provider()
    configured = bool(provider and _api_key_for_provider(provider))
    if not enabled:
        return AIConfigStatus(
            enabled=False,
            configured=configured,
            provider=provider,
            message="LLM disabled. Set BOVIMED_LLM_ENABLED=true to enable live AI.",
        )
    if not configured:
        return AIConfigStatus(
            enabled=True,
            configured=False,
            provider=provider,
            message=(
                "AI assistant is not configured. Set GEMINI_API_KEY or OPENAI_API_KEY "
                "in backend .env (never in the frontend)."
            ),
        )
    return AIConfigStatus(
        enabled=True,
        configured=True,
        provider=provider,
        message=f"AI assistant ready ({provider}).",
    )


def _resolve_provider() -> str | None:
    explicit = (os.getenv("BOVIMED_LLM_PROVIDER") or "").strip().lower()
    if explicit in ("gemini", "openai"):
        return explicit
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("BOVIMED_LLM_API_KEY"):
        return "gemini"
    return None


def _api_key_for_provider(provider: str) -> str | None:
    if provider == "gemini":
        return os.getenv("GEMINI_API_KEY") or os.getenv("BOVIMED_LLM_API_KEY")
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY") or os.getenv("BOVIMED_LLM_API_KEY")
    return None


def generate_ai_reply(
    *,
    message: str,
    language: str,
    cow_id: str | None = None,
    context: dict | None = None,
    history: list[dict[str, str]] | None = None,
) -> AIChatResult | None:
    """Call configured LLM provider. Returns None if not configured or on failure."""
    status = get_ai_config_status()
    if not status.enabled or not status.configured or not status.provider:
        return None

    provider = status.provider
    api_key = _api_key_for_provider(provider)
    if not api_key:
        return None

    lang = (language or "en").split("-")[0].lower()
    ctx = context or {}
    user_block = _build_user_prompt(message, lang=lang, cow_id=cow_id, context=ctx, history=history)

    try:
        if provider == "gemini":
            return _call_gemini(api_key, user_block, lang=lang)
        if provider == "openai":
            return _call_openai(api_key, user_block, lang=lang, history=history)
    except Exception as exc:
        logger.warning("LLM provider %s failed: %s", provider, exc)
        return None
    return None


def _build_user_prompt(
    message: str,
    *,
    lang: str,
    cow_id: str | None,
    context: dict,
    history: list[dict[str, str]] | None,
) -> str:
    parts = [MEDICAL_SYSTEM_PROMPT, f"\nRespond in language code: {lang}\n"]
    if cow_id or context:
        parts.append(f"Cow context JSON: {json.dumps({'cow_id': cow_id, **context}, ensure_ascii=False)}")
    if history:
        recent = history[-6:]
        parts.append("Recent conversation:")
        for turn in recent:
            role = turn.get("role", "user")
            text = turn.get("content") or turn.get("message") or ""
            parts.append(f"{role}: {text}")
    parts.append(f"Farmer question: {message}")
    return "\n".join(parts)


def _call_gemini(api_key: str, prompt: str, *, lang: str) -> AIChatResult:
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model)}:generateContent?key={urllib.parse.quote(api_key)}"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.35, "maxOutputTokens": 900},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = (parts[0].get("text") if parts else "") or ""
    if not text.strip():
        raise RuntimeError("Gemini returned empty text")
    return AIChatResult(text=text.strip(), provider="gemini", model=model)


def _call_openai(api_key: str, prompt: str, *, lang: str, history: list[dict[str, str]] | None) -> AIChatResult:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    messages: list[dict[str, str]] = [{"role": "system", "content": MEDICAL_SYSTEM_PROMPT}]
    if history:
        for turn in history[-8:]:
            role = turn.get("role", "user")
            if role not in ("user", "assistant"):
                role = "user"
            content = turn.get("content") or turn.get("message") or ""
            if content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.35,
        "max_tokens": 900,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("OpenAI returned no choices")
    text = choices[0].get("message", {}).get("content", "")
    if not text.strip():
        raise RuntimeError("OpenAI returned empty text")
    return AIChatResult(text=text.strip(), provider="openai", model=model)
