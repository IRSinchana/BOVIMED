# -*- coding: utf-8 -*-
"""Rebuild dashboard.* keys in every locale from that locale's own strings (never Hindi copy-paste)."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"

# Dashboard-only phrases (nav/cows keys are composed automatically).
DASHBOARD_EXTRA = {
    "en": {
        "welcome": "Welcome to BOVIMED",
        "monitoring": "Monitoring",
        "atRisk": "Needs Attention",
        "analysesMonth": "Scans This Month",
        "riskDistribution": "Risk Distribution",
        "analysisTrend": "Scan Trend (6 months)",
        "unreadAlerts": "unread alerts",
        "recent": "Recent AI Scans",
        "recentAlerts": "Recent Alerts",
        "date": "Date",
        "result": "Finding",
        "confidence": "AI Confidence",
        "empty": "No scans yet. Upload or capture an image to start.",
        "viewAlert": "View Alert",
        "findVet": "Find Veterinarian",
    },
    "hi": {
        "welcome": "BOVIMED में आपका स्वागत है",
        "monitoring": "निगरानी",
        "atRisk": "ध्यान देने योग्य",
        "analysesMonth": "इस महीने की जांच",
        "riskDistribution": "जोखिम वितरण",
        "analysisTrend": "स्कैन प्रवृत्ति (6 महीने)",
        "unreadAlerts": "अपठित अलर्ट",
        "recent": "हालिया AI स्कैन",
        "recentAlerts": "हालिया अलर्ट्स",
        "date": "दिनांक",
        "result": "जांच परिणाम",
        "confidence": "AI विश्वास स्तर",
        "empty": "अभी तक कोई स्कैन नहीं। फोटो अपलोड या कैप्चर करें।",
        "viewAlert": "अलर्ट देखें",
        "findVet": "डॉक्टर खोजें",
    },
    "kn": {
        "welcome": "BOVIMED ಗೆ ಸ್ವಾಗತ",
        "monitoring": "ಮೇಲ್ವಿಚಾರಣೆ",
        "atRisk": "ಗಮನ ಬೇಕು",
        "analysesMonth": "ಈ ತಿಂಗಳ ಸ್ಕ್ಯಾನ್‌ಗಳು",
        "riskDistribution": "ಅಪಾಯ ವಿತರಣೆ",
        "analysisTrend": "ಸ್ಕ್ಯಾನ್ ಪ್ರವೃತ್ತಿ (6 ತಿಂಗಳು)",
        "unreadAlerts": "ಓದದ ಅಧಿಸೂಚನೆಗಳು",
        "recent": "ಇತ್ತೀಚಿನ AI ಸ್ಕ್ಯಾನ್‌ಗಳು",
        "recentAlerts": "ಇತ್ತೀಚಿನ ಎಚ್ಚರಿಕೆಗಳು",
        "date": "ದಿನಾಂಕ",
        "result": "ಫಲಿತಾಂಶ",
        "confidence": "AI ವಿಶ್ವಾಸ",
        "empty": "ಇನ್ನೂ ಯಾವುದೇ ಸ್ಕ್ಯಾನ್ ಇಲ್ಲ. ಪ್ರಾರಂಭಿಸಲು ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಸೆರೆಹಿಡಿಯಿರಿ.",
        "viewAlert": "ಎಚ್ಚರಿಕೆ ವೀಕ್ಷಿಸಿ",
        "findVet": "ಪಶುವೈದ್ಯರನ್ನು ಹುಡುಕಿ",
    },
    "te": {
        "welcome": "BOVIMED కు స్వాగతం",
        "monitoring": "పర్యవేక్షణ",
        "atRisk": "శ్రద్ధ అవసరం",
        "analysesMonth": "ఈ నెల స్కాన్‌లు",
        "riskDistribution": "ప్రమాదం వితరణ",
        "analysisTrend": "స్కాన్ ధోరణి (6 నెలలు)",
        "unreadAlerts": "చదవని నోటిఫికేషన్‌లు",
        "recent": "ఇటీవలి AI స్కాన్‌లు",
        "recentAlerts": "ఇటీవలి హెచ్చరికలు",
        "date": "తేదీ",
        "result": "ఫలితం",
        "confidence": "AI నమ్మకం",
        "empty": "ఇంకా స్కాన్‌లు లేవు. ప్రారంభించడానికి చిత్రాన్ని అప్‌లోడ్ చేయండి లేదా క్యాప్చర్ చేయండి.",
        "viewAlert": "హెచ్చరిక చూడండి",
        "findVet": "పశువైద్యుడిని కనుగొనండి",
    },
    "ta": {
        "welcome": "BOVIMED வரவேற்கிறது",
        "monitoring": "கண்காணிப்பு",
        "atRisk": "கவனம் தேவை",
        "analysesMonth": "இந்த மாத ஸ்கேன்கள்",
        "riskDistribution": "அபாய விநியோகம்",
        "analysisTrend": "ஸ்கேன் போக்கு (6 மாதங்கள்)",
        "unreadAlerts": "படிக்காத அறிவிப்புகள்",
        "recent": "சமீபத்திய AI ஸ்கேன்கள்",
        "recentAlerts": "சமீபத்திய எச்சரிக்கைகள்",
        "date": "தேதி",
        "result": "கண்டறிதல்",
        "confidence": "AI நம்பிக்கை",
        "empty": "இன்னும் ஸ்கேன்கள் இல்லை. தொடங்குவதற்கு படத்தை பதிவேற்றவும் அல்லது பிடிக்கவும்.",
        "viewAlert": "எச்சரிக்கையைக் காண்க",
        "findVet": "கால்நடை மருத்துவரைக் கண்டறியுங்கள்",
    },
    "ml": {
        "welcome": "BOVIMED-ലേക്ക് സ്വാഗതം",
        "monitoring": "നിരീക്ഷണം",
        "atRisk": "ശ്രദ്ധ ആവശ്യം",
        "analysesMonth": "ഈ മാസത്തെ സ്കാൻകൾ",
        "riskDistribution": "അപകട വിതരണം",
        "analysisTrend": "സ്കാൻ പ്രവണത (6 മാസം)",
        "unreadAlerts": "വായിക്കാത്ത അറിയിപ്പുകൾ",
        "recent": "സമീപകാല AI സ്കാൻകൾ",
        "recentAlerts": "സമീപകാല അലേർട്ടുകൾ",
        "date": "തീയതി",
        "result": "ഫലം",
        "confidence": "AI ആത്മവിശ്വാസം",
        "empty": "ഇതുവരെ സ്കാൻകളില്ല. ആരംഭിക്കാൻ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക അല്ലെങ്കിൽ ക്യാപ്ചർ ചെയ്യുക.",
        "viewAlert": "അലേർട്ട് കാണുക",
        "findVet": "മൃഗവൈദ്യനെ കണ്ടെത്തുക",
    },
    "bn": {
        "welcome": "BOVIMED-এ স্বাগত",
        "monitoring": "পর্যবেক্ষণ",
        "atRisk": "মনোযোগ প্রয়োজন",
        "analysesMonth": "এই মাসের স্ক্যান",
        "riskDistribution": "ঝুঁকি বিতরণ",
        "analysisTrend": "স্ক্যান প্রবণতা (৬ মাস)",
        "unreadAlerts": "অপঠিত সতর্কতা",
        "recent": "সাম্প্রতিক AI স্ক্যান",
        "recentAlerts": "সাম্প্রতিক সতর্কতা",
        "date": "তারিখ",
        "result": "ফলাফল",
        "confidence": "AI আস্থা",
        "empty": "এখনও কোনো স্ক্যান নেই। শুরু করতে ছবি আপলোড বা ক্যাপচার করুন।",
        "viewAlert": "সতর্কতা দেখুন",
        "findVet": "পশুচিকিৎসক খুঁজুন",
    },
    "mr": {
        "welcome": "BOVIMED मध्ये स्वागत आहे",
        "monitoring": "निरीक्षण",
        "atRisk": "लक्ष देणे आवश्यक",
        "analysesMonth": "या महिन्यातील स्कॅन",
        "riskDistribution": "जोखीम वितरण",
        "analysisTrend": "स्कॅन प्रवृत्ती (6 महीने)",
        "unreadAlerts": "वाचले नसलेले अलर्ट",
        "recent": "अलीकडील AI स्कॅन",
        "recentAlerts": "अलीकडील अलर्ट",
        "date": "तारीख",
        "result": "निकाल",
        "confidence": "AI विश्वास",
        "empty": "अद्याप कोणतेही स्कॅन नाहीत. सुरू करण्यासाठी चित्र अपलोड किंवा कॅप्चर करा.",
        "viewAlert": "अलर्ट पहा",
        "findVet": "पशुवैद्य शोधा",
    },
    "gu": {
        "welcome": "BOVIMED માં સ્વાગત છે",
        "monitoring": "નિરીક્ષણ",
        "atRisk": "ધ્યાન જરૂરી",
        "analysesMonth": "આ મહિનાના સ્કેન",
        "riskDistribution": "જોખમ વિતરણ",
        "analysisTrend": "સ્કેન પ્રવૃત્તિ (6 મહિના)",
        "unreadAlerts": "ન વાંચેલા અલર્ટ",
        "recent": "તાજેતરના AI સ્કેન",
        "recentAlerts": "તાજેતરના અલર્ટ",
        "date": "તારીખ",
        "result": "પરિણામ",
        "confidence": "AI વિશ્વાસ",
        "empty": "હજી સુધી કોઈ સ્કેન નથી. શરૂ કરવા માટે ચિત્ર અપલોડ કરો અથવા કેપ્ચર કરો.",
        "viewAlert": "અલર્ટ જુઓ",
        "findVet": "પશુચિકિત્સક શોધો",
    },
    "pa": {
        "welcome": "BOVIMED ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ",
        "monitoring": "ਨਿਗਰਾਨੀ",
        "atRisk": "ਧਿਆਨ ਚਾਹੀਦਾ",
        "analysesMonth": "ਇਸ ਮਹੀਨੇ ਦੇ ਸਕੈਨ",
        "riskDistribution": "ਜੋਖਮ ਵੰਡ",
        "analysisTrend": "ਸਕੈਨ ਰੁਝਾਨ (6 ਮਹੀਨੇ)",
        "unreadAlerts": "ਨਾ ਪੜ੍ਹੀਆਂ ਚੇਤਾਵਨੀਆਂ",
        "recent": "ਹਾਲੀਆ AI ਸਕੈਨ",
        "recentAlerts": "ਹਾਲੀਆ ਚੇਤਾਵਨੀਆਂ",
        "date": "ਤਾਰੀਖ",
        "result": "ਨਤੀਜਾ",
        "confidence": "AI ਭਰੋਸਾ",
        "empty": "ਅਜੇ ਕੋਈ ਸਕੈਨ ਨਹੀਂ। ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ ਜਾਂ ਕੈਪਚਰ ਕਰੋ।",
        "viewAlert": "ਚੇਤਾਵਨੀ ਦੇਖੋ",
        "findVet": "ਪਸ਼ੂ ਡਾਕਟਰ ਲੱਭੋ",
    },
    "or": {
        "welcome": "BOVIMED କୁ ସ୍ୱାଗତ",
        "monitoring": "ନିରୀକ୍ଷଣ",
        "atRisk": "ଧ୍ୟାନ ଆବଶ୍ୟକ",
        "analysesMonth": "ଏହି ମାସର ସ୍କାନ",
        "riskDistribution": "ଝୁଁକି ବିତରଣ",
        "analysisTrend": "ସ୍କାନ ପ୍ରବୃତ୍ତି (୬ ମାସ)",
        "unreadAlerts": "ନ ପଢ଼ା ସତର୍କତା",
        "recent": "ସାମ୍ପ୍ରତିକ AI ସ୍କାନ",
        "recentAlerts": "ସାମ୍ପ୍ରତିକ ସତର୍କତା",
        "date": "ତାରିଖ",
        "result": "ଫଳାଫଳ",
        "confidence": "AI ବିଶ୍ୱାସ",
        "empty": "ଏପର୍ଯ୍ୟନ୍ତ କୌଣସି ସ୍କାନ ନାହିଁ। ଆରମ୍ଭ କରିବାକୁ ଛବି ଅପଲୋଡ୍ କରନ୍ତୁ କିମ୍ବା କ୍ୟାପଚର୍ କରନ୍ତୁ।",
        "viewAlert": "ସତର୍କତା ଦେଖନ୍ତୁ",
        "findVet": "ପଶୁଚିକିତ୍ସକ ଖୋଜନ୍ତୁ",
    },
    "as": {
        "welcome": "BOVIMED-লৈ স্বাগতম",
        "monitoring": "পৰ্যবেক্ষণ",
        "atRisk": "মনোযোগ প্ৰয়োজন",
        "analysesMonth": "এই মাহৰ স্কেন",
        "riskDistribution": "বিপদ বিতৰণ",
        "analysisTrend": "স্কেন প্ৰৱণতি (৬ মাহ)",
        "unreadAlerts": "পঢ়া নোহোৱা সতৰ্কতা",
        "recent": "শেহতীয়া AI স্কেন",
        "recentAlerts": "শেহতীয়া সতৰ্কতা",
        "date": "তাৰিখ",
        "result": "ফলাফল",
        "confidence": "AI আস্থা",
        "empty": "এতিয়ালৈকে কোনো স্কেন নাই। আৰম্ভ কৰিবলৈ ছবি আপলোড বা কেপচাৰ কৰক।",
        "viewAlert": "সতৰ্কতা চাওক",
        "findVet": "পশুচিকিৎসক বিচাৰক",
    },
    "ur": {
        "welcome": "BOVIMED میں خوش آمدید",
        "monitoring": "نگرانی",
        "atRisk": "توجہ درکار",
        "analysesMonth": "اس مہینے کے اسکین",
        "riskDistribution": "خطرے کی تقسیم",
        "analysisTrend": "اسکین رجحان (6 ماہ)",
        "unreadAlerts": "غیر پڑھی انتباہات",
        "recent": "حالیہ AI اسکین",
        "recentAlerts": "حالیہ انتباہات",
        "date": "تاریخ",
        "result": "نتیجہ",
        "confidence": "AI اعتماد",
        "empty": "ابھی کوئی اسکین نہیں۔ شروع کرنے کے لیے تصویر اپ لوڈ یا کیپچر کریں۔",
        "viewAlert": "انتباہ دیکھیں",
        "findVet": "ویٹرنری ڈاکٹر تلاش کریں",
    },
    "ne": {
        "welcome": "BOVIMED मा स्वागत छ",
        "monitoring": "निगरानी",
        "atRisk": "ध्यान आवश्यक",
        "analysesMonth": "यस महिनाका स्क्यान",
        "riskDistribution": "जोखिम वितरण",
        "analysisTrend": "स्क्यान प्रवृत्ति (६ महिना)",
        "unreadAlerts": "नपढिएका अलर्ट",
        "recent": "हालैका AI स्क्यान",
        "recentAlerts": "हालैका अलर्ट",
        "date": "मिति",
        "result": "परिणाम",
        "confidence": "AI विश्वास",
        "empty": "अहिलेसम्म कुनै स्क्यान छैन। सुरु गर्न तस्बिर अपलोड वा क्याप्चर गर्नुहोस्।",
        "viewAlert": "अलर्ट हेर्नुहोस्",
        "findVet": "पशु चिकित्सक खोज्नुहोस्",
    },
    "kok": {
        "welcome": "BOVIMED मां येवकार",
        "monitoring": "निरीक्षण",
        "atRisk": "लक्ष देणे गरजेचें",
        "analysesMonth": "ह्या म्हयन्याचे स्कॅन",
        "riskDistribution": "धोको वितरण",
        "analysisTrend": "स्कॅन प्रवृत्ती (६ म्हयने)",
        "unreadAlerts": "वाचूंक नाशिल्ले अलर्ट",
        "recent": "हालींचे AI स्कॅन",
        "recentAlerts": "हालींचे अलर्ट",
        "date": "तारीख",
        "result": "निकाल",
        "confidence": "AI विश्वास",
        "empty": "अजून स्कॅन नात. सुरवात करपाक चित्र अपलोड वा कॅप्चर करात.",
        "viewAlert": "अलर्ट पळयात",
        "findVet": "पशुवैद्य सोदात",
    },
    "sa": {
        "welcome": "BOVIMED इत्यस्मिन् स्वागतम्",
        "monitoring": "निरीक्षणम्",
        "atRisk": "ध्यानं आवश्यकम्",
        "analysesMonth": "अस्मिन् मासे स्कैन्",
        "riskDistribution": "जोखिमवितरणम्",
        "analysisTrend": "स्कैन् प्रवृत्तिः (६ मासाः)",
        "unreadAlerts": "अपठितसूचनाः",
        "recent": "सद्यः AI स्कैन्",
        "recentAlerts": "सद्यः सूचनाः",
        "date": "दिनाङ्कः",
        "result": "परिणामः",
        "confidence": "AI विश्वासः",
        "empty": "अद्यापि स्कैन् नास्ति। आरम्भाय चित्रं अपलोड् कुरुत।",
        "viewAlert": "सूचनां पश्यतु",
        "findVet": "पशुचिकित्सकं अन्विष्यतु",
    },
    "brx": {
        "welcome": "BOVIMED आव थाखाय सागोरनाय",
        "monitoring": "निरीक्षण",
        "atRisk": "ध्यान दं",
        "analysesMonth": "बे दान स्कैन",
        "riskDistribution": "जोखिम बिख्राव",
        "analysisTrend": "स्कैन प्रवृत्ति (६ दान)",
        "unreadAlerts": "फरायनाय अलर्ट",
        "recent": "दासिम स्कैन",
        "recentAlerts": "दासिम अलर्ट",
        "date": "तारीख",
        "result": "फलाफल",
        "confidence": "AI बिसोर",
        "empty": "दासिमै स्कैन नङा। आरोबावनो थाखाय सावगारि अपलोड एबा कैप्चार खालाम।",
        "viewAlert": "अलर्ट नुजा",
        "findVet": "डाक्टर नागिर",
    },
    "doi": {
        "welcome": "BOVIMED च स्वागत ऐ",
        "monitoring": "निगरानी",
        "atRisk": "ध्यान देने दी लोड़",
        "analysesMonth": "एह् महीने दे स्कैन",
        "riskDistribution": "जोखिम वितरण",
        "analysisTrend": "स्कैन प्रवृत्ति (६ महीने)",
        "unreadAlerts": "न पढ़े अलर्ट",
        "recent": "हालिया AI स्कैन",
        "recentAlerts": "हालिया अलर्ट",
        "date": "तारीख",
        "result": "नतीजा",
        "confidence": "AI भरोसा",
        "empty": "हाले तक कोई स्कैन नेईं। शुरू करन लेई फोटो अपलोड जां कैप्चर करो।",
        "viewAlert": "अलर्ट देखो",
        "findVet": "डाक्टर लब्भो",
    },
    "mai": {
        "welcome": "BOVIMED मे स्वागत अछि",
        "monitoring": "निरीक्षण",
        "atRisk": "ध्यान देबाक जरूरत",
        "analysesMonth": "एहि महीना स्कैन",
        "riskDistribution": "जोखिम वितरण",
        "analysisTrend": "स्कैन प्रवृत्ति (६ महीना)",
        "unreadAlerts": "न पढ़ल अलर्ट",
        "recent": "हालिया AI स्कैन",
        "recentAlerts": "हालिया अलर्ट",
        "date": "तिथि",
        "result": "परिणाम",
        "confidence": "AI विश्वास",
        "empty": "एखन धरि कोनो स्कैन नहि। शुरू करबाक लेल फोटो अपलोड वा कैप्चर करू।",
        "viewAlert": "अलर्ट देखू",
        "findVet": "डाक्टर खोजू",
    },
    "mni": {
        "welcome": "BOVIMED দা ওন্থোক্লে",
        "monitoring": "পর্যবেক্ষণ",
        "atRisk": "মনোযোগ দরকার",
        "analysesMonth": "মমিংগী স্ক্যানশিং",
        "riskDistribution": "ঝুঁকি বিতরণ",
        "analysisTrend": "স্ক্যান প্রবণতা (৬ মাস)",
        "unreadAlerts": "পড়া নত্রবা সতর্কতা",
        "recent": "হান্নবা AI স্ক্যান",
        "recentAlerts": "হান্নবা সতর্কতা",
        "date": "তারিখ",
        "result": "ফলাফল",
        "confidence": "AI আস্থা",
        "empty": "হজিক পর্যন্ত স্ক্যান নাই। আৰম্ভ কৰিবলৈ ছবি আপলোড বা কেপচাৰ কৰক।",
        "viewAlert": "সতর্কতা উৎ",
        "findVet": "পশুচিকিৎসক থিংবিয়ু",
    },
    "sd": {
        "welcome": "BOVIMED ۾ خوش آمديد",
        "monitoring": "نگراني",
        "atRisk": "توجھو گھربل",
        "analysesMonth": "هن مهيني جا اسڪين",
        "riskDistribution": "خطري جي ورهاست",
        "analysisTrend": "اسڪين رجحان (6 مهينا)",
        "unreadAlerts": "نه پڙهيل الرٽ",
        "recent": "تازيون AI اسڪين",
        "recentAlerts": "تازيون الرٽ",
        "date": "تاريخ",
        "result": "نتيجو",
        "confidence": "AI اعتماد",
        "empty": "اڃا تائين ڪوبه اسڪين ناهي. شروع ڪرڻ لاءِ تصوير اپلوڊ يا ڪيپچر ڪريو.",
        "viewAlert": "الرٽ ڏسو",
        "findVet": "ويٽرنري ڊاڪٽر ڳوليو",
    },
    "ks": {
        "welcome": "BOVIMED مَنٛز خوش آمدید",
        "monitoring": "نگرانی",
        "atRisk": "توجہ ضروری",
        "analysesMonth": "یِم مہینہِ کٕہ اسکین",
        "riskDistribution": "خطرٕچ تقسیم",
        "analysisTrend": "اسکین رجحان (6 مہینہ)",
        "unreadAlerts": "نَہ پَڑھِتھ اطلاع",
        "recent": "تازہ AI اسکین",
        "recentAlerts": "تازہ اطلاع",
        "date": "تاریخ",
        "result": "نتیجہ",
        "confidence": "AI اعتماد",
        "empty": "ابھی تام کُنہِ اسکین نِہ۔ شروع کرنہٕ خٲطرٕ تصویر اپلوڈ یا کیپچر کٔرِو۔",
        "viewAlert": "اطلاع وُچھِو",
        "findVet": "ویٹرنری ڈاکٹر تلاش کٔرِو",
    },
    "sat": {
        "welcome": "BOVIMED ᱨᱮ ᱥᱟᱹᱜᱚᱱ",
        "monitoring": "ᱧᱮᱞ",
        "atRisk": "ᱧᱮᱞ ᱞᱟᱹᱜᱤᱫ",
        "analysesMonth": "ᱱᱤᱛᱚᱜ ᱪᱟᱸᱫ ᱥᱠᱟᱱ",
        "riskDistribution": "ᱡᱚᱠᱷᱤᱢ ᱵᱤᱛᱨᱚᱱ",
        "analysisTrend": "ᱥᱠᱟᱱ ᱯᱨᱚᱵᱷᱟᱵ (᱖ ᱪᱟᱸᱫ)",
        "unreadAlerts": "ᱵᱟᱝ ᱯᱚᱲᱷᱟᱣ ᱟᱞᱟᱨᱴ",
        "recent": "ᱱᱮᱡᱟᱨ AI ᱥᱠᱟᱱ",
        "recentAlerts": "ᱱᱮᱡᱟᱨ ᱟᱞᱟᱨᱴ",
        "date": "ᱢᱟᱦᱟ",
        "result": "ᱯᱷᱞᱟᱫ",
        "confidence": "AI ᱵᱤᱥᱣᱟᱥ",
        "empty": "ᱱᱤᱛᱚᱜ ᱫᱚ ᱪᱮᱫ ᱥᱠᱟᱱ ᱵᱟᱹᱱᱤᱭᱟ। ᱮᱛᱚᱢ ᱞᱟᱹᱜᱤᱫ ᱪᱤᱛᱟᱹᱨ ᱟᱯᱞᱚᱰ ᱟᱨᱵᱟᱝ ᱠᱮᱯᱪᱟᱨ ᱢᱮ।",
        "viewAlert": "ᱟᱞᱟᱨᱴ ᱧᱮᱞ",
        "findVet": "ᱫᱟᱠᱛᱟᱨ ᱯᱟᱱᱛᱮ",
    },
}

# Locales without explicit extras inherit from closest reference.
REF = {
    "as": "bn",
    "or": "bn",
    "mni": "bn",
    "sat": "bn",
    "kok": "mr",
    "gu": "mr",
    "ne": "hi",
    "sa": "hi",
    "brx": "hi",
    "doi": "hi",
    "mai": "hi",
    "sd": "ur",
    "ks": "ur",
    "te": "te",
    "ta": "ta",
    "ml": "ml",
    "pa": "pa",
}


def load(code: str) -> dict:
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def save(code: str, data: dict) -> None:
    (DIR / f"{code}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def strip_optional(text: str) -> str:
    if not text:
        return text
    if "(" in text:
        return text.split("(")[0].strip()
    return text


def extras_for(code: str) -> dict:
    merged = dict(DASHBOARD_EXTRA["en"])
    ref = REF.get(code, code)
    if ref in DASHBOARD_EXTRA:
        merged.update(DASHBOARD_EXTRA[ref])
    if code in DASHBOARD_EXTRA:
        merged.update(DASHBOARD_EXTRA[code])
    return merged


def compose_dashboard(locale: dict, code: str) -> dict:
    en = load("en")["dashboard"]
    extra = extras_for(code)
    nav = locale.get("nav", {})
    cows = locale.get("cows", {})
    risk = locale.get("risk", {})
    analyze = locale.get("analyze", {})
    result = locale.get("result", {})
    notifications = locale.get("notifications", {})
    vets = locale.get("vets", {})
    chat = locale.get("chat", {})
    chips = chat.get("chips", {}) if isinstance(chat.get("chips"), dict) else {}

    def first(*values):
        for value in values:
            if value:
                return value
        return None

    dashboard = {
        "welcome": first(extra.get("welcome"), f"BOVIMED — {locale.get('tagline')}" if locale.get("tagline") else None),
        "subtitle": first(locale.get("shortDesc"), en["subtitle"]),
        "analyzeCta": first(nav.get("analyze"), en["analyzeCta"]),
        "cameraCta": first(nav.get("camera"), en["cameraCta"]),
        "askCta": first(nav.get("chat"), en["askCta"]),
        "vetCta": first(nav.get("vets"), en["vetCta"]),
        "totalCows": first(cows.get("title"), nav.get("cows"), en["totalCows"]),
        "healthy": first(risk.get("Healthy"), en["healthy"]),
        "monitoring": first(extra.get("monitoring"), en["monitoring"]),
        "atRisk": first(extra.get("atRisk"), en["atRisk"]),
        "analysesMonth": first(extra.get("analysesMonth"), en["analysesMonth"]),
        "riskDistribution": first(extra.get("riskDistribution"), en["riskDistribution"]),
        "analysisTrend": first(extra.get("analysisTrend"), en["analysisTrend"]),
        "unreadAlerts": first(extra.get("unreadAlerts"), en["unreadAlerts"]),
        "recent": first(extra.get("recent"), en["recent"]),
        "recentAlerts": first(extra.get("recentAlerts"), nav.get("alerts"), en["recentAlerts"]),
        "cowId": first(strip_optional(analyze.get("cowId")), en["cowId"]),
        "date": first(extra.get("date"), en["date"]),
        "result": first(extra.get("result"), en["result"]),
        "confidence": first(extra.get("confidence"), en["confidence"]),
        "risk": first(notifications.get("risk"), en["risk"]),
        "empty": first(extra.get("empty"), en["empty"]),
        "viewAlert": first(extra.get("viewAlert"), notifications.get("viewAll"), en["viewAlert"]),
        "findVet": first(extra.get("findVet"), vets.get("title"), chips.get("findVet"), en["findVet"]),
    }

    for key, value in dashboard.items():
        if not value:
            dashboard[key] = en[key]

    return dashboard


def main() -> None:
    for path in sorted(DIR.glob("*.json")):
        code = path.stem
        locale = load(code)
        locale["dashboard"] = compose_dashboard(locale, code)
        save(code, locale)
        print(f"fixed dashboard for {code}")


if __name__ == "__main__":
    main()
