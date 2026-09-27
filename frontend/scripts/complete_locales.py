# -*- coding: utf-8 -*-
"""Fill incomplete locale JSON files from complete reference locales."""
import json
from copy import deepcopy
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"

# Reference complete locale per language (same script family / mutual intelligibility).
REFERENCE = {
    "as": "bn",   # Assamese ← Bengali (very close)
    "or": "bn",   # Odia ← Bengali base + existing Odia overrides kept
    "mni": "bn",  # Manipuri (Bengali script)
    "pa": "hi",   # Punjabi ← Hindi base + existing Gurmukhi overrides kept
    "ne": "hi",   # Nepali ← Hindi (Devanagari)
    "kok": "hi",  # Konkani
    "sa": "hi",   # Sanskrit
    "brx": "hi",  # Bodo (Devanagari)
    "doi": "hi",  # Dogri
    "mai": "hi",  # Maithili
    "ur": "hi",   # Urdu ← Hindi base + existing Urdu overrides kept
    "sd": "ur",   # Sindhi ← Urdu (Arabic script)
    "ks": "ur",   # Kashmiri ← Urdu (Arabic script)
    "sat": "bn",  # Santhali ← Bengali script base
}

# Urdu translations for keys still in English after merge (from hi reference).
UR_VET = {
    "searchByLocation": "مقام سے تلاش کریں",
    "placeholderState": "ریاست درج کریں",
    "placeholderDistrict": "ضلع درج کریں",
    "placeholderCity": "شہر درج کریں",
    "placeholderPincode": "پن کوڈ درج کریں",
    "locating": "آپ کا مقام حاصل کیا جا رہا ہے…",
    "locationDetected": "مقام مل گیا",
    "locationReady": "مقام مل گیا — قریبی ویٹرنری ڈاکٹر تلاش کیے جا رہے ہیں…",
    "notVerified": "اس تلاش کے لیے ویٹرنری دستیابی فی الحال تصدیق شدہ نہیں ہے۔",
    "noVerified": "اس تلاش کے لیے کوئی تصدیق شدہ ویٹرنری رابطے دستیاب نہیں ہیں۔",
    "noVerifiedAtLocation": "آپ کا مقام کامیابی سے مل گیا، لیکن اس مقام کے لیے کوئی تصدیق شدہ ویٹرنری رابطے دستیاب نہیں ہیں۔",
    "openMaps": "Google Maps کھولیں",
    "foundVerified": "تصدیق شدہ ویٹرنری رابطے ملے",
    "geoUnavailable": "اس ڈیوائس پر مقام دستیاب نہیں ہے۔",
    "geoTimeout": "مقام حاصل کرنے کا وقت ختم ہو گیا۔ دوبارہ کوشش کریں یا پتہ درج کریں۔",
}

UR_AUTH = {
    "loginTitle": "خوش آمدید",
    "loginSubtitle": "اپنے مویشیوں کی دیکھ بھال کے لیے BOVIMED میں سائن ان کریں۔",
    "registerTitle": "کسان اکاؤنٹ بنائیں",
    "registerSubtitle": "AI معاون ڈیری صحت اسکریننگ کے لیے BOVIMED میں شامل ہوں۔",
    "identifier": "موبائل نمبر یا ای میل",
    "password": "پاس ورڈ",
    "confirmPassword": "پاس ورڈ کی تصدیق کریں",
    "showPassword": "دکھائیں",
    "hidePassword": "چھپائیں",
    "rememberMe": "مجھے یاد رکھیں",
    "login": "لاگ ان",
    "register": "اکاؤنٹ بنائیں",
    "forgot": "پاس ورڈ بھول گئے؟",
    "forgotHint": "رسائی بحال کرنے کے لیے سپورٹ سے رابطہ کریں۔",
    "noAccount": "BOVIMED میں نئے ہیں؟",
    "hasAccount": "پہلے سے اکاؤنٹ ہے؟",
    "createAccount": "اکاؤنٹ بنائیں",
    "fullName": "کسان کا نام",
    "mobile": "موبائل نمبر",
    "email": "ای میل (اختیاری)",
    "farmName": "فارم کا نام",
    "state": "ریاست",
    "district": "ضلع",
    "loggingIn": "سائن ان ہو رہا ہے…",
    "registering": "اکاؤنٹ بن رہا ہے…",
}

