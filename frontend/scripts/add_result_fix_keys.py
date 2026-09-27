# -*- coding: utf-8 -*-
"""Propagate result page fix i18n keys to all locales."""
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
        "result.detectionSummaryOnly": "स्क्रीनिंग परिणाम उपलब्ध है, लेकिन इस स्कैन के लिए प्रति-वस्तु YOLO निर्देशांक संग्रहीत नहीं हैं।",
        "result.noPrimaryDetected": "कोई स्पष्ट स्वास्थ्य संकेत नहीं मिला।",
        "result.imageUnavailable": "छवि लोड नहीं हो सकी। विश्लेषण डेटा नीचे उपलब्ध है।",
        "result.classFindings.Mastitis_infected_udder": "संभावित मास्टाइटिस संकेत पाए गए",
        "result.classFindings.Lumpy_infected_cow": "संभावित संक्रमण संबंधी संकेत पाए गए",
        "result.classFindings.Healthy_udder": "स्वस्थ थन के संकेत पाए गए",
    },
    "bn": {
        "result.detectionSummaryOnly": "স্ক্রিনিং ফলাফল উপলব্ধ, তবে এই স্ক্যানের জন্য প্রতি-অবজেক্ট YOLO স্থানাঙ্ক সংরক্ষিত হয়নি।",
        "result.noPrimaryDetected": "কোনো স্পষ্ট স্বাস্থ্য সংকেত পাওয়া যায়নি।",
        "result.imageUnavailable": "ছবি লোড করা যায়নি। বিশ্লেষণের তথ্য নিচে উপলব্ধ।",
        "result.classFindings.Mastitis_infected_udder": "সম্ভাব্য মাস্টাইটিস সংকেত সনাক্ত",
        "result.classFindings.Lumpy_infected_cow": "সম্ভাব্য সংক্রমণ সংক্রান্ত সংকেত সনাক্ত",
        "result.classFindings.Healthy_udder": "সুস্থ স্তনের সংকেত সনাক্ত",
    },
    "mr": {
        "result.noPrimaryDetected": "स्पष्ट आरोग्य संकेत आढळले नाहीत.",
        "result.imageUnavailable": "प्रतिमा लोड करता आली नाही. विश्लेषण डेटा खाली उपलब्ध आहे.",
        "result.classFindings.Mastitis_infected_udder": "संभाव्य मास्टायटिस संकेत आढळले",
        "result.classFindings.Lumpy_infected_cow": "संभाव्य संसर्ग संबंधित संकेत आढळले",
        "result.classFindings.Healthy_udder": "निरोगी थनाचे संकेत आढळले",
    },
    "kn": {
        "result.noPrimaryDetected": "ಸ್ಪಷ್ಟ ಆರೋಗ್ಯ ಸೂಚಕಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        "result.imageUnavailable": "ಚಿತ್ರವನ್ನು ಲೋಡ್ ಮಾಡಲಾಗಲಿಲ್ಲ. ವಿಶ್ಲೇಷಣೆ ಡೇಟಾ ಕೆಳಗೆ ಲಭ್ಯವಿದೆ.",
        "result.classFindings.Mastitis_infected_udder": "ಸಂಭಾವ್ಯ ಮಾಸ್ಟೈಟಿಸ್ ಸೂಚಕಗಳು ಪತ್ತೆಯಾಗಿದೆ",
        "result.classFindings.Lumpy_infected_cow": "ಸಂಭಾವ್ಯ ಸೋಂಕು ಸಂಬಂಧಿತ ಸೂಚಕಗಳು ಪತ್ತೆಯಾಗಿದೆ",
        "result.classFindings.Healthy_udder": "ಆರೋಗ್ಯಕರ ಸ್ತನದ ಸೂಚಕಗಳು ಪತ್ತೆಯಾಗಿದೆ",
    },
    "ur": {
        "result.noPrimaryDetected": "کوئی واضح صحت کا اشارہ نہیں ملا۔",
        "result.imageUnavailable": "تصویر لوڈ نہیں ہو سکی۔ تجزیے کا ڈیٹا نیچے دستیاب ہے۔",
        "result.classFindings.Mastitis_infected_udder": "ممکنہ ماسٹائٹس کے اشارے پائے گئے",
        "result.classFindings.Lumpy_infected_cow": "ممکنہ انفیکشن سے متعلق اشارے پائے گئے",
        "result.classFindings.Healthy_udder": "صحت مند تھن کے اشارے پائے گئے",
    },
}


def flatten(obj, prefix=""):
    out = {}
    for k, v in obj.items():
        nk = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, nk))
        else:
            out[nk] = v
    return out


def unflatten(flat):
    root = {}
    for k, v in flat.items():
        parts = k.split(".")
        cur = root
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


def merge(code, patch):
    path = DIR / f"{code}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    flat = flatten(data)
    flat.update(patch)
    path.write_text(json.dumps(unflatten(flat), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {code}")


def main():
    en = flatten(json.loads((DIR / "en.json").read_text(encoding="utf-8")))
    keys = [
        k
        for k in en
        if k.startswith("result.noPrimaryDetected")
        or k.startswith("result.imageUnavailable")
        or k.startswith("result.detectionSummaryOnly")
        or k.startswith("result.classFindings.")
    ]
    for f in sorted(DIR.glob("*.json")):
        code = f.stem
        if code == "en":
            continue
        if code in PATCHES:
            merge(code, PATCHES[code])
            continue
        ref = REF.get(code)
        if ref and ref in PATCHES:
            merge(code, PATCHES[ref])
        elif ref:
            ref_flat = flatten(json.loads((DIR / f"{ref}.json").read_text(encoding="utf-8")))
            merge(code, {k: ref_flat[k] for k in keys if k in ref_flat})
        else:
            merge(code, {k: en[k] for k in keys})


if __name__ == "__main__":
    main()
