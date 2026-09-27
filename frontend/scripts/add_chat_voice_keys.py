# -*- coding: utf-8 -*-
"""Add chat/voice UI keys to every locale using language-family references."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"

PATCHES = {
    "hi": {
        "fallbackNotice": "BOVIMED स्थानीय मार्गदर्शन — AI बंद होने पर सत्यापित सुरक्षा नियम।",
        "externalNotice": "BOVIMED AI — लाइव सहायक",
        "unconfiguredNotice": "AI सहायक सर्वर पर कॉन्फ़िगर नहीं है। backend .env में BOVIMED_LLM_ENABLED और API key सेट करें।",
        "localNotice": "BOVIMED स्थानीय मार्गदर्शन — सत्यापित सुरक्षा नियम।",
        "errorNotice": "AI अभी उत्तर नहीं दे सका। सुरक्षित स्थानीय मार्गदर्शन दिखाया जा रहा है।",
        "aiStatusLive": "लाइव AI",
        "aiStatusLocal": "स्थानीय मार्गदर्शन",
        "aiStatusUnconfigured": "AI कॉन्फ़िगर नहीं",
        "aiStatusError": "AI अनुपलब्ध",
        "listening": "सुन रहा है…",
        "speak": "बोलें",
        "stopSpeaking": "बोलना बंद करें",
        "micDenied": "माइक्रोफ़ोन अनुमति अस्वीकार। आप टाइप करके भी पूछ सकते हैं।",
        "micUnsupported": "इस ब्राउज़र में वॉइस इनपुट समर्थित नहीं है।",
        "speechNoInput": "कोई आवाज़ नहीं मिली। पुनः प्रयास करें।",
        "speechError": "स्पीच रिकग्निशन त्रुटि। पुनः प्रयास करें।",
        "speechTimeout": "सुनने का समय समाप्त। पुनः प्रयास करें।",
        "speechLangUnavailable": "इस भाषा के लिए स्पीच रिकग्निशन उपलब्ध नहीं है।",
        "ttsUnsupported": "इस ब्राउज़र में टेक्स्ट-टू-स्पीच समर्थित नहीं है।",
        "languageFallback": "AI आपकी भाषा में विश्वसनीय उत्तर नहीं दे सका। नीचे स्थानीय मार्गदर्शन है।",
    },
    "bn": {
        "fallbackNotice": "BOVIMED স্থানীয় নির্দেশনা — AI বন্ধ থাকলে যাচাইকৃত নিরাপত্তা নিয়ম।",
        "externalNotice": "BOVIMED AI — লাইভ সহায়ক",
        "unconfiguredNotice": "AI সহায়ক সার্ভারে কনফিগার করা নেই। backend .env-এ BOVIMED_LLM_ENABLED এবং API key সেট করুন।",
        "localNotice": "BOVIMED স্থানীয় নির্দেশনা — যাচাইকৃত নিরাপত্তা নিয়ম।",
        "errorNotice": "AI এখন উত্তর দিতে পারছে না। নিরাপদ স্থানীয় নির্দেশনা দেখানো হচ্ছে।",
        "aiStatusLive": "লাইভ AI",
        "aiStatusLocal": "স্থানীয় নির্দেশনা",
        "aiStatusUnconfigured": "AI কনফিগার নেই",
        "aiStatusError": "AI অনুপলব্ধ",
        "listening": "শুনছি…",
        "speak": "বলুন",
        "stopSpeaking": "বলা বন্ধ করুন",
        "micDenied": "মাইক্রোফোন অনুমতি প্রত্যাখ্যান। টাইপ করেও জিজ্ঞাসা করতে পারেন।",
        "micUnsupported": "এই ব্রাউজারে ভয়েস ইনপুট সমর্থিত নয়।",
        "speechNoInput": "কোনো কথা শোনা যায়নি। আবার চেষ্টা করুন।",
        "speechError": "স্পিচ রিকগনিশন ত্রুটি। আবার চেষ্টা করুন।",
        "speechTimeout": "শোনার সময় শেষ। আবার চেষ্টা করুন।",
        "speechLangUnavailable": "এই ভাষায় স্পিচ রিকগনিশন উপলব্ধ নয়।",
        "ttsUnsupported": "এই ব্রাউজারে টেক্সট-টু-স্পিচ সমর্থিত নয়।",
        "languageFallback": "AI আপনার ভাষায় নির্ভরযোগ্য উত্তর দিতে পারেনি। নিচে স্থানীয় নির্দেশনা আছে।",
    },
    "ur": {
        "fallbackNotice": "BOVIMED مقامی رہنمائی — AI بند ہونے پر تصدیق شدہ حفاظتی اصول۔",
        "externalNotice": "BOVIMED AI — لائیو معاون",
        "unconfiguredNotice": "AI معاون سرور پر ترتیب نہیں ہے۔ backend .env میں BOVIMED_LLM_ENABLED اور API key سیٹ کریں۔",
        "localNotice": "BOVIMED مقامی رہنمائی — تصدیق شدہ حفاظتی اصول۔",
        "errorNotice": "AI ابھی جواب نہیں دے سکا۔ محفوظ مقامی رہنمائی دکھائی جا رہی ہے۔",
        "aiStatusLive": "لائیو AI",
        "aiStatusLocal": "مقامی رہنمائی",
        "aiStatusUnconfigured": "AI ترتیب نہیں",
        "aiStatusError": "AI دستیاب نہیں",
        "listening": "سن رہا ہے…",
        "speak": "بولیں",
        "stopSpeaking": "بولنا بند کریں",
        "micDenied": "مائیکروفون کی اجازت مسترد۔ آپ ٹائپ کر کے بھی پوچھ سکتے ہیں۔",
        "micUnsupported": "اس براؤزر میں وائس ان پٹ دستیاب نہیں۔",
        "speechNoInput": "کوئی آواز نہیں سنی گئی۔ دوبارہ کوشش کریں۔",
        "speechError": "اسپیچ ریکگنیشن خرابی۔ دوبارہ کوشش کریں۔",
        "speechTimeout": "سننے کا وقت ختم۔ دوبارہ کوشش کریں۔",
        "speechLangUnavailable": "اس زبان کے لیے اسپیچ ریکگنیشن دستیاب نہیں۔",
        "ttsUnsupported": "اس براؤزر میں ٹیکسٹ ٹو اسپیچ دستیاب نہیں۔",
        "languageFallback": "AI آپ کی زبان میں قابلِ اعتماد جواب نہیں دے سکا۔ نیچے مقامی رہنمائی ہے۔",
    },
    "mr": {
        "fallbackNotice": "BOVIMED स्थानिक मार्गदर्शन — AI बंद असल्यास सत्यापित सुरक्षा नियम।",
        "externalNotice": "BOVIMED AI — थेट सहाय्यक",
        "unconfiguredNotice": "AI सहाय्यक सर्व्हरवर कॉन्फिगर नाही. backend .env मध्ये BOVIMED_LLM_ENABLED आणि API key सेट करा.",
        "localNotice": "BOVIMED स्थानिक मार्गदर्शन — सत्यापित सुरक्षा नियम।",
        "errorNotice": "AI आत्ता उत्तर देऊ शकले नाही. सुरक्षित स्थानिक मार्गदर्शन दाखवले आहे.",
        "aiStatusLive": "थेट AI",
        "aiStatusLocal": "स्थानिक मार्गदर्शन",
        "aiStatusUnconfigured": "AI कॉन्फिगर नाही",
        "aiStatusError": "AI अनुपलब्ध",
        "listening": "ऐकत आहे…",
        "speak": "बोला",
        "stopSpeaking": "बोलणे थांबवा",
        "micDenied": "मायक्रोफोन परवानगी नाकारली. टाइप करूनही विचारू शकता.",
        "micUnsupported": "या ब्राउझरमध्ये व्हॉइस इनपुट समर्थित नाही.",
        "speechNoInput": "कोणताही आवाज ऐकला गेला नाही. पुन्हा प्रयत्न करा.",
        "speechError": "स्पीच रेकग्निशन त्रुटी. पुन्हा प्रयत्न करा.",
        "speechTimeout": "ऐकण्याची वेळ संपली. पुन्हा प्रयत्न करा.",
        "speechLangUnavailable": "या भाषेसाठी स्पीच रेकग्निशन उपलब्ध नाही.",
        "ttsUnsupported": "या ब्राउझरमध्ये टेक्स्ट-टू-स्पीच समर्थित नाही.",
        "languageFallback": "AI तुमच्या भाषेत विश्वासार्ह उत्तर देऊ शकले नाही. खाली स्थानिक मार्गदर्शन आहे.",
    },
    "kn": {
        "listening": "ಕೇಳುತ್ತಿದೆ…",
        "speak": "ಮಾತನಾಡಿ",
        "stopSpeaking": "ಮಾತು ನಿಲ್ಲಿಸಿ",
        "aiStatusLive": "ಲೈವ್ AI",
        "aiStatusLocal": "ಸ್ಥಳೀಯ ಮಾರ್ಗದರ್ಶನ",
        "externalNotice": "BOVIMED AI — ಲೈವ್ ಸಹಾಯಕ",
        "localNotice": "BOVIMED ಸ್ಥಳೀಯ ಮಾರ್ಗದರ್ಶನ — ಪರಿಶೀಲಿತ ಸುರಕ್ಷತಾ ನಿಯಮಗಳು.",
        "unconfiguredNotice": "AI ಸಹಾಯಕ ಸರ್ವರ್‌ನಲ್ಲಿ ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ. backend .env ನಲ್ಲಿ API key ಹೊಂದಿಸಿ.",
        "errorNotice": "AI ಈಗ ಉತ್ತರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಸುರಕ್ಷಿತ ಸ್ಥಳೀಯ ಮಾರ್ಗದರ್ಶನ ತೋರಿಸಲಾಗಿದೆ.",
        "fallbackNotice": "BOVIMED ಸ್ಥಳೀಯ ಮಾರ್ಗದರ್ಶನ — AI ಆಫ್ ಆಗಿದ್ದಾಗ ಪರಿಶೀಲಿತ ನಿಯಮಗಳು.",
        "aiStatusUnconfigured": "AI ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ",
        "aiStatusError": "AI ಲಭ್ಯವಿಲ್ಲ",
        "micDenied": "ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ನಿರಾಕರಿಸಲಾಗಿದೆ.",
        "micUnsupported": "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ವಾಯ್ಸ್ ಇನ್‌ಪುಟ್ ಬೆಂಬಲಿತವಲ್ಲ.",
        "speechNoInput": "ಯಾವುದೇ ಧ್ವನಿ ಕೇಳಿಸಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "speechError": "ಸ್ಪೀಚ್ ರೆಕಗ್ನಿಷನ್ ದೋಷ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "speechTimeout": "ಕೇಳುವ ಸಮಯ ಮುಗಿದಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "speechLangUnavailable": "ಈ ಭಾಷೆಗೆ ಸ್ಪೀಚ್ ರೆಕಗ್ನಿಷನ್ ಲಭ್ಯವಿಲ್ಲ.",
        "ttsUnsupported": "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಟೆಕ್ಸ್ಟ್-ಟು-ಸ್ಪೀಚ್ ಬೆಂಬಲಿತವಲ್ಲ.",
        "languageFallback": "AI ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ನಂಬಿಕಸ್ತ ಉತ್ತರ ನೀಡಲಿಲ್ಲ.",
    },
}

REFERENCE = {
    "as": "bn",
    "or": "bn",
    "mni": "bn",
    "sat": "bn",
    "ne": "hi",
    "kok": "mr",
    "sa": "hi",
    "brx": "hi",
    "doi": "hi",
    "mai": "hi",
    "sd": "ur",
    "ks": "ur",
    "gu": "mr",
    "te": "kn",
    "ta": "kn",
    "ml": "kn",
    "pa": "hi",
}


def load(code: str) -> dict:
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code: str, data: dict) -> None:
    (DIR / f"{code}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def patch_for(code: str) -> dict:
    if code in PATCHES:
        return PATCHES[code]
    ref = REFERENCE.get(code, "hi")
    return PATCHES.get(ref, PATCHES["hi"])


def main() -> None:
    en = load("en")
    keys = [k for k in en["chat"] if k not in ("chips",) and not isinstance(en["chat"][k], dict)]
    voice_keys = [
        k
        for k in keys
        if k
        in {
            "fallbackNotice",
            "externalNotice",
            "unconfiguredNotice",
            "localNotice",
            "errorNotice",
            "aiStatusLive",
            "aiStatusLocal",
            "aiStatusUnconfigured",
            "aiStatusError",
            "listening",
            "speak",
            "stopSpeaking",
            "micDenied",
            "micUnsupported",
            "speechNoInput",
            "speechError",
            "speechTimeout",
            "speechLangUnavailable",
            "ttsUnsupported",
            "languageFallback",
        }
    ]

    for file in sorted(DIR.glob("*.json")):
        code = file.stem
        if code == "en":
            continue
        data = load(code)
        chat = data.setdefault("chat", {})
        source = patch_for(code)
        for key in voice_keys:
            chat[key] = source.get(key, en["chat"][key])
        save(code, data)
        print(f"patched {code}")


if __name__ == "__main__":
    main()
