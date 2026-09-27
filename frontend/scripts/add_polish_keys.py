# -*- coding: utf-8 -*-
"""Propagate demo polish i18n keys to all locales."""
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
        "dashboard": {
            "monitoring": "निगरानी",
            "riskDistribution": "जोखिम वितरण",
            "analysisTrend": "स्कैन प्रवृत्ति (6 महीने)",
            "unreadAlerts": "अपठित अलर्ट",
        },
        "result": {
            "explainTitle": "मेरे परिणाम समझाएं",
            "explainSubtitle": "अपने वास्तविक स्कैन संदर्भ के साथ किसान-अनुकूल AI व्याख्या प्राप्त करें।",
            "explainAction": "मेरे परिणाम समझाएं",
            "explaining": "BOVIMED समझा रहा है…",
        },
        "cowProfile": {
            "viewProfile": "प्रोफ़ाइल देखें",
            "currentRisk": "वर्तमान जोखिम",
            "latestDetection": "नवीनतम पहचान",
            "analysisCount": "कुल स्कैन",
            "timeline": "स्वास्थ्य समयरेखा",
            "compareLatest": "नवीनतम 2 स्कैन की तुलना करें",
            "noHistory": "इस गाय के लिए अभी कोई स्कैन नहीं।",
        },
        "compare": {
            "title": "स्कैन की तुलना",
            "subtitle": "दो वास्तविक स्कैन के बीच पहचान विश्वास और जोखिम में बदलाव देखें।",
            "selectTwo": "तुलना के लिए स्वास्थ्य इतिहास से ठीक 2 स्कैन चुनें।",
            "action": "चयनित स्कैन की तुलना करें",
            "pick": "तुलना",
            "previous": "पहले का स्कैन",
            "latest": "बाद का स्कैन",
            "changeOverTime": "समय के साथ बदलाव",
            "latestDetail": "नवीनतम स्कैन विवरण",
        },
        "alerts": {
            "viewAnalysis": "विश्लेषण देखें",
            "emptyHint": "सभी गायें वर्तमान में सुरक्षित निगरानी सीमा में हैं।",
        },
    },
    "bn": {
        "dashboard": {
            "monitoring": "পর্যবেক্ষণ",
            "riskDistribution": "ঝুঁকি বিতরণ",
            "analysisTrend": "স্ক্যান প্রবণতা (৬ মাস)",
            "unreadAlerts": "অপঠিত সতর্কতা",
        },
        "result": {
            "explainTitle": "আমার ফলাফল ব্যাখ্যা করুন",
            "explainSubtitle": "আপনার প্রকৃত স্ক্যান প্রসঙ্গ দিয়ে কৃষক-বান্ধব AI ব্যাখ্যা পান।",
            "explainAction": "আমার ফলাফল ব্যাখ্যা করুন",
            "explaining": "BOVIMED ব্যাখ্যা করছে…",
        },
        "cowProfile": {
            "viewProfile": "প্রোফাইল দেখুন",
            "currentRisk": "বর্তমান ঝুঁকি",
            "latestDetection": "সর্বশেষ সনাক্তকরণ",
            "analysisCount": "মোট স্ক্যান",
            "timeline": "স্বাস্থ্য সময়রেখা",
            "compareLatest": "সর্বশেষ ২টি স্ক্যান তুলনা করুন",
            "noHistory": "এই গরুর জন্য এখনও কোনো স্ক্যান নেই।",
        },
        "compare": {
            "title": "স্ক্যান তুলনা",
            "subtitle": "দুটি প্রকৃত স্ক্যানের মধ্যে সনাক্তকরণ আত্মবিশ্বাস ও ঝুঁকির পরিবর্তন দেখুন।",
            "selectTwo": "তুলনার জন্য স্বাস্থ্য ইতিহাস থেকে ঠিক ২টি স্ক্যান নির্বাচন করুন।",
            "action": "নির্বাচিত স্ক্যান তুলনা করুন",
            "pick": "তুলনা",
            "previous": "পূর্ববর্তী স্ক্যান",
            "latest": "পরবর্তী স্ক্যান",
            "changeOverTime": "সময়ের সাথে পরিবর্তন",
            "latestDetail": "সর্বশেষ স্ক্যান বিবরণ",
        },
        "alerts": {
            "viewAnalysis": "বিশ্লেষণ দেখুন",
            "emptyHint": "সব গরু এখন নিরাপদ পর্যবেক্ষণ সীমার মধ্যে আছে।",
        },
    },
    "ur": {
        "dashboard": {
            "monitoring": "نگرانی",
            "riskDistribution": "خطرے کی تقسیم",
            "analysisTrend": "اسکین رجحان (6 ماہ)",
            "unreadAlerts": "غیر پڑھی انتباہات",
        },
        "alerts": {
            "viewAnalysis": "تجزیہ دیکھیں",
            "emptyHint": "تمام مویشی فی الحال محفوظ نگرانی کی حدود میں ہیں۔",
        },
        "result": {
            "explainTitle": "میرے نتیجے کی وضاحت کریں",
            "explainSubtitle": "اپنے اصل اسکین کے ساتھ کسان دوست AI وضاحت حاصل کریں۔",
            "explainAction": "میرے نتیجے کی وضاحت کریں",
            "explaining": "BOVIMED وضاحت کر رہا ہے…",
        },
        "cowProfile": {
            "viewProfile": "پروفائل دیکھیں",
            "currentRisk": "موجودہ خطرہ",
            "latestDetection": "تازہ ترین شناخت",
            "analysisCount": "کل اسکین",
            "timeline": "صحت کی ٹائم لائن",
            "compareLatest": "تازہ ترین 2 اسکین کا موازنہ",
            "noHistory": "اس گائے کے لیے ابھی کوئی اسکین نہیں۔",
        },
        "compare": {
            "title": "اسکین کا موازنہ",
            "subtitle": "دو اصل اسکین کے درمیان شناخت کے اعتماد اور خطرے میں تبدیلی دیکھیں۔",
            "selectTwo": "موازنہ کے لیے صحت کی تاریخ سے بالکل 2 اسکین منتخب کریں۔",
            "action": "منتخب اسکین کا موازنہ",
            "pick": "موازنہ",
            "previous": "پہلے کا اسکین",
            "latest": "بعد کا اسکین",
            "changeOverTime": "وقت کے ساتھ تبدیلی",
            "latestDetail": "تازہ ترین اسکین کی تفصیل",
        },
    },
}


def load(code):
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code, data):
    (DIR / f"{code}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    en = load("en")
    sections = ["dashboard", "result", "cowProfile", "compare", "alerts"]
    for file in sorted(DIR.glob("*.json")):
        code = file.stem
        if code == "en":
            continue
        data = load(code)
        ref_code = REF.get(code, "hi")
        ref = load(ref_code)
        patch = PATCHES.get(code, PATCHES.get(ref_code, PATCHES.get("hi", {})))
        for section in sections:
            if section not in en:
                continue
            target = data.setdefault(section, {})
            ref_patch = PATCHES.get(ref_code, PATCHES.get("hi", {}))
            for key, val in en[section].items():
                translated = (
                    patch.get(section, {}).get(key)
                    or ref_patch.get(section, {}).get(key)
                    or ref.get(section, {}).get(key)
                )
                if translated and translated != val:
                    target[key] = translated
                elif key not in target:
                    target[key] = val
        save(code, data)
        print(f"patched {code}")


if __name__ == "__main__":
    main()