UR_ANALYZE = {
    "title": "گائے کی صحت کا معائنہ",
    "subtitle": "AI اسکین کے لیے گائے یا تھن کی تصویر اپ لوڈ کریں۔",
    "cowId": "گائے ID (اختیاری)",
    "analyzeBtn": "AI اسکین شروع کریں",
    "analyzing": "AI اسکین چل رہا ہے…",
    "noImage": "براہ کرم پہلے گائے/تھن کی تصویر منتخب کریں۔",
    "drop": "گائے/تھن کی تصویر یہاں گھسیٹیں اور چھوڑیں",
    "clickBrowse": "یا براؤز کرنے کے لیے کلک کریں",
    "browse": "تصویر منتخب کریں",
    "remove": "ہٹائیں",
    "stepScan": "AI اسکین",
}

UR_CAMERA = {
    "title": "کیمرہ اسکین",
    "subtitle": "ایک تصویر لیں اور AI اسکین کے لیے بھیجیں۔",
    "open": "کیمرہ کھولیں",
    "capture": "تصویر لیں",
    "close": "بند کریں",
    "retake": "دوبارہ لیں",
    "analyze": "تصویر کا معائنہ کریں",
    "permission": "کیمرہ کی اجازت درکار ہے۔",
    "useUpload": "اپ لوڈ استعمال کریں",
}

UR_RESULT = {
    "title": "AI صحت کا جائزہ",
    "screening": "AI معاون اسکریننگ کا نتیجہ",
    "prediction": "نتیجہ",
    "confidence": "AI اعتماد",
    "risk": "خطرے کی سطح",
    "primary": "اہم نتیجہ",
    "noPrimary": "اس تصویر کے لیے کوئی واضح صحت کا نتیجہ نہیں۔",
    "detections": "AI اسکین نتائج",
    "noDetections": "کوئی چیز نہیں ملی۔",
    "recommendations": "آپ کیا کر سکتے ہیں",
    "careGuidance": "AI معاون نگہداشت کی رہنمائی",
    "newUpload": "نیا اپ لوڈ",
    "newCamera": "نیا کیمرہ اسکین",
    "original": "آپ کی تصویر",
    "annotated": "AI اسکین تصویر",
    "askBovimed": "اس نتیجے کے بارے میں BOVIMED سے پوچھیں",
}

UR_COWS = {
    "title": "آپ کی گائیں",
    "empty": "ابھی کوئی گائے نہیں۔ شامل کرنے کے لیے AI اسکین چلائیں۔",
    "breed": "نسل",
    "status": "حالت",
    "analyze": "معائنہ کریں",
    "ask": "اس گائے کے بارے میں BOVIMED سے پوچھیں",
}

UR_HISTORY = {"title": "صحت کی تاریخ"}
UR_SETTINGS_EXTRA = {
    "language": "زبان",
    "languageSubtitle": "اپنی پسندیدہ زبان منتخب کریں۔",
    "profile": "کسان پروفائل",
    "name": "نام",
    "mobile": "موبائل",
    "farmName": "فارم کا نام",
    "state": "ریاست",
    "district": "ضلع",
    "preferredLanguage": "پسندیدہ زبان",
    "save": "پروفائل محفوظ کریں",
    "saving": "محفوظ ہو رہا ہے…",
    "saved": "پروفائل محفوظ ہو گئی۔",
    "api": "API کنکشن",
    "aboutBody": "BOVIMED ڈیری کسانوں کو تھن کی صحت کی AI معاون ابتدائی اسکریننگ میں مدد کرتا ہے۔ ہمیشہ ویٹرنری ڈاکٹر سے تصدیق کریں۔",
    "title": "ترتیبات",
}

