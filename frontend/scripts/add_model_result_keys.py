# -*- coding: utf-8 -*-
"""Propagate new result/model transparency keys to all locale files."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"
REF = {
    "as": "bn", "or": "bn", "mni": "bn", "sat": "bn",
    "ne": "hi", "kok": "mr", "sa": "hi", "brx": "hi", "doi": "hi", "mai": "hi",
    "sd": "ur", "ks": "ur", "gu": "mr", "te": "kn", "ta": "kn", "ml": "kn", "pa": "hi",
}
PATCHES = {
    "hi": {
        "modelSection": "AI मॉडल",
        "modelSubtitle": "कस्टम प्रशिक्षित मॉडल",
        "modelLoaded": "कस्टम वेट लोड हुए",
        "modelNotLoaded": "कस्टम वेट लोड नहीं हुए",
        "detectionLabel": "पहचान",
        "detectionConfidence": "पहचान विश्वास",
        "validationPerformance": "सत्यापन डेटासेट प्रदर्शन",
        "modelPerformance": "मॉडल प्रदर्शन",
        "precision": "शुद्धता",
        "recall": "रिकॉल",
        "screeningDisclaimer": "AI-सहायक स्क्रीनिंग। सत्यापन मेट्रिक्स सत्यापन डेटासेट पर मॉडल प्रदर्शन बताते हैं और पशु चिकित्सक निदान नहीं हैं।",
        "confidence": "पहचान विश्वास",
    },
    "bn": {
        "modelSection": "AI মডেল",
        "modelSubtitle": "কাস্টম প্রশিক্ষিত মডেল",
        "modelLoaded": "কাস্টম ওজন লোড হয়েছে",
        "modelNotLoaded": "কাস্টম ওজন লোড হয়নি",
        "detectionLabel": "সনাক্তকরণ",
        "detectionConfidence": "সনাক্তকরণ আত্মবিশ্বাস",
        "validationPerformance": "যাচাইকরণ ডেটাসেট পারফরম্যান্স",
        "modelPerformance": "মডেল পারফরম্যান্স",
        "precision": "নির্ভুলতা",
        "recall": "রিকল",
        "screeningDisclaimer": "AI-সহায়ক স্ক্রিনিং। যাচাইকরণ মেট্রিক্স যাচাইকরণ ডেটাসেটে মডেল পারফরম্যান্স বর্ণনা করে এবং পশুচিকিৎসক নির্ণয় নয়।",
        "confidence": "সনাক্তকরণ আত্মবিশ্বাস",
    },
    "ur": {
        "modelSection": "AI ماڈل",
        "modelSubtitle": "کسٹم تربیت یافتہ ماڈل",
        "modelLoaded": "کسٹم ویٹ لوڈ ہو گئے",
        "modelNotLoaded": "کسٹم ویٹ لوڈ نہیں ہوئے",
        "detectionLabel": "شناخت",
        "detectionConfidence": "شناخت کا اعتماد",
        "validationPerformance": "تصدیقی ڈیٹاسیٹ کارکردگی",
        "modelPerformance": "ماڈل کارکردگی",
        "precision": "درستگی",
        "recall": "ریکال",
        "screeningDisclaimer": "AI معاون اسکریننگ۔ تصدیقی میٹرکس تصدیقی ڈیٹاسیٹ پر ماڈل کارکردگی بیان کرتے ہیں اور ویٹرنری تشخیص نہیں ہیں۔",
        "confidence": "شناخت کا اعتماد",
    },
    "mr": {
        "modelSection": "AI मॉडेल",
        "modelSubtitle": "सानुकूल प्रशिक्षित मॉडेल",
        "modelLoaded": "सानुकूल वजन लोड झाले",
        "modelNotLoaded": "सानुकूल वजन लोड झाले नाही",
        "detectionLabel": "ओळख",
        "detectionConfidence": "ओळख विश्वास",
        "validationPerformance": "प्रमाणीकरण डेटासेट कामगिरी",
        "modelPerformance": "मॉडेल कामगिरी",
        "precision": "अचूकता",
        "recall": "रिकॉल",
        "screeningDisclaimer": "AI-सहाय्यित स्क्रीनिंग. प्रमाणीकरण मेट्रिक्स प्रमाणीकरण डेटासेटवरील मॉडेल कामगिरी दर्शवतात आणि पशुवैद्यकीय निदान नाहीत.",
        "confidence": "ओळख विश्वास",
    },
}

NEW_KEYS = [
    "modelSection", "modelSubtitle", "modelLoaded", "modelNotLoaded",
    "detectionLabel", "detectionConfidence", "validationPerformance",
    "modelPerformance", "map50", "map5095", "precision", "recall",
    "classId", "screeningDisclaimer",
]


def load(code):
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code, data):
    (DIR / f"{code}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    en = load("en")
    for file in sorted(DIR.glob("*.json")):
        code = file.stem
        if code == "en":
            continue
        data = load(code)
        ref = load(REF.get(code, "hi"))
        result = data.setdefault("result", {})
        patch = PATCHES.get(code, PATCHES.get(REF.get(code, "hi"), {}))
        for key in NEW_KEYS:
            if key in en["result"]:
                result[key] = patch.get(key) or ref.get("result", {}).get(key) or en["result"][key]
        if "confidence" in en["result"]:
            result["confidence"] = patch.get("confidence") or ref.get("result", {}).get("confidence") or en["result"]["confidence"]
        save(code, data)
        print(f"patched {code}")


if __name__ == "__main__":
    main()
