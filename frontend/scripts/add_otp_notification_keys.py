# -*- coding: utf-8 -*-
"""Propagate OTP + notification i18n keys to all 22 locales."""
import json
from copy import deepcopy
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"

REF = {
    "as": "bn", "or": "bn", "mni": "bn", "sat": "bn",
    "ne": "hi", "kok": "mr", "sa": "hi", "brx": "hi", "doi": "hi", "mai": "hi",
    "sd": "ur", "ks": "ur", "gu": "mr", "te": "kn", "ta": "kn", "ml": "kn", "pa": "hi",
}

PATCHES = {
    "hi": {
        "auth.loginWithPassword": "पासवर्ड",
        "auth.loginWithOtp": "OTP",
        "auth.sendOtp": "OTP भेजें",
        "auth.sendingOtp": "OTP भेजा जा रहा है…",
        "auth.verifyOtp": "OTP सत्यापित करें",
        "auth.verifyingOtp": "सत्यापन हो रहा है…",
        "auth.otpCode": "6 अंकों का OTP",
        "auth.otpPrompt": "{{destination}} पर भेजा गया 6 अंकों का OTP दर्ज करें",
        "auth.resendOtp": "OTP पुनः भेजें",
        "auth.resendAvailableIn": "{{seconds}} सेकंड में पुनः भेजें",
        "auth.backToLogin": "लॉगिन पर वापस",
        "auth.otpSent": "यदि खाता मौजूद है, तो सत्यापन कोड भेज दिया गया है।",
        "auth.otpVerified": "OTP सत्यापित। साइन इन हो रहा है…",
        "auth.otpInvalid": "अमान्य सत्यापन कोड।",
        "auth.otpExpired": "सत्यापन कोड समाप्त हो गया। नया कोड मांगें।",
        "auth.otpTooManyAttempts": "बहुत अधिक गलत प्रयास। नया कोड मांगें।",
        "auth.otpTooManyRequests": "बहुत अधिक OTP अनुरोध। बाद में पुनः प्रयास करें।",
        "auth.otpNetworkError": "नेटवर्क त्रुटि। पुनः प्रयास करें।",
        "auth.otpProviderMissing": "OTP डिलीवरी प्रदाता कॉन्फ़िगर नहीं है।",
        "auth.otpDevHint": "विकास मोड — कोड पहले से भरा",
        "notifications.title": "सूचनाएं",
        "notifications.empty": "अभी कोई सूचना नहीं।",
        "notifications.markRead": "पढ़ा हुआ चिह्नित करें",
        "notifications.markAllRead": "सभी को पढ़ा चिह्नित करें",
        "notifications.viewAnalysis": "विश्लेषण देखें",
        "notifications.moderateRisk.title": "मध्यम जोखिम पाया गया",
        "notifications.moderateRisk.message": "{{cowId}} में संभावित {{detection}} संकेत। जोखिम: {{risk}}। पहचान विश्वास: {{confidence}}%।",
        "notifications.highRisk.title": "उच्च जोखिम पाया गया",
        "notifications.highRisk.message": "{{cowId}} में संभावित {{detection}} संकेत। जोखिम: {{risk}}। पहचान विश्वास: {{confidence}}%।",
        "notifications.criticalRisk.title": "गंभीर जोखिम पाया गया",
        "notifications.criticalRisk.message": "{{cowId}} में संभावित {{detection}} संकेत। जोखिम: {{risk}}। पहचान विश्वास: {{confidence}}%। तुरंत पशु चिकित्सक से संपर्क करें।",
        "settings.notificationsSubtitle": "चुनें कि BOVIMED में कौन से अलर्ट प्राप्त करें।",
        "settings.notifHealthAlerts": "स्वास्थ्य अलर्ट (मध्यम और उससे ऊपर)",
        "settings.notifAnalysisCompleted": "विश्लेषण पूर्ण",
        "settings.notifVeterinary": "पशु चिकित्सा अनुस्मारक",
        "settings.notifSystem": "सिस्टम सूचनाएं",
        "settings.notifBrowser": "ब्राउज़र सूचनाएं",
        "settings.enableBrowserNotifications": "BOVIMED सूचनाएं सक्षम करें",
        "settings.browserNotifEnabled": "ब्राउज़र सूचनाएं सक्षम।",
        "settings.browserNotifDenied": "ब्राउज़र सूचनाएं अवरुद्ध हैं। इन-ऐप सूचनाएं काम करती हैं।",
        "settings.browserNotifUnsupported": "इस डिवाइस पर ब्राउज़र सूचनाएं समर्थित नहीं।",
        "settings.saveNotifications": "सूचना सेटिंग्स सहेजें",
        "settings.notifSaved": "सूचना सेटिंग्स सहेजी गईं।",
    },
    "bn": {
        "auth.loginWithPassword": "পাসওয়ার্ড",
        "auth.loginWithOtp": "OTP",
        "auth.sendOtp": "OTP পাঠান",
        "auth.sendingOtp": "OTP পাঠানো হচ্ছে…",
        "auth.verifyOtp": "OTP যাচাই করুন",
        "auth.verifyingOtp": "যাচাই হচ্ছে…",
        "auth.otpCode": "৬ অঙ্কের OTP",
        "auth.otpPrompt": "{{destination}}-এ পাঠানো ৬ অঙ্কের OTP লিখুন",
        "auth.resendOtp": "OTP পুনরায় পাঠান",
        "auth.resendAvailableIn": "{{seconds}} সেকেন্ডে পুনরায় পাঠানো যাবে",
        "auth.backToLogin": "লগইনে ফিরে যান",
        "auth.otpSent": "অ্যাকাউন্ট থাকলে যাচাইকরণ কোড পাঠানো হয়েছে।",
        "auth.otpVerified": "OTP যাচাই হয়েছে। সাইন ইন হচ্ছে…",
        "auth.otpInvalid": "অবৈধ যাচাইকরণ কোড।",
        "auth.otpExpired": "যাচাইকরণ কোড মেয়াদোত্তীর্ণ। নতুন কোড চান।",
        "auth.otpTooManyAttempts": "অনেক ভুল চেষ্টা। নতুন কোড চান।",
        "auth.otpTooManyRequests": "অতিরিক্ত OTP অনুরোধ। পরে আবার চেষ্টা করুন।",
        "auth.otpNetworkError": "নেটওয়ার্ক ত্রুটি। আবার চেষ্টা করুন।",
        "auth.otpProviderMissing": "OTP ডেলিভারি প্রদানকারী কনফিগার করা নেই।",
        "auth.otpDevHint": "ডেভেলপমেন্ট মোড — কোড পূরণ করা",
        "notifications.title": "বিজ্ঞপ্তি",
        "notifications.empty": "এখনও কোনো বিজ্ঞপ্তি নেই।",
        "notifications.markRead": "পঠিত চিহ্নিত করুন",
        "notifications.markAllRead": "সব পঠিত চিহ্নিত করুন",
        "notifications.viewAnalysis": "বিশ্লেষণ দেখুন",
        "notifications.moderateRisk.title": "মাঝারি ঝুঁকি সনাক্ত",
        "notifications.moderateRisk.message": "{{cowId}}-এ সম্ভাব্য {{detection}} সংকেত। ঝুঁকি: {{risk}}। সনাক্তকরণ আস্থা: {{confidence}}%।",
        "notifications.highRisk.title": "উচ্চ ঝুঁকি সনাক্ত",
        "notifications.highRisk.message": "{{cowId}}-এ সম্ভাব্য {{detection}} সংকেত। ঝুঁকি: {{risk}}। সনাক্তকরণ আস্থা: {{confidence}}%।",
        "notifications.criticalRisk.title": "গুরুতর ঝুঁকি সনাক্ত",
        "notifications.criticalRisk.message": "{{cowId}}-এ সম্ভাব্য {{detection}} সংকেত। ঝুঁকি: {{risk}}। সনাক্তকরণ আস্থা: {{confidence}}%। দ্রুত পশুচিকিৎসকের সাথে যোগাযোগ করুন।",
        "settings.notificationsSubtitle": "BOVIMED-এ কোন সতর্কতা পাবেন তা বেছে নিন।",
        "settings.notifHealthAlerts": "স্বাস্থ্য সতর্কতা (মাঝারি ও তার উপরে)",
        "settings.notifAnalysisCompleted": "বিশ্লেষণ সম্পন্ন",
        "settings.notifVeterinary": "পশুচিকিৎসা অনুস্মারক",
        "settings.notifSystem": "সিস্টেম বিজ্ঞপ্তি",
        "settings.notifBrowser": "ব্রাউজার বিজ্ঞপ্তি",
        "settings.enableBrowserNotifications": "BOVIMED বিজ্ঞপ্তি সক্ষম করুন",
        "settings.browserNotifEnabled": "ব্রাউজার বিজ্ঞপ্তি সক্ষম।",
        "settings.browserNotifDenied": "ব্রাউজার বিজ্ঞপ্তি ব্লক। ইন-অ্যাপ বিজ্ঞপ্তি কাজ করবে।",
        "settings.browserNotifUnsupported": "এই ডিভাইসে ব্রাউজার বিজ্ঞপ্তি সমর্থিত নয়।",
        "settings.saveNotifications": "বিজ্ঞপ্তি সেটিংস সংরক্ষণ",
        "settings.notifSaved": "বিজ্ঞপ্তি সেটিংস সংরক্ষিত।",
    },
    "mr": {
        "auth.loginWithPassword": "पासवर्ड",
        "auth.loginWithOtp": "OTP",
        "auth.sendOtp": "OTP पाठवा",
        "auth.sendingOtp": "OTP पाठवत आहे…",
        "auth.verifyOtp": "OTP सत्यापित करा",
        "auth.verifyingOtp": "सत्यापन होत आहे…",
        "auth.otpCode": "६ अंकी OTP",
        "auth.otpPrompt": "{{destination}} वर पाठवलेला ६ अंकी OTP प्रविष्ट करा",
        "auth.resendOtp": "OTP पुन्हा पाठवा",
        "auth.resendAvailableIn": "{{seconds}} सेकंदात पुन्हा पाठवा",
        "auth.backToLogin": "लॉगिनवर परत",
        "auth.otpSent": "खाते असल्यास सत्यापन कोड पाठवला आहे.",
        "auth.otpVerified": "OTP सत्यापित. साइन इन होत आहे…",
        "auth.otpInvalid": "अवैध सत्यापन कोड.",
        "auth.otpExpired": "सत्यापन कोड कालबाह्य. नवीन कोड मागा.",
        "auth.otpTooManyAttempts": "खूप चुकीचे प्रयत्न. नवीन कोड मागा.",
        "auth.otpTooManyRequests": "खूप OTP विनंत्या. नंतर पुन्हा प्रयत्न करा.",
        "auth.otpNetworkError": "नेटवर्क त्रुटी. पुन्हा प्रयत्न करा.",
        "auth.otpProviderMissing": "OTP वितरण प्रदाता कॉन्फिगर नाही.",
        "auth.otpDevHint": "विकास मोड — कोड भरलेला",
        "notifications.title": "सूचना",
        "notifications.empty": "अद्याप सूचना नाहीत.",
        "notifications.markRead": "वाचले म्हणून चिन्हांकित करा",
        "notifications.markAllRead": "सर्व वाचले म्हणून चिन्हांकित करा",
        "notifications.viewAnalysis": "विश्लेषण पहा",
        "notifications.moderateRisk.title": "मध्यम धोका आढळला",
        "notifications.moderateRisk.message": "{{cowId}} मध्ये संभाव्य {{detection}} संकेत. धोका: {{risk}}. ओळख विश्वास: {{confidence}}%.",
        "notifications.highRisk.title": "उच्च धोका आढळला",
        "notifications.highRisk.message": "{{cowId}} मध्ये संभाव्य {{detection}} संकेत. धोका: {{risk}}. ओळख विश्वास: {{confidence}}%.",
        "notifications.criticalRisk.title": "गंभीर धोका आढळला",
        "notifications.criticalRisk.message": "{{cowId}} मध्ये संभाव्य {{detection}} संकेत. धोका: {{risk}}. ओळख विश्वास: {{confidence}}%. त्वरित पशुवैद्यकाशी संपर्क साधा.",
        "settings.notificationsSubtitle": "BOVIMED मध्ये कोणते अलर्ट मिळवायचे ते निवडा.",
        "settings.notifHealthAlerts": "आरोग्य अलर्ट (मध्यम व त्यावर)",
        "settings.notifAnalysisCompleted": "विश्लेषण पूर्ण",
        "settings.notifVeterinary": "पशुवैद्यकीय स्मरणपत्रे",
        "settings.notifSystem": "सिस्टम सूचना",
        "settings.notifBrowser": "ब्राउझर सूचना",
        "settings.enableBrowserNotifications": "BOVIMED सूचना सक्षम करा",
        "settings.browserNotifEnabled": "ब्राउझर सूचना सक्षम.",
        "settings.browserNotifDenied": "ब्राउझर सूचना अवरोधित. इन-अॅप सूचना कार्यरत.",
        "settings.browserNotifUnsupported": "या डिव्हाइसवर ब्राउझर सूचना समर्थित नाहीत.",
        "settings.saveNotifications": "सूचना सेटिंग्ज जतन करा",
        "settings.notifSaved": "सूचना सेटिंग्ज जतन केल्या.",
    },
    "kn": {
        "auth.loginWithPassword": "ಪಾಸ್‌ವರ್ಡ್",
        "auth.loginWithOtp": "OTP",
        "auth.sendOtp": "OTP ಕಳುಹಿಸಿ",
        "auth.sendingOtp": "OTP ಕಳುಹಿಸಲಾಗುತ್ತಿದೆ…",
        "auth.verifyOtp": "OTP ಪರಿಶೀಲಿಸಿ",
        "auth.verifyingOtp": "ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ…",
        "auth.otpCode": "6 ಅಂಕಿಯ OTP",
        "auth.otpPrompt": "{{destination}} ಗೆ ಕಳುಹಿಸಿದ 6 ಅಂಕಿಯ OTP ನಮೂದಿಸಿ",
        "auth.resendOtp": "OTP ಮರುಕಳುಹಿಸಿ",
        "auth.resendAvailableIn": "{{seconds}} ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಮರುಕಳುಹಿಸಬಹುದು",
        "auth.backToLogin": "ಲಾಗಿನ್‌ಗೆ ಹಿಂತಿರುಗಿ",
        "auth.otpSent": "ಖಾತೆ ಇದ್ದರೆ ಪರಿಶೀಲನಾ ಕೋಡ್ ಕಳುಹಿಸಲಾಗಿದೆ.",
        "auth.otpVerified": "OTP ಪರಿಶೀಲಿಸಲಾಗಿದೆ. ಸೈನ್ ಇನ್ ಆಗುತ್ತಿದೆ…",
        "auth.otpInvalid": "ಅಮಾನ್ಯ ಪರಿಶೀಲನಾ ಕೋಡ್.",
        "auth.otpExpired": "ಪರಿಶೀಲನಾ ಕೋಡ್ ಅವಧಿ ಮುಗಿದಿದೆ. ಹೊಸ ಕೋಡ್ ಕೇಳಿ.",
        "auth.otpTooManyAttempts": "ಹಲವಾರು ತಪ್ಪು ಪ್ರಯತ್ನಗಳು. ಹೊಸ ಕೋಡ್ ಕೇಳಿ.",
        "auth.otpTooManyRequests": "ಹೆಚ್ಚು OTP ವಿನಂತಿಗಳು. ನಂತರ ಪ್ರಯತ್ನಿಸಿ.",
        "auth.otpNetworkError": "ನೆಟ್‌ವರ್ಕ್ ದೋಷ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "auth.otpProviderMissing": "OTP ವಿತರಣಾ ಪೂರೈಕೆದಾರ ಕಾನ್ಫಿಗರ್ ಮಾಡಿಲ್ಲ.",
        "auth.otpDevHint": "ಅಭಿವೃದ್ಧಿ ಮೋಡ್ — ಕೋಡ್ ತುಂಬಿದೆ",
        "notifications.title": "ಅಧಿಸೂಚನೆಗಳು",
        "notifications.empty": "ಇನ್ನೂ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ.",
        "notifications.markRead": "ಓದಿದೆ ಎಂದು ಗುರುತಿಸಿ",
        "notifications.markAllRead": "ಎಲ್ಲವನ್ನು ಓದಿದೆ ಎಂದು ಗುರುತಿಸಿ",
        "notifications.viewAnalysis": "ವಿಶ್ಲೇಷಣೆ ವೀಕ್ಷಿಸಿ",
        "notifications.moderateRisk.title": "ಮಧ್ಯಮ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
        "notifications.moderateRisk.message": "{{cowId}} ನಲ್ಲಿ ಸಂಭಾವ್ಯ {{detection}} ಸೂಚಕಗಳು. ಅಪಾಯ: {{risk}}. ಪತ್ತೆ ವಿಶ್ವಾಸ: {{confidence}}%.",
        "notifications.highRisk.title": "ಅಧಿಕ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
        "notifications.highRisk.message": "{{cowId}} ನಲ್ಲಿ ಸಂಭಾವ್ಯ {{detection}} ಸೂಚಕಗಳು. ಅಪಾಯ: {{risk}}. ಪತ್ತೆ ವಿಶ್ವಾಸ: {{confidence}}%.",
        "notifications.criticalRisk.title": "ಗಂಭೀರ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
        "notifications.criticalRisk.message": "{{cowId}} ನಲ್ಲಿ ಸಂಭಾವ್ಯ {{detection}} ಸೂಚಕಗಳು. ಅಪಾಯ: {{risk}}. ಪತ್ತೆ ವಿಶ್ವಾಸ: {{confidence}}%. ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "settings.notificationsSubtitle": "BOVIMED ನಲ್ಲಿ ಯಾವ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಸ್ವೀಕರಿಸಬೇಕು ಎಂಬುದನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "settings.notifHealthAlerts": "ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆಗಳು (ಮಧ್ಯಮ ಮತ್ತು ಮೇಲೆ)",
        "settings.notifAnalysisCompleted": "ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣಗೊಂಡಿದೆ",
        "settings.notifVeterinary": "ಪಶುವೈದ್ಯಕೀಯ ಜ್ಞಾಪನೆಗಳು",
        "settings.notifSystem": "ಸಿಸ್ಟಮ್ ಅಧಿಸೂಚನೆಗಳು",
        "settings.notifBrowser": "ಬ್ರೌಸರ್ ಅಧಿಸೂಚನೆಗಳು",
        "settings.enableBrowserNotifications": "BOVIMED ಅಧಿಸೂಚನೆಗಳನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ",
        "settings.browserNotifEnabled": "ಬ್ರೌಸರ್ ಅಧಿಸೂಚನೆಗಳು ಸಕ್ರಿಯ.",
        "settings.browserNotifDenied": "ಬ್ರೌಸರ್ ಅಧಿಸೂಚನೆಗಳು ನಿರ್ಬಂಧಿತ. ಇನ್-ಅಪ್ ಅಧಿಸೂಚನೆಗಳು ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತವೆ.",
        "settings.browserNotifUnsupported": "ಈ ಸಾಧನದಲ್ಲಿ ಬ್ರೌಸರ್ ಅಧಿಸೂಚನೆಗಳು ಬೆಂಬಲಿತವಲ್ಲ.",
        "settings.saveNotifications": "ಅಧಿಸೂಚನೆ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಉಳಿಸಿ",
        "settings.notifSaved": "ಅಧಿಸೂಚನೆ ಸೆಟ್ಟಿಂಗ್‌ಗಳು ಉಳಿಸಲಾಗಿದೆ.",
    },
    "ur": {
        "auth.loginWithPassword": "پاس ورڈ",
        "auth.loginWithOtp": "OTP",
        "auth.sendOtp": "OTP بھیجیں",
        "auth.sendingOtp": "OTP بھیجا جا رہا ہے…",
        "auth.verifyOtp": "OTP تصدیق کریں",
        "auth.verifyingOtp": "تصدیق ہو رہی ہے…",
        "auth.otpCode": "6 ہندسوں کا OTP",
        "auth.otpPrompt": "{{destination}} پر بھیجا گیا 6 ہندسوں کا OTP درج کریں",
        "auth.resendOtp": "OTP دوبارہ بھیجیں",
        "auth.resendAvailableIn": "{{seconds}} سیکنڈ میں دوبارہ بھیجیں",
        "auth.backToLogin": "لاگ ان پر واپس",
        "auth.otpSent": "اگر اکاؤنٹ موجود ہے تو تصدیقی کوڈ بھیج دیا گیا ہے۔",
        "auth.otpVerified": "OTP تصدیق ہو گیا۔ سائن ان ہو رہا ہے…",
        "auth.otpInvalid": "غلط تصدیقی کوڈ۔",
        "auth.otpExpired": "تصدیقی کوڈ ختم ہو گیا۔ نیا کوڈ مانگیں۔",
        "auth.otpTooManyAttempts": "بہت زیادہ غلط کوششیں۔ نیا کوڈ مانگیں۔",
        "auth.otpTooManyRequests": "بہت زیادہ OTP درخواستیں۔ بعد میں کوشش کریں۔",
        "auth.otpNetworkError": "نیٹ ورک خرابی۔ دوبارہ کوشش کریں۔",
        "auth.otpProviderMissing": "OTP فراہمی فراہم کنندہ ترتیب نہیں دیا گیا۔",
        "auth.otpDevHint": "ڈیولپمنٹ موڈ — کوڈ بھرا ہوا",
        "notifications.title": "اطلاعات",
        "notifications.empty": "ابھی کوئی اطلاع نہیں۔",
        "notifications.markRead": "پڑھا ہوا نشان زد کریں",
        "notifications.markAllRead": "سب کو پڑھا ہوا نشان زد کریں",
        "notifications.viewAnalysis": "تجزیہ دیکھیں",
        "notifications.moderateRisk.title": "درمیانی خطرہ پایا گیا",
        "notifications.moderateRisk.message": "{{cowId}} میں ممکنہ {{detection}} اشارے۔ خطرہ: {{risk}}۔ شناخت کا اعتماد: {{confidence}}%۔",
        "notifications.highRisk.title": "زیادہ خطرہ پایا گیا",
        "notifications.highRisk.message": "{{cowId}} میں ممکنہ {{detection}} اشارے۔ خطرہ: {{risk}}۔ شناخت کا اعتماد: {{confidence}}%۔",
        "notifications.criticalRisk.title": "سنگین خطرہ پایا گیا",
        "notifications.criticalRisk.message": "{{cowId}} میں ممکنہ {{detection}} اشارے۔ خطرہ: {{risk}}۔ شناخت کا اعتماد: {{confidence}}%۔ فوری طور پر ویٹرنری ڈاکٹر سے رابطہ کریں۔",
        "settings.notificationsSubtitle": "منتخب کریں کہ BOVIMED میں کون سے الرٹس موصول ہوں۔",
        "settings.notifHealthAlerts": "صحت کے الرٹس (درمیانی اور اوپر)",
        "settings.notifAnalysisCompleted": "تجزیہ مکمل",
        "settings.notifVeterinary": "ویٹرنری یاددہانیاں",
        "settings.notifSystem": "سسٹم اطلاعات",
        "settings.notifBrowser": "براؤزر اطلاعات",
        "settings.enableBrowserNotifications": "BOVIMED اطلاعات فعال کریں",
        "settings.browserNotifEnabled": "براؤزر اطلاعات فعال۔",
        "settings.browserNotifDenied": "براؤزر اطلاعات بلاک ہیں۔ ان-ایپ اطلاعات کام کرتی ہیں۔",
        "settings.browserNotifUnsupported": "اس ڈیوائس پر براؤزر اطلاعات معاون نہیں۔",
        "settings.saveNotifications": "اطلاع کی ترتیبات محفوظ کریں",
        "settings.notifSaved": "اطلاع کی ترتیبات محفوظ ہو گئیں۔",
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
    en_flat = flatten(json.loads((DIR / "en.json").read_text(encoding="utf-8")))
    new_keys = [k for k in en_flat if k.startswith(("auth.loginWith", "auth.send", "auth.verify", "auth.otp", "auth.resend", "auth.back", "notifications.", "settings.notif", "settings.enable", "settings.browser", "settings.saveNotifications"))]
    for code in sorted(p for p in DIR.glob("*.json") if p.name != "en.json"):
        lang = code.stem
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
            merge_locale(lang, {k: en_flat[k] for k in new_keys})


if __name__ == "__main__":
    main()