UR_COMMON = {
    "loading": "لوڈ ہو رہا ہے…",
    "error": "کچھ غلط ہو گیا",
    "backendDown": "BOVIMED سرور تک نہیں پہنچ سکے۔ کیا بیک اینڈ چل رہا ہے؟",
    "save": "محفوظ کریں",
    "cancel": "منسوخ کریں",
    "retry": "دوبارہ کوشش کریں",
    "close": "بند کریں",
    "confirm": "تصدیق کریں",
    "success": "کامیاب",
}

UR_DASHBOARD_EXTRA = {
    "analysesMonth": "اس مہینے کے اسکین",
    "recent": "حالیہ AI اسکین",
    "cowId": "گائے ID",
    "date": "تاریخ",
    "result": "نتیجہ",
    "confidence": "AI اعتماد",
    "risk": "خطرہ",
    "empty": "ابھی کوئی اسکین نہیں۔ تصویر اپ لوڈ یا کیپچر کریں۔",
}

UR_NAV_EXTRA = {"reports": "رپورٹس", "home": "ہوم"}

PA_VET = {
    "searchByLocation": "ਸਥਾਨ ਨਾਲ ਖੋਜੋ",
    "placeholderState": "ਰਾਜ ਦਰਜ ਕਰੋ",
    "placeholderDistrict": "ਜ਼ਿਲ੍ਹਾ ਦਰਜ ਕਰੋ",
    "placeholderCity": "ਸ਼ਹਿਰ ਦਰਜ ਕਰੋ",
    "placeholderPincode": "ਪਿਨ ਕੋਡ ਦਰਜ ਕਰੋ",
    "locating": "ਤੁਹਾਡਾ ਸਥਾਨ ਪ੍ਰਾਪਤ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ…",
    "locationDetected": "ਸਥਾਨ ਮਿਲ ਗਿਆ",
    "locationReady": "ਸਥਾਨ ਮਿਲ ਗਿਆ — ਨੇੜਲੇ ਪਸ਼ੂ ਡਾਕਟਰ ਖੋਜੇ ਜਾ ਰਹੇ ਹਨ…",
    "notVerified": "ਇਸ ਖੋਜ ਲਈ ਪਸ਼ੂ ਡਾਕਟਰ ਦੀ ਉਪਲਬਧਤਾ ਇਸ ਸਮੇਂ ਪ੍ਰਮਾਣਿਤ ਨਹੀਂ ਹੈ।",
    "noVerified": "ਇਸ ਖੋਜ ਲਈ ਕੋਈ ਪ੍ਰਮਾਣਿਤ ਪਸ਼ੂ ਡਾਕਟਰ ਸੰਪਰਕ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
    "noVerifiedAtLocation": "ਤੁਹਾਡਾ ਸਥਾਨ ਸਫਲਤਾਪੂਰਵਕ ਮਿਲ ਗਿਆ, ਪਰ ਇਸ ਸਥਾਨ ਲਈ ਕੋਈ ਪ੍ਰਮਾਣਿਤ ਪਸ਼ੂ ਡਾਕਟਰ ਸੰਪਰਕ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
    "openMaps": "Google Maps ਖੋਲ੍ਹੋ",
    "foundVerified": "ਪ੍ਰਮਾਣਿਤ ਪਸ਼ੂ ਡਾਕਟਰ ਸੰਪਰਕ ਮਿਲੇ",
    "geoUnavailable": "ਇਸ ਡਿਵਾਈਸ ਤੇ ਸਥਾਨ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
    "geoTimeout": "ਸਥਾਨ ਪ੍ਰਾਪਤ ਕਰਨ ਦਾ ਸਮਾਂ ਸਮਾਪਤ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ ਜਾਂ ਪਤਾ ਦਰਜ ਕਰੋ।",
}


