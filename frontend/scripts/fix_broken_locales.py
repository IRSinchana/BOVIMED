# -*- coding: utf-8 -*-
"""
Fix the three broken locale bundles identified in BOVIMED:
- mni (Manipuri): mixed Sanskrit/Hindi/Bengali nav — rebuild from Bengali (Bengali script UI)
- pa (Punjabi): Gurmukhi nav but Hindi auth/dashboard — complete Gurmukhi sections
- kok (Konkani): Hindi copy — rebuild from Marathi (closest living reference)
Also add sat (Santhali) from Bengali base with Santhali lang indicator.
"""
import json
from copy import deepcopy
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"


def load(code: str) -> dict:
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code: str, data: dict) -> None:
    (DIR / f"{code}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def clone_from(ref_code: str, target_code: str, *, lang_indicator: str, overrides: dict | None = None) -> None:
    data = deepcopy(load(ref_code))
    data["langIndicator"] = lang_indicator
    if overrides:
        for section, values in overrides.items():
            data.setdefault(section, {}).update(values)
    save(target_code, data)
    print(f"fixed {target_code} from {ref_code}")


PA_AUTH = {
    "loginTitle": "ਜੀ ਆਇਆਂ ਨੂੰ",
    "loginSubtitle": "ਆਪਣੇ ਪਸ਼ੂਆਂ ਦੀ ਦੇਖਭਾਲ ਲਈ BOVIMED ਵਿੱਚ ਸਾਈਨ ਇਨ ਕਰੋ।",
    "registerTitle": "ਕਿਸਾਨ ਖਾਤਾ ਬਣਾਓ",
    "registerSubtitle": "AI-ਸਹਾਇਤਾ ਡੇਅਰੀ ਸਿਹਤ ਸਕ੍ਰੀਨਿੰਗ ਲਈ BOVIMED ਨਾਲ ਜੁੜੋ।",
    "identifier": "ਮੋਬਾਈਲ ਨੰਬਰ ਜਾਂ ਈਮੇਲ",
    "password": "ਪਾਸਵਰਡ",
    "confirmPassword": "ਪਾਸਵਰਡ ਦੀ ਪੁਸ਼ਟੀ",
    "showPassword": "ਦਿਖਾਓ",
    "hidePassword": "ਛੁਪਾਓ",
    "rememberMe": "ਮੈਨੂੰ ਯਾਦ ਰੱਖੋ",
    "login": "ਲਾਗ ਇਨ",
    "register": "ਖਾਤਾ ਬਣਾਓ",
    "forgot": "ਪਾਸਵਰਡ ਭੁੱਲ ਗਏ?",
    "forgotHint": "ਪਹੁੰਚ ਬਹਾਲ ਕਰਨ ਲਈ ਸਹਾਇਤਾ ਨਾਲ ਸੰਪਰਕ ਕਰੋ।",
    "noAccount": "BOVIMED ਵਿੱਚ ਨਵੇਂ ਹੋ?",
    "hasAccount": "ਪਹਿਲਾਂ ਤੋਂ ਖਾਤਾ ਹੈ?",
    "createAccount": "ਖਾਤਾ ਬਣਾਓ",
    "fullName": "ਕਿਸਾਨ ਦਾ ਨਾਮ",
    "mobile": "ਮੋਬਾਈਲ ਨੰਬਰ",
    "email": "ਈਮੇਲ (ਵਿਕਲਪਿਕ)",
    "farmName": "ਖੇਤ ਦਾ ਨਾਮ",
    "state": "ਰਾਜ",
    "district": "ਜ਼ਿਲ੍ਹਾ",
    "loggingIn": "ਸਾਈਨ ਇਨ ਹੋ ਰਿਹਾ ਹੈ…",
    "registering": "ਖਾਤਾ ਬਣ ਰਿਹਾ ਹੈ…",
}

PA_DASHBOARD = {
    "welcome": "BOVIMED ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ",
    "subtitle": "ਸਮਾਰਟ ਡੇਅਰੀ ਸਿਹਤ ਸਕ੍ਰੀਨਿੰਗ ਲਈ AI-ਸਹਾਇਤਾ।",
    "analyzeCta": "ਗਾਂ ਦੀ ਜਾਂਚ ਕਰੋ",
    "cameraCta": "ਕੈਮਰੇ ਨਾਲ ਸਕੈਨ ਕਰੋ",
    "askCta": "BOVIMED ਨੂੰ ਪੁੱਛੋ",
    "vetCta": "ਪਸ਼ੂ ਡਾਕਟਰੀ ਸੇਵਾ",
    "totalCows": "ਕੁੱਲ ਗਾਵਾਂ",
    "healthy": "ਸਿਹਤਮੰਦ",
    "atRisk": "ਧਿਆਨ ਚਾਹੀਦਾ",
    "analysesMonth": "ਇਸ ਮਹੀਨੇ ਦੇ ਸਕੈਨ",
    "recent": "ਹਾਲੀਆ AI ਸਕੈਨ",
    "recentAlerts": "ਹਾਲੀਆ ਚੇਤਾਵਨੀਆਂ",
    "cowId": "ਗਾਂ ID",
    "date": "ਤਾਰੀਖ",
    "result": "ਨਤੀਜਾ",
    "confidence": "AI ਭਰੋਸਾ",
    "risk": "ਜੋਖਮ",
    "empty": "ਅਜੇ ਕੋਈ ਸਕੈਨ ਨਹੀਂ। ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ।",
    "viewAlert": "ਚੇਤਾਵਨੀ ਦੇਖੋ",
    "findVet": "ਪਸ਼ੂ ਡਾਕਟਰ ਲੱਭੋ",
}


def main() -> None:
    clone_from("bn", "mni", lang_indicator="মৈতৈলোন্")

    pa = load("pa")
    pa["auth"] = {**pa.get("auth", {}), **PA_AUTH}
    pa["dashboard"] = {**pa.get("dashboard", {}), **PA_DASHBOARD}
    pa["langIndicator"] = "ਪੰਜਾਬੀ"
    save("pa", pa)
    print("fixed pa Gurmukhi auth/dashboard")

    kok = deepcopy(load("mr"))
    kok["langIndicator"] = "कोंकणी"
    kok["nav"]["chat"] = "BOVIMED कडेन विचारात"
    save("kok", kok)
    print("fixed kok from mr")

    if not (DIR / "sat.json").exists():
        sat = deepcopy(load("bn"))
        sat["langIndicator"] = "ᱥᱟᱱᱛᱟᱲᱤ"
        sat["nav"]["chat"] = "BOVIMED ᱠᱩᱛᱷᱟᱹ ᱢᱮ"
        save("sat", sat)
        print("created sat.json")


if __name__ == "__main__":
    main()
