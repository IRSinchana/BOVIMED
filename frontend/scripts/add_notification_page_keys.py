# -*- coding: utf-8 -*-
"""Add notification page / bell i18n keys to all 22 locales."""
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
        "notifications.loading": "सूचनाएं लोड हो रही हैं…",
        "notifications.loadError": "सूचनाएं लोड नहीं हो सकीं। कृपया पुनः प्रयास करें।",
        "notifications.viewAll": "सभी सूचनाएं देखें",
        "notifications.cow": "गाय",
        "notifications.risk": "जोखिम",
        "notifications.confidence": "विश्वास",
        "notifications.unread": "अपठित",
        "notifications.read": "पढ़ा हुआ",
        "notifications.mildRisk.title": "निरीक्षण की सिफारिश",
        "notifications.mildRisk.message": "{{cowId}} में संभावित {{detection}} संकेत। जोखिम: {{risk}}। पहचान विश्वास: {{confidence}}%। निरंतर निरीक्षण करें।",
    },
    "bn": {
        "notifications.loading": "বিজ্ঞপ্তি লোড হচ্ছে…",
        "notifications.loadError": "বিজ্ঞপ্তি লোড করা যায়নি। আবার চেষ্টা করুন।",
        "notifications.viewAll": "সব বিজ্ঞপ্তি দেখুন",
        "notifications.cow": "গরু",
        "notifications.risk": "ঝুঁকি",
        "notifications.confidence": "আস্থা",
        "notifications.unread": "অপঠিত",
        "notifications.read": "পঠিত",
        "notifications.mildRisk.title": "পর্যবেক্ষণের পরামর্শ",
        "notifications.mildRisk.message": "{{cowId}}-এ সম্ভাব্য {{detection}} লক্ষণ। ঝুঁকি: {{risk}}। সনাক্তকরণ আস্থা: {{confidence}}%। পর্যবেক্ষণ চালিয়ে যান।",
    },
    "mr": {
        "notifications.loading": "सूचना लोड होत आहेत…",
        "notifications.loadError": "सूचना लोड होऊ शकल्या नाहीत. पुन्हा प्रयत्न करा.",
        "notifications.viewAll": "सर्व सूचना पहा",
        "notifications.cow": "गाय",
        "notifications.risk": "धोका",
        "notifications.confidence": "विश्वास",
        "notifications.unread": "न वाचलेले",
        "notifications.read": "वाचलेले",
        "notifications.mildRisk.title": "देखरेख शिफारस",
        "notifications.mildRisk.message": "{{cowId}} मध्ये संभाव्य {{detection}} चिन्हे. धोका: {{risk}}. ओळख विश्वास: {{confidence}}%. निरंतर देखरेख करा.",
    },
    "kn": {
        "notifications.loading": "ಅಧಿಸೂಚನೆಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ…",
        "notifications.loadError": "ಅಧಿಸೂಚನೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "notifications.viewAll": "ಎಲ್ಲಾ ಅಧಿಸೂಚನೆಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
        "notifications.cow": "ಹಸು",
        "notifications.risk": "ಅಪಾಯ",
        "notifications.confidence": "ವಿಶ್ವಾಸ",
        "notifications.unread": "ಓದದ",
        "notifications.read": "ಓದಿದ",
        "notifications.mildRisk.title": "ಮೇಲ್ವಿಚಾರಣೆ ಶಿಫಾರಸು",
        "notifications.mildRisk.message": "{{cowId}} ನಲ್ಲಿ ಸಂಭವನೀಯ {{detection}} ಸೂಚಕಗಳು. ಅಪಾಯ: {{risk}}. ಪತ್ತೆ ವಿಶ್ವಾಸ: {{confidence}}%. ಮೇಲ್ವಿಚಾರಣೆ ಮುಂದುವರಿಸಿ.",
    },
    "ur": {
        "notifications.loading": "اطلاعات لوڈ ہو رہی ہیں…",
        "notifications.loadError": "اطلاعات لوڈ نہیں ہو سکیں۔ دوبارہ کوشش کریں۔",
        "notifications.viewAll": "تمام اطلاعات دیکھیں",
        "notifications.cow": "گائے",
        "notifications.risk": "خطرہ",
        "notifications.confidence": "اعتماد",
        "notifications.unread": "نہ پڑھی",
        "notifications.read": "پڑھی",
        "notifications.mildRisk.title": "نگرانی کی سفارش",
        "notifications.mildRisk.message": "{{cowId}} میں ممکنہ {{detection}} اشارے۔ خطرہ: {{risk}}۔ شناخت کا اعتماد: {{confidence}}%۔ نگرانی جاری رکھیں۔",
    },
    "ta": {
        "notifications.loading": "அறிவிப்புகள் ஏற்றப்படுகின்றன…",
        "notifications.loadError": "அறிவிப்புகளை ஏற்ற முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
        "notifications.viewAll": "அனைத்து அறிவிப்புகளையும் காண்க",
        "notifications.cow": "மாடு",
        "notifications.risk": "ஆபத்து",
        "notifications.confidence": "நம்பிக்கை",
        "notifications.unread": "படிக்காதது",
        "notifications.read": "படித்தது",
        "notifications.mildRisk.title": "கண்காணிப்பு பரிந்துரை",
        "notifications.mildRisk.message": "{{cowId}} இல் சாத்தியமான {{detection}} அறிகுறிகள். ஆபத்து: {{risk}}. கண்டறிதல் நம்பிக்கை: {{confidence}}%. தொடர்ந்து கண்காணிக்கவும்.",
    },
    "te": {
        "notifications.loading": "నోటిఫికేషన్‌లు లోడ్ అవుతున్నాయి…",
        "notifications.loadError": "నోటిఫికేషన్‌లు లోడ్ చేయలేకపోయాము. మళ్లీ ప్రయత్నించండి.",
        "notifications.viewAll": "అన్ని నోటిఫికేషన్‌లు చూడండి",
        "notifications.cow": "ఆవు",
        "notifications.risk": "ప్రమాదం",
        "notifications.confidence": "నమ్మకం",
        "notifications.unread": "చదవనిది",
        "notifications.read": "చదివినది",
        "notifications.mildRisk.title": "పర్యవేక్షణ సిఫారసు",
        "notifications.mildRisk.message": "{{cowId}} లో సంభావ్య {{detection}} సూచనలు. ప్రమాదం: {{risk}}. గుర్తింపు నమ్మకం: {{confidence}}%. పర్యవేక్షణ కొనసాగించండి.",
    },
    "gu": {
        "notifications.loading": "સૂચનાઓ લોડ થઈ રહી છે…",
        "notifications.loadError": "સૂચનાઓ લોડ થઈ શકી નહીં. ફરી પ્રયાસ કરો.",
        "notifications.viewAll": "બધી સૂચનાઓ જુઓ",
        "notifications.cow": "ગાય",
        "notifications.risk": "જોખમ",
        "notifications.confidence": "વિશ્વાસ",
        "notifications.unread": "ન વાંચેલ",
        "notifications.read": "વાંચેલ",
        "notifications.mildRisk.title": "નિરીક્ષણની ભલામણ",
        "notifications.mildRisk.message": "{{cowId}} માં સંભવિત {{detection}} ચિહ્નો. જોખમ: {{risk}}. ઓળખ વિશ્વાસ: {{confidence}}%. સતત નિરીક્ષણ કરો.",
    },
    "pa": {
        "notifications.loading": "ਸੂਚਨਾਵਾਂ ਲੋਡ ਹੋ ਰਹੀਆਂ ਹਨ…",
        "notifications.loadError": "ਸੂਚਨਾਵਾਂ ਲੋਡ ਨਹੀਂ ਹੋ ਸਕੀਆਂ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        "notifications.viewAll": "ਸਾਰੀਆਂ ਸੂਚਨਾਵਾਂ ਦੇਖੋ",
        "notifications.cow": "ਗਾਂ",
        "notifications.risk": "ਜੋਖਮ",
        "notifications.confidence": "ਭਰੋਸਾ",
        "notifications.unread": "ਨਾ ਪੜ੍ਹੀ",
        "notifications.read": "ਪੜ੍ਹੀ",
        "notifications.mildRisk.title": "ਨਿਗਰਾਨੀ ਦੀ ਸਿਫਾਰਸ਼",
        "notifications.mildRisk.message": "{{cowId}} ਵਿੱਚ ਸੰਭਾਵਿਤ {{detection}} ਸੰਕੇਤ। ਜੋਖਮ: {{risk}}। ਪਛਾਣ ਭਰੋਸਾ: {{confidence}}%। ਨਿਰੰਤਰ ਨਿਗਰਾਨੀ ਕਰੋ।",
    },
    "ml": {
        "notifications.loading": "അറിയിപ്പുകൾ ലോഡ് ചെയ്യുന്നു…",
        "notifications.loadError": "അറിയിപ്പുകൾ ലോഡ് ചെയ്യാൻ കഴിഞ്ഞില്ല. വീണ്ടും ശ്രമിക്കുക.",
        "notifications.viewAll": "എല്ലാ അറിയിപ്പുകളും കാണുക",
        "notifications.cow": "പശു",
        "notifications.risk": "അപകടം",
        "notifications.confidence": "വിശ്വാസം",
        "notifications.unread": "വായിക്കാത്തത്",
        "notifications.read": "വായിച്ചത്",
        "notifications.mildRisk.title": "നിരീക്ഷണം ശുപാർശ ചെയ്യുന്നു",
        "notifications.mildRisk.message": "{{cowId}} ൽ സാധ്യമായ {{detection}} സൂചനകൾ. അപകടം: {{risk}}. കണ്ടെത്തൽ വിശ്വാസം: {{confidence}}%. നിരീക്ഷണം തുടരുക.",
    },
    "or": {
        "notifications.loading": "ବିଜ୍ଞପ୍ତି ଲୋଡ୍ ହେଉଛି…",
        "notifications.loadError": "ବିଜ୍ଞପ୍ତି ଲୋଡ୍ ହୋଇପାରିଲା ନାହିଁ। ପୁନର୍ବାର ଚେଷ୍ଟା କରନ୍ତୁ।",
        "notifications.viewAll": "ସମସ୍ତ ବିଜ୍ଞପ୍ତି ଦେଖନ୍ତୁ",
        "notifications.cow": "ଗାଈ",
        "notifications.risk": "ବିପଦ",
        "notifications.confidence": "ବିଶ୍ୱାସ",
        "notifications.unread": "ନ ପଢ଼ା",
        "notifications.read": "ପଢ଼ା",
        "notifications.mildRisk.title": "ନିରୀକ୍ଷଣ ସୁପାରିଶ",
        "notifications.mildRisk.message": "{{cowId}} ରେ ସମ୍ଭାବ୍ୟ {{detection}} ଚିହ୍ନ। ବିପଦ: {{risk}}। ଚିହ୍ନଟ ବିଶ୍ୱାସ: {{confidence}}%। ନିରନ୍ତର ନିରୀକ୍ଷଣ କରନ୍ତୁ।",
    },
    "as": {
        "notifications.loading": "জাননী ল'ড হৈ আছে…",
        "notifications.loadError": "জাননী ল'ড কৰিব পৰা নগ'ল। পুনৰ চেষ্টা কৰক।",
        "notifications.viewAll": "সকলো জাননী চাওক",
        "notifications.cow": "গাই",
        "notifications.risk": "বিপদাশংকা",
        "notifications.confidence": "বিশ্বাস",
        "notifications.unread": "নপঢ়া",
        "notifications.read": "পঢ়া",
        "notifications.mildRisk.title": "নিৰীক্ষণৰ পৰামৰ্শ",
        "notifications.mildRisk.message": "{{cowId}} ত সম্ভাৱ্য {{detection}} সংকেত। বিপদাশংকা: {{risk}}। চিনাক্তকৰণ বিশ্বাস: {{confidence}}%। নিৰন্তৰ নিৰীক্ষণ কৰক।",
    },
    "ne": {
        "notifications.loading": "सूचनाहरू लोड हुँदैछ…",
        "notifications.loadError": "सूचनाहरू लोड गर्न सकिएन। फेरि प्रयास गर्नुहोस्।",
        "notifications.viewAll": "सबै सूचनाहरू हेर्नुहोस्",
        "notifications.cow": "गाई",
        "notifications.risk": "जोखिम",
        "notifications.confidence": "विश्वास",
        "notifications.unread": "नपढिएको",
        "notifications.read": "पढिएको",
        "notifications.mildRisk.title": "अनुगमन सिफारिस",
        "notifications.mildRisk.message": "{{cowId}} मा सम्भावित {{detection}} संकेत। जोखिम: {{risk}}। पहिचान विश्वास: {{confidence}}%। निरन्तर अनुगमन गर्नुहोस्।",
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


def merge_locale(code, flat_patch):
    path = DIR / f"{code}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    flat = flatten(data)
    flat.update(flat_patch)
    path.write_text(json.dumps(unflatten(flat), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {code}.json")


def main():
    new_keys = [
        "notifications.loading",
        "notifications.loadError",
        "notifications.viewAll",
        "notifications.cow",
        "notifications.risk",
        "notifications.confidence",
        "notifications.unread",
        "notifications.read",
        "notifications.mildRisk.title",
        "notifications.mildRisk.message",
    ]
    for path in sorted(DIR.glob("*.json")):
        lang = path.stem
        if lang == "en":
            continue
        if lang in PATCHES:
            merge_locale(lang, PATCHES[lang])
            continue
        ref = REF.get(lang)
        if ref and ref in PATCHES:
            merge_locale(lang, PATCHES[ref])
            continue
        if ref:
            ref_flat = flatten(json.loads((DIR / f"{ref}.json").read_text(encoding="utf-8")))
            patch = {k: ref_flat[k] for k in new_keys if k in ref_flat}
            merge_locale(lang, patch)
        else:
            en_flat = flatten(json.loads((DIR / "en.json").read_text(encoding="utf-8")))
            merge_locale(lang, {k: en_flat[k] for k in new_keys})


if __name__ == "__main__":
    main()