def load(code: str) -> dict:
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code: str, data: dict) -> None:
    (DIR / f"{code}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def flatten(obj: dict, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in obj.items():
        nk = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, nk))
        else:
            out[nk] = v
    return out


def unflatten(flat: dict[str, str]) -> dict:
    root: dict = {}
    for k, v in flat.items():
        parts = k.split(".")
        cur = root
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


def deep_merge_dict(base: dict, overlay: dict) -> dict:
    out = deepcopy(base)
    for k, v in overlay.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge_dict(out[k], v)
        else:
            out[k] = v
    return out


def fill_from_reference(code: str, ref_code: str) -> dict:
    en = load("en")
    ref = load(ref_code)
    existing = load(code)
    en_flat = flatten(en)
    ref_flat = flatten(ref)
    exist_flat = flatten(existing)

    out_flat = flatten(deepcopy(en))
    for key, en_val in en_flat.items():
        if key in exist_flat and exist_flat[key] != en_val:
            out_flat[key] = exist_flat[key]
        elif key in ref_flat and ref_flat[key] != en_val:
            out_flat[key] = ref_flat[key]
        else:
            out_flat[key] = en_val

    return unflatten(out_flat)


def apply_urdu_patches(data: dict) -> dict:
    for k, v in UR_VET.items():
        data.setdefault("vets", {})[k] = v
    data["auth"] = {**data.get("auth", {}), **UR_AUTH}
    data["analyze"] = {**data.get("analyze", {}), **UR_ANALYZE}
    data["camera"] = {**data.get("camera", {}), **UR_CAMERA}
    data["result"] = {**data.get("result", {}), **UR_RESULT}
    data["cows"] = {**data.get("cows", {}), **UR_COWS}
    data["history"] = {**data.get("history", {}), **UR_HISTORY}
    data["settings"] = {**data.get("settings", {}), **UR_SETTINGS_EXTRA}
    data["common"] = {**data.get("common", {}), **UR_COMMON}
    data["dashboard"] = {**data.get("dashboard", {}), **UR_DASHBOARD_EXTRA}
    data["nav"] = {**data.get("nav", {}), **UR_NAV_EXTRA}
    data["demoMode"] = "ڈیمو موڈ"
    data["langIndicator"] = "زبان"
    return data


def apply_punjabi_vet(data: dict) -> dict:
    data.setdefault("vets", {}).update(PA_VET)
    data["nav"]["reports"] = "ਰਿਪੋਰਟਾਂ"
    data["nav"]["home"] = "ਘਰ"
    return data


def validate_all() -> None:
    en_flat = flatten(load("en"))
    errors = []
    for code in sorted(REFERENCE.keys()) + ["en", "hi", "kn", "te", "ta", "ml", "mr", "bn", "gu"]:
        if code == "en":
            continue
        flat = flatten(load(code))
        missing = [k for k in en_flat if k not in flat]
        if missing:
            errors.append(f"{code}: missing {len(missing)} keys")
    if errors:
        raise SystemExit("\n".join(errors))
    print("All locales have complete key sets.")


def main() -> None:
    # Pass 1: fill from references
    for code, ref in REFERENCE.items():
        if ref == "ur" and code in ("sd", "ks"):
            continue  # pass 2
        data = fill_from_reference(code, ref)
        if code == "ur":
            data = apply_urdu_patches(data)
        if code == "pa":
            data = apply_punjabi_vet(data)
        save(code, data)
        print(f"completed {code}.json from {ref}")

    # Pass 2: sd, ks from completed ur
    for code in ("sd", "ks"):
        data = fill_from_reference(code, "ur")
        if code == "sd":
            data["langIndicator"] = "زبان"
        if code == "ks":
            data["langIndicator"] = "زَبان"
        save(code, data)
        print(f"completed {code}.json from ur")

    validate_all()


if __name__ == "__main__":
    main()
