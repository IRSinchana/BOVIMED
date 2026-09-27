# -*- coding: utf-8 -*-
"""Fix mixed-language nav and remaining English vet strings."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"


def load(code):
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code, data):
    (DIR / f"{code}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


hi = load("hi")
ur = load("ur")
mr = load("mr")

# Devanagari family: use Hindi nav (clear farmer UI) with language-specific dashboard label
NEPALI_NAV = {
    **hi["nav"],
    "dashboard": "ड्यासबोर्ड",
    "settings": "सेटिङहरू",
}
for code, nav, indicator in [
    ("ne", NEPALI_NAV, "नेपाली"),
    ("kok", {**hi["nav"], "dashboard": "डॅशबोर्ड"}, "कोंकणी"),
    ("sa", {**hi["nav"], "dashboard": "फलकम्"}, "संस्कृतम्"),
    ("brx", {**hi["nav"], "dashboard": "डैशबोर्ड"}, "बड़ो"),
    ("doi", {**hi["nav"], "dashboard": "डैशबोर्ड"}, "डोगरी"),
    ("mai", {**hi["nav"], "dashboard": "डैशबोर्ड"}, "मैथिली"),
]:
    d = load(code)
    d["nav"] = nav
    d["langIndicator"] = indicator
    save(code, d)
    print(f"fixed nav: {code}")

# Arabic-script: full Urdu nav
for code in ("ks", "sd"):
    d = load(code)
    d["nav"] = ur["nav"]
    if code == "ks":
        d["langIndicator"] = "کٲشُر"
    save(code, d)
    print(f"fixed nav: {code}")

# Punjabi: restore Gurmukhi nav + complete vets from hi with Gurmukhi vet keys
pa = load("pa")
pa["nav"] = {
    "dashboard": "ਡੈਸ਼ਬੋਰਡ",
    "analyze": "ਗਾਂ ਦੀ ਜਾਂਚ",
    "camera": "ਕੈਮਰਾ ਸਕੈਨ",
    "cows": "ਗਾਵਾਂ",
    "history": "ਸਿਹਤ ਰਿਕਾਰਡ",
    "alerts": "ਚੇਤਾਵਨੀਆਂ",
    "chat": "BOVIMED ਨੂੰ ਪੁੱਛੋ",
    "vets": "ਪਸ਼ੂ ਹਸਪਤਾਲ",
    "settings": "ਸੈਟਿੰਗਾਂ",
    "logout": "ਲਾਗ ਆਉਟ",
    "reports": "ਰਿਪੋਰਟਾਂ",
    "home": "ਘਰ",
}
pa["vets"] = {**hi["vets"], **pa["vets"]}
pa["vets"]["useLocation"] = "ਮੇਰਾ ਸਥਾਨ ਵਰਤੋ"
pa["vets"]["empty"] = hi["vets"]["empty"]
pa["vets"]["verify"] = hi["vets"]["verify"]
pa["tagline"] = "ਸਿਹਤਮੰਦ ਪਸ਼ੂਆਂ ਲਈ ਸਮਾਰਟ ਦ੍ਰਿਸ਼ਟੀ"
pa["shortDesc"] = "ਡੇਅਰੀ ਸਿਹਤ ਲਈ AI-ਅਧਾਰਿਤ ਮਸਟਾਇਟਿਸ ਸਕ੍ਰੀਨਿੰਗ।"
pa["disclaimer"] = (
    "BOVIMED ਸਿਰਫ਼ AI-ਸਹਾਇਤਾ ਪ੍ਰਾਪਤ ਸਕ੍ਰੀਨਿੰਗ ਮਾਰਗਦਰਸ਼ਨ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ। "
    "ਇਹ ਡਾਕਟਰੀ ਜਾਂਚ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ।"
)
pa["demoMode"] = "ਡੈਮੋ ਮੋਡ"
pa["langIndicator"] = "ਭਾਸ਼ਾ"
save("pa", pa)
print("fixed pa")

mr["demoMode"] = "डेमो मोड"
save("mr", mr)
print("fixed mr")
