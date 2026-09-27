# -*- coding: utf-8 -*-
"""Propagate rebuilt alerts page notification keys to all 22 locales."""
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
        "notifications.pageSubtitle": "महत्वपूर्ण गाय स्वास्थ्य घटनाओं के बारे में अपडेट रहें।",
        "notifications.emptyTitle": "कोई नई सूचना नहीं",
        "notifications.emptyHint": "गाय स्वास्थ्य और AI स्क्रीनिंग परिणामों की सूचनाएं यहां दिखाई देंगी।",
        "notifications.viewResult": "परिणाम देखें",
        "notifications.summaryAll": "सभी",
        "notifications.summaryUnread": "अपठित",
        "notifications.summaryHighRisk": "उच्च जोखिम",
        "notifications.summaryRecent": "हाल का",
        "notifications.condition": "स्थिति",
        "notifications.screeningNote": "AI स्क्रीनिंग ने निकट निगरानी की आवश्यकता वाले संकेत पाए।",
        "notifications.screeningNoteModerate": "AI स्क्रीनिंग ने निकट निगरानी की आवश्यकता वाले संकेत पाए।",
        "notifications.screeningNoteHigh": "AI स्क्रीनिंग ने पशु चिकित्सा ध्यान की आवश्यकता वाले संकेत पाए।",
        "notifications.markRead": "पढ़ा हुआ चिह्नित करें",
        "notifications.loading": "सूचनाएं लोड हो रही हैं...",
    },
    "bn": {
        "notifications.pageSubtitle": "গুরুত্বপূর্ণ গরু স্বাস্থ্য ঘটনা সম্পর্কে আপডেট থাকুন।",
        "notifications.emptyTitle": "কোনো নতুন বিজ্ঞপ্তি নেই",
        "notifications.emptyHint": "গরু স্বাস্থ্য এবং AI স্ক্রিনিং ফলাফলের বিজ্ঞপ্তি এখানে দেখা যাবে।",
        "notifications.viewResult": "ফলাফল দেখুন",
        "notifications.summaryAll": "সব",
        "notifications.summaryUnread": "অপঠিত",
        "notifications.summaryHighRisk": "উচ্চ ঝুঁকি",
        "notifications.summaryRecent": "সাম্প্রতিক",
        "notifications.condition": "অবস্থা",
        "notifications.screeningNote": "AI স্ক্রিনিং নিকট পর্যবেক্ষণের প্রয়োজনীয় লক্ষণ সনাক্ত করেছে।",
        "notifications.screeningNoteModerate": "AI স্ক্রিনিং নিকট পর্যবেক্ষণের প্রয়োজনীয় লক্ষণ সনাক্ত করেছে।",
        "notifications.screeningNoteHigh": "AI স্ক্রিনিং পশুচিকিৎসকের মনোযোগের প্রয়োজনীয় লক্ষণ সনাক্ত করেছে।",
        "notifications.markRead": "পঠিত চিহ্নিত করুন",
        "notifications.loading": "বিজ্ঞপ্তি লোড হচ্ছে...",
    },
    "mr": {
        "notifications.pageSubtitle": "महत्त्वाच्या गायींच्या आरोग्य घटनांबद्दल अद्ययावत राहा.",
        "notifications.emptyTitle": "नवीन सूचना नाहीत",
        "notifications.emptyHint": "गायींच्या आरोग्य आणि AI स्क्रीनिंग निकालांच्या सूचना येथे दिसतील.",
        "notifications.viewResult": "निकाल पहा",
        "notifications.summaryAll": "सर्व",
        "notifications.summaryUnread": "न वाचलेले",
        "notifications.summaryHighRisk": "उच्च धोका",
        "notifications.summaryRecent": "अलीकडील",
        "notifications.condition": "स्थिती",
        "notifications.screeningNote": "AI स्क्रीनिंगने जवळून निरीक्षण आवश्यक असलेले चिन्हे आढळली.",
        "notifications.screeningNoteModerate": "AI स्क्रीनिंगने जवळून निरीक्षण आवश्यक असलेले चिन्हे आढळली.",
        "notifications.screeningNoteHigh": "AI स्क्रीनिंगने पशुवैद्यकीय लक्ष देण्याची गरज असलेले चिन्हे आढळली.",
        "notifications.markRead": "वाचलेले चिन्हांकित करा",
        "notifications.loading": "सूचना लोड होत आहेत...",
    },
    "kn": {
        "notifications.pageSubtitle": "ಪ್ರಮುಖ ಹಸು ಆರೋಗ್ಯ ಘಟನೆಗಳ ಬಗ್ಗೆ ಅಪ್‌ಡೇಟ್ ಆಗಿರಿ.",
        "notifications.emptyTitle": "ಹೊಸ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ",
        "notifications.emptyHint": "ಹಸು ಆರೋಗ್ಯ ಮತ್ತು AI ಸ್ಕ್ರೀನಿಂಗ್ ಫಲಿತಾಂಶಗಳ ಅಧಿಸೂಚನೆಗಳು ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ.",
        "notifications.viewResult": "ಫಲಿತಾಂಶ ವೀಕ್ಷಿಸಿ",
        "notifications.summaryAll": "ಎಲ್ಲಾ",
        "notifications.summaryUnread": "ಓದದ",
        "notifications.summaryHighRisk": "ಅಧಿಕ ಅಪಾಯ",
        "notifications.summaryRecent": "ಇತ್ತೀಚಿನ",
        "notifications.condition": "ಸ್ಥಿತಿ",
        "notifications.screeningNote": "AI ಸ್ಕ್ರೀನಿಂಗ್ ಹತ್ತಿರದ ಮೇಲ್ವಿಚಾರಣೆ ಅಗತ್ಯವಿರುವ ಕಂಡಿಕೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿದೆ.",
        "notifications.screeningNoteModerate": "AI ಸ್ಕ್ರೀನಿಂಗ್ ಹತ್ತಿರದ ಮೇಲ್ವಿಚಾರಣೆ ಅಗತ್ಯವಿರುವ ಕಂಡಿಕೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿದೆ.",
        "notifications.screeningNoteHigh": "AI ಸ್ಕ್ರೀನಿಂಗ್ ಪಶುವೈದ್ಯಕೀಯ ಗಮನ ಅಗತ್ಯವಿರುವ ಕಂಡಿಕೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿದೆ.",
        "notifications.markRead": "ಓದಿದ ಎಂದು ಗುರುತಿಸಿ",
        "notifications.loading": "ಅಧಿಸೂಚನೆಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...",
    },
    "ur": {
        "notifications.pageSubtitle": "اہم گائے کی صحت کے واقعات سے باخبر رہیں۔",
        "notifications.emptyTitle": "کوئی نئی اطلاع نہیں",
        "notifications.emptyHint": "گائے کی صحت اور AI اسکریننگ کے نتائج کی اطلاعات یہاں ظاہر ہوں گی۔",
        "notifications.viewResult": "نتیجہ دیکھیں",
        "notifications.summaryAll": "تمام",
        "notifications.summaryUnread": "نہ پڑھی",
        "notifications.summaryHighRisk": "اعلیٰ خطرہ",
        "notifications.summaryRecent": "حالیہ",
        "notifications.condition": "حالت",
        "notifications.screeningNote": "AI اسکریننگ نے قریبی نگرانی کی ضرورت والے اشارے پائے۔",
        "notifications.screeningNoteModerate": "AI اسکریننگ نے قریبی نگرانی کی ضرورت والے اشارے پائے۔",
        "notifications.screeningNoteHigh": "AI اسکریننگ نے ویٹرنری توجہ کی ضرورت والے اشارے پائے۔",
        "notifications.markRead": "پڑھا ہوا نشان زد کریں",
        "notifications.loading": "اطلاعات لوڈ ہو رہی ہیں...",
    },
    "ta": {
        "notifications.pageSubtitle": "முக்கியமான மாடு ஆரோக்கிய நிகழ்வுகளைப் பற்றி புதுப்பித்த நிலையில் இருங்கள்.",
        "notifications.emptyTitle": "புதிய அறிவிப்புகள் இல்லை",
        "notifications.emptyHint": "மாடு ஆரோக்கியம் மற்றும் AI திரையிடல் முடிவுகள் பற்றிய அறிவிப்புகள் இங்கே தோன்றும்.",
        "notifications.viewResult": "முடிவைக் காண்க",
        "notifications.summaryAll": "அனைத்தும்",
        "notifications.summaryUnread": "படிக்காதது",
        "notifications.summaryHighRisk": "அதிக ஆபத்து",
        "notifications.summaryRecent": "சமீபத்திய",
        "notifications.condition": "நிலை",
        "notifications.screeningNote": "AI திரையிடல் நெருக்கமான கண்காணிப்பு தேவைப்படும் கண்டறிதல்களைக் கண்டது.",
        "notifications.screeningNoteModerate": "AI திரையிடல் நெருக்கமான கண்காணிப்பு தேவைப்படும் கண்டறிதல்களைக் கண்டது.",
        "notifications.screeningNoteHigh": "AI திரையிடல் கால்நடை மருத்துவ கவனம் தேவைப்படும் கண்டறிதல்களைக் கண்டது.",
        "notifications.markRead": "படித்ததாகக் குறி",
        "notifications.loading": "அறிவிப்புகள் ஏற்றப்படுகின்றன...",
    },
    "te": {
        "notifications.pageSubtitle": "ముఖ్యమైన ఆవు ఆరోగ్య సంఘటనల గురించి తాజాగా ఉండండి.",
        "notifications.emptyTitle": "కొత్త నోటిఫికేషన్‌లు లేవు",
        "notifications.emptyHint": "ఆవు ఆరోగ్యం మరియు AI స్క్రీనింగ్ ఫలితాల నోటిఫికేషన్‌లు ఇక్కడ కనిపిస్తాయి.",
        "notifications.viewResult": "ఫలితం చూడండి",
        "notifications.summaryAll": "అన్నీ",
        "notifications.summaryUnread": "చదవనిది",
        "notifications.summaryHighRisk": "అధిక ప్రమాదం",
        "notifications.summaryRecent": "ఇటీవలి",
        "notifications.condition": "పరిస్థితి",
        "notifications.screeningNote": "AI స్క్రీనింగ్ సన్నిహిత పర్యవేక్షణ అవసరమైన కనుగొన్నదాన్ని గుర్తించింది.",
        "notifications.screeningNoteModerate": "AI స్క్రీనింగ్ సన్నిహిత పర్యవేక్షణ అవసరమైన కనుగొన్నదాన్ని గుర్తించింది.",
        "notifications.screeningNoteHigh": "AI స్క్రీనింగ్ పశువైద్య శ్రద్ధ అవసరమైన కనుగొన్నదాన్ని గుర్తించింది.",
        "notifications.markRead": "చదివినట్లు గుర్తించండి",
        "notifications.loading": "నోటిఫికేషన్‌లు లోడ్ అవుతున్నాయి...",
    },
    "gu": {
        "notifications.pageSubtitle": "મહત્વપૂર્ણ ગાય સ્વાસ્થ્ય ઘટનાઓ વિશે અપડેટ રહો.",
        "notifications.emptyTitle": "કોઈ નવી સૂચના નથી",
        "notifications.emptyHint": "ગાય સ્વાસ્થ્ય અને AI સ્ક્રીનિંગ પરિણામોની સૂચનાઓ અહીં દેખાશે.",
        "notifications.viewResult": "પરિણામ જુઓ",
        "notifications.summaryAll": "બધા",
        "notifications.summaryUnread": "ન વાંચેલ",
        "notifications.summaryHighRisk": "ઉચ્ચ જોખમ",
        "notifications.summaryRecent": "તાજેતરનું",
        "notifications.condition": "સ્થિતિ",
        "notifications.screeningNote": "AI સ્ક્રીનિંગે નજીકની નિરીક્ષણ જરૂરી શોધ કરી.",
        "notifications.screeningNoteModerate": "AI સ્ક્રીનિંગે નજીકની નિરીક્ષણ જરૂરી શોધ કરી.",
        "notifications.screeningNoteHigh": "AI સ્ક્રીનિંગે પશુચિકિત્સક ધ્યાન જરૂરી શોધ કરી.",
        "notifications.markRead": "વાંચેલ તરીકે ચિહ્નિત કરો",
        "notifications.loading": "સૂચનાઓ લોડ થઈ રહી છે...",
    },
    "pa": {
        "notifications.pageSubtitle": "ਮਹੱਤਵਪੂਰਨ ਗਾਂ ਦੀ ਸਿਹਤ ਦੀਆਂ ਘਟਨਾਵਾਂ ਬਾਰੇ ਅਪਡੇਟ ਰਹੋ।",
        "notifications.emptyTitle": "ਕੋਈ ਨਵੀਂ ਸੂਚਨਾ ਨਹੀਂ",
        "notifications.emptyHint": "ਗਾਂ ਦੀ ਸਿਹਤ ਅਤੇ AI ਸਕ੍ਰੀਨਿੰਗ ਨਤੀਜਿਆਂ ਦੀਆਂ ਸੂਚਨਾਵਾਂ ਇੱਥੇ ਦਿਖਾਈ ਦੇਣਗੀਆਂ।",
        "notifications.viewResult": "ਨਤੀਜਾ ਦੇਖੋ",
        "notifications.summaryAll": "ਸਾਰੇ",
        "notifications.summaryUnread": "ਨਾ ਪੜ੍ਹੀ",
        "notifications.summaryHighRisk": "ਉੱਚ ਜੋਖਮ",
        "notifications.summaryRecent": "ਹਾਲੀਆ",
        "notifications.condition": "ਹਾਲਤ",
        "notifications.screeningNote": "AI ਸਕ੍ਰੀਨਿੰਗ ਨੇ ਨੇੜਲੀ ਨਿਗਰਾਨੀ ਵਾਲੇ ਨਤੀਜੇ ਖੋਜੇ।",
        "notifications.screeningNoteModerate": "AI ਸਕ੍ਰੀਨਿੰਗ ਨੇ ਨੇੜਲੀ ਨਿਗਰਾਨੀ ਵਾਲੇ ਨਤੀਜੇ ਖੋਜੇ।",
        "notifications.screeningNoteHigh": "AI ਸਕ੍ਰੀਨਿੰਗ ਨੇ ਪਸ਼ੂ ਚਿਕਿਤਸਕ ਧਿਆਨ ਵਾਲੇ ਨਤੀਜੇ ਖੋਜੇ।",
        "notifications.markRead": "ਪੜ੍ਹਿਆ ਚਿੰਨ੍ਹਿਤ ਕਰੋ",
        "notifications.loading": "ਸੂਚਨਾਵਾਂ ਲੋਡ ਹੋ ਰਹੀਆਂ ਹਨ...",
    },
    "ml": {
        "notifications.pageSubtitle": "പ്രധാന പശു ആരോഗ്യ സംഭവങ്ങളെക്കുറിച്ച് അപ്ഡേറ്റ് ആയിരിക്കുക.",
        "notifications.emptyTitle": "പുതിയ അറിയിപ്പുകളില്ല",
        "notifications.emptyHint": "പശു ആരോഗ്യവും AI സ്ക്രീനിംഗ് ഫലങ്ങളുമായുള്ള അറിയിപ്പുകൾ ഇവിടെ കാണാം.",
        "notifications.viewResult": "ഫലം കാണുക",
        "notifications.summaryAll": "എല്ലാം",
        "notifications.summaryUnread": "വായിക്കാത്തത്",
        "notifications.summaryHighRisk": "ഉയർന്ന അപകടം",
        "notifications.summaryRecent": "സമീപകാല",
        "notifications.condition": "അവസ്ഥ",
        "notifications.screeningNote": "AI സ്ക്രീനിംഗ് അടുത്ത നിരീക്ഷണം ആവശ്യമായ കണ്ടെത്തലുകൾ കണ്ടെത്തി.",
        "notifications.screeningNoteModerate": "AI സ്ക്രീനിംഗ് അടുത്ത നിരീക്ഷണം ആവശ്യമായ കണ്ടെത്തലുകൾ കണ്ടെത്തി.",
        "notifications.screeningNoteHigh": "AI സ്ക്രീനിംഗ് പശുവൈദ്യ ശ്രദ്ധ ആവശ്യമായ കണ്ടെത്തലുകൾ കണ്ടെത്തി.",
        "notifications.markRead": "വായിച്ചതായി അടയാളപ്പെടുത്തുക",
        "notifications.loading": "അറിയിപ്പുകൾ ലോഡ് ചെയ്യുന്നു...",
    },
    "or": {
        "notifications.pageSubtitle": "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଗାଈ ସ୍ୱାସ୍ଥ୍ୟ ଘଟଣା ବିଷୟରେ ଅପଡେଟ୍ ରୁହନ୍ତୁ।",
        "notifications.emptyTitle": "କୌଣସି ନୂଆ ବିଜ୍ଞପ୍ତି ନାହିଁ",
        "notifications.emptyHint": "ଗାଈ ସ୍ୱାସ୍ଥ୍ୟ ଏବଂ AI ସ୍କ୍ରିନିଂ ଫଳାଫଳର ବିଜ୍ଞପ୍ତି ଏଠାରେ ଦେଖାଯିବ।",
        "notifications.viewResult": "ଫଳାଫଳ ଦେଖନ୍ତୁ",
        "notifications.summaryAll": "ସମସ୍ତ",
        "notifications.summaryUnread": "ନ ପଢ଼ା",
        "notifications.summaryHighRisk": "ଉଚ୍ଚ ବିପଦ",
        "notifications.summaryRecent": "ସାମ୍ପ୍ରତିକ",
        "notifications.condition": "ଅବସ୍ଥା",
        "notifications.screeningNote": "AI ସ୍କ୍ରିନିଂ ନିକଟ ନିରୀକ୍ଷଣ ଆବଶ୍ୟକ ଚିହ୍ନ ଚିହ୍ନଟ କରିଛି।",
        "notifications.screeningNoteModerate": "AI ସ୍କ୍ରିନିଂ ନିକଟ ନିରୀକ୍ଷଣ ଆବଶ୍ୟକ ଚିହ୍ନ ଚିହ୍ନଟ କରିଛି।",
        "notifications.screeningNoteHigh": "AI ସ୍କ୍ରିନିଂ ପଶୁଚିକିତ୍ସା ଧ୍ୟାନ ଆବଶ୍ୟକ ଚିହ୍ନ ଚିହ୍ନଟ କରିଛି।",
        "notifications.markRead": "ପଢ଼ା ଚିହ୍ନିତ କରନ୍ତୁ",
        "notifications.loading": "ବିଜ୍ଞପ୍ତି ଲୋଡ୍ ହେଉଛି...",
    },
    "as": {
        "notifications.pageSubtitle": "গুৰুত্বপূৰ্ণ গাইৰ স্বাস্থ্য ঘটনাৰ বিষয়ে আপডেট থাকক।",
        "notifications.emptyTitle": "নতুন জাননী নাই",
        "notifications.emptyHint": "গাইৰ স্বাস্থ্য আৰু AI স্ক্ৰীনিং ফলাফলৰ জাননী ইয়াত দেখা যাব।",
        "notifications.viewResult": "ফলাফল চাওক",
        "notifications.summaryAll": "সকলো",
        "notifications.summaryUnread": "নপঢ়া",
        "notifications.summaryHighRisk": "উচ্চ বিপদাশংকা",
        "notifications.summaryRecent": "শেহতীয়া",
        "notifications.condition": "অৱস্থা",
        "notifications.screeningNote": "AI স্ক্ৰীনিংয়ে নিকট পৰ্যবেক্ষণৰ প্ৰয়োজনীয় চিহ্ন চিনাক্ত কৰিছে।",
        "notifications.screeningNoteModerate": "AI স্ক্ৰীনিংয়ে নিকট পৰ্যবেক্ষণৰ প্ৰয়োজনীয় চিহ্ন চিনাক্ত কৰিছে।",
        "notifications.screeningNoteHigh": "AI স্ক্ৰীনিংয়ে পশুচিকিৎসক মনোযোগৰ প্ৰয়োজনীয় চিহ্ন চিনাক্ত কৰিছে।",
        "notifications.markRead": "পঢ়া চিহ্নিত কৰক",
        "notifications.loading": "জাননী ল'ড হৈ আছে...",
    },
    "ne": {
        "notifications.pageSubtitle": "महत्त्वपूर्ण गाई स्वास्थ्य घटनाहरूबारे अद्यावधिक रहनुहोस्।",
        "notifications.emptyTitle": "कुनै नयाँ सूचना छैन",
        "notifications.emptyHint": "गाई स्वास्थ्य र AI स्क्रिनिङ परिणामका सूचनाहरू यहाँ देखिनेछन्।",
        "notifications.viewResult": "परिणाम हेर्नुहोस्",
        "notifications.summaryAll": "सबै",
        "notifications.summaryUnread": "नपढिएको",
        "notifications.summaryHighRisk": "उच्च जोखिम",
        "notifications.summaryRecent": "हालैको",
        "notifications.condition": "अवस्था",
        "notifications.screeningNote": "AI स्क्रिनिङले नजिकको अनुगमन आवश्यक निष्कर्ष पत्ता लगायो।",
        "notifications.screeningNoteModerate": "AI स्क्रिनिङले नजिकको अनुगमन आवश्यक निष्कर्ष पत्ता लगायो।",
        "notifications.screeningNoteHigh": "AI स्क्रिनिङले पशु चिकित्सक ध्यान आवश्यक निष्कर्ष पत्ता लगायो।",
        "notifications.markRead": "पढिएको चिन्ह लगाउनुहोस्",
        "notifications.loading": "सूचनाहरू लोड हुँदैछ...",
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
        "notifications.pageSubtitle",
        "notifications.emptyTitle",
        "notifications.emptyHint",
        "notifications.viewResult",
        "notifications.summaryAll",
        "notifications.summaryUnread",
        "notifications.summaryHighRisk",
        "notifications.summaryRecent",
        "notifications.condition",
        "notifications.screeningNote",
        "notifications.screeningNoteModerate",
        "notifications.screeningNoteHigh",
        "notifications.markRead",
        "notifications.loading",
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
