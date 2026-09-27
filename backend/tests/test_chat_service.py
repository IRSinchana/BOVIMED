"""Basic chat service tests (no external LLM calls)."""

from app.services.ai_chat_service import get_ai_config_status
from app.services.chat_service import ChatService, _detect_topic


def test_detect_topic_mastitis():
    assert _detect_topic("What are signs of mastitis?") == "signs"


def test_detect_topic_antibiotic():
    assert _detect_topic("Can I give amoxicillin?") == "antibiotic"


def test_local_reply_has_safety_notice():
    svc = ChatService()
    out = svc.reply("How can I prevent mastitis?", language="en")
    assert out["safety_notice"] is True
    assert "veterinarian" in out["answer"].lower()
    assert out["mode"] in ("local", "unconfigured", "external", "error", "fallback")


def test_ai_config_status_defaults():
    status = get_ai_config_status()
    assert hasattr(status, "enabled")
    assert hasattr(status, "configured")
