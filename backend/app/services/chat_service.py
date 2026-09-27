"""BOVIMED chatbot — safe farmer guidance with multilingual knowledge base, strict medical safety, and optional external LLM."""

from __future__ import annotations

import logging
import os
import re
from typing import Any

from app.services.ai_chat_service import generate_ai_reply, get_ai_config_status
from app.services.care_guidance import get_care_guidance, normalize_risk

logger = logging.getLogger(__name__)

# Languages with direct local rule-based response dictionaries
SUPPORTED_LOCAL_LANGS = {
    "en", "hi", "kn", "te", "ta", "ml", "mr", "bn", "gu", "pa", "or", "as", "ur"
}

FAQ_KNOWLEDGE: dict[str, dict[str, str]] = {
    "en": {
        "signs": (
            "Common signs farmers watch for include a hot, swollen, hard or painful udder, "
            "changes in milk (clots, watery milk, discoloration), reduced milk yield, "
            "and cow restlessness during milking. "
            "These signs need a veterinarian to confirm — BOVIMED cannot diagnose."
        ),
        "prevent": (
            "Helpful precautions: keep udders clean and dry, use clean milking equipment, "
            "wash hands thoroughly, milk healthy quarters first, and inspect milk before milking. "
            "Maintain clean shed bedding. Ask your veterinarian for a herd health plan."
        ),
        "high_risk": (
            "Your scan indicates High or Critical risk. Arrange veterinary evaluation promptly. "
            "Do not start antibiotics from the AI result alone. Keep the affected animal under "
            "close observation and maintain strict hygiene while seeking professional care."
        ),
        "milking": (
            "During milking: clean and dry teats before attachment, ensure milking equipment is sterilized, "
            "and check foremilk for abnormalities. Avoid teat injury and maintain regular milking routines."
        ),
        "when_vet": (
            "Contact a veterinarian immediately if there is udder swelling, heat, pain, abnormal milk, "
            "fever, sudden drop in milk yield, or if BOVIMED indicates Moderate, High, or Critical risk."
        ),
        "interpret": (
            "Your BOVIMED scan shows detected visual patterns and a risk level as screening guidance only. "
            "Confidence reflects how closely visual features match training samples — not a medical diagnosis. "
            "Always consult a qualified veterinarian."
        ),
        "find_vet": (
            "Use the 'Find Veterinarian' tool in BOVIMED to search by State, District, City, or PIN code. "
            "BOVIMED never invents phone numbers or addresses. If unverified, use map directions to locate verified clinics."
        ),
        "waiting": (
            "While waiting for the veterinarian: keep the cow isolated in a clean, dry, shaded area. "
            "Provide clean drinking water. Do not administer any medication without direct veterinary instructions."
        ),
        "medicine": (
            "I can explain common veterinary treatment approaches at a general level, but BOVIMED cannot prescribe medicine "
            "or dosage. A qualified veterinarian should examine the cow and decide the appropriate treatment."
        ),
        "antibiotic": (
            "Please do not start antibiotics based only on the BOVIMED result. A veterinarian should determine whether treatment is appropriate."
        ),
        "emergency": (
            "For urgent symptoms or Critical risk, seek veterinary assistance immediately. "
            "Do not administer medication without veterinary advice."
        ),
        "history": (
            "Reviewing cow health history helps identify recurring udder inflammation patterns. "
            "Share previous BOVIMED screening records with your veterinarian during clinical visits."
        ),
    },
    "hi": {
        "signs": (
            "थनैला रोग (Mastitis) के मुख्य लक्षण हैं: थनों में सूजन, गर्मी, कठोरता या दर्द, "
            "दूध में बदलाव (छीछड़े, पानी जैसा दूध, असामान्य रंग), दूध उत्पादन में गिरावट, "
            "और दुहते समय गाय का बेचैन होना। इसकी पुष्टि पशु चिकित्सक ही कर सकते हैं।"
        ),
        "prevent": (
            "बचाव के उपाय: थनों को हमेशा साफ और सूखा रखें, दुहने के बर्तनों की स्वच्छता बनाए रखें, "
            "हाथ धोकर दुहें, और स्वस्थ थनों को पहले दुहें। बाड़े में सूखा बिछावन रखें।"
        ),
        "high_risk": (
            "यदि स्कैन में उच्च या गंभीर जोखिम (High/Critical Risk) दिखा है, तो तुरंत पशु चिकित्सक से संपर्क करें। "
            "केवल AI परिणाम के आधार पर एंटीबायोटिक शुरू न करें। गाय को अलग और साफ स्थान पर रखें।"
        ),
        "milking": (
            "दुहते समय सावधानियां: दुहने से पहले थनों को साफ करके पोंछ लें, साफ बर्तनों का उपयोग करें, "
            "और पहली धार की जांच करें। दुहने के बाद गाय को कुछ समय खड़े रहने दें।"
        ),
        "when_vet": (
            "थनों में सूजन, गर्माहट, दर्द, दूध में खून या छीछड़े दिखने, या बुखार होने पर तुरंत पशु चिकित्सक को बुलाएं।"
        ),
        "interpret": (
            "BOVIMED स्कैन केवल प्रारंभिक स्क्रीनिंग मार्गदर्शन है। कॉन्फिडेंस AI मॉडल का मिलान स्तर है, "
            "यह कोई पक्का चिकित्सीय निदान नहीं है। डॉक्टर से सलाह अवश्य लें।"
        ),
        "find_vet": (
            "निकटतम पशु चिकित्सक खोजने के लिए BOVIMED में राज्य/जिला/पिनकोड द्वारा खोजें। "
            "हम कोई भी फर्जी नंबर नहीं दिखाते। जाने से पहले उपलब्धता की पुष्टि करें।"
        ),
        "waiting": (
            "डॉक्टर के आने तक: गाय को शांत, साफ और सूखी जगह पर रखें। पीने के लिए ताजा पानी दें, "
            "और डॉक्टर की सलाह के बिना कोई दवाई न दें।"
        ),
        "medicine": (
            "मैं सामान्य देखभाल के बारे में बता सकता हूँ, लेकिन BOVIMED दवा या खुराक (dosage) नहीं बता सकता। "
            "केवल एक योग्य पशु चिकित्सक ही गाय की जांच कर सही इलाज तय कर सकता है।"
        ),
        "antibiotic": (
            "कृपया केवल BOVIMED परिणाम के आधार पर एंटीबायोटिक्स शुरू न करें। पशु चिकित्सक ही तय करेंगे कि इलाज आवश्यक है या नहीं।"
        ),
        "emergency": (
            "गंभीर स्थिति में तुरंत नजदीकी पशु चिकित्सालय से संपर्क करें। बिना सलाह के कोई दवा न दें।"
        ),
        "history": (
            "गाय के स्वास्थ्य इतिहास की जांच करने से बार-बार होने वाले संक्रमण का पता चलता है। "
            "डॉक्टर को पुरानी जांच रिपोर्ट अवश्य दिखाएं।"
        ),
    },
    "kn": {
        "signs": (
            "ಕೆಚ್ಚಲು ಬಾವು (ಮ್ಯಾಸ್ಟೈಟಿಸ್) ರೋಗಲಕ್ಷಣಗಳು: ಕೆಚ್ಚಲು ಬಿಸಿಯಾಗುವುದು, ಊತ, ಗಟ್ಟಿಯಾಗುವುದು ಅಥವಾ ನೋವು, "
            "ಹಾಲಿನಲ್ಲಿ ಬದಲಾವಣೆ (ಹೆಪ್ಪುಗಟ್ಟುವುದು, ನೀರಾಗುವುದು, ಬಣ್ಣ ಬದಲಾವಣೆ), ಹಾಲಿನ ಇಳುವರಿ ಕಡಿಮೆಯಾಗುವುದು. "
            "ಇದನ್ನು ಪಶುವೈದ್ಯರೇ ಪರೀಕ್ಷಿಸಿ ಖಚಿತಪಡಿಸಬೇಕು."
        ),
        "prevent": (
            "ತಡೆಗಟ್ಟುವ ಕ್ರಮಗಳು: ಕೆಚ್ಚಲನ್ನು ಸ್ವಚ್ಛ ಮತ್ತು ಒಣಗಿದ ಸ್ಥಿತಿಯಲ್ಲಿಡಿ, ಹಾಲು ಕರೆಯುವ ಉಪಕರಣಗಳನ್ನು ಶುಚಿಯಾಗಿಡಿ, "
            "ಕೈಗಳನ್ನು ತೊಳೆದು ಹಾಲು ಕರೆಯಿರಿ, ಮತ್ತು ಕೊಟ್ಟಿಗೆಯ ನೈರ್ಮಲ್ಯವನ್ನು ಕಾಪಾಡಿ."
        ),
        "high_risk": (
            "ಹೆಚ್ಚಿನ ಅಪಾಯ (High/Critical Risk) ಕಂಡುಬಂದರೆ ತಕ್ಷಣವೇ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ. "
            "ಕೇವಲ AI ಫಲಿತಾಂಶದ ಆಧಾರದ ಮೇಲೆ ಆ್ಯಂಟಿಬಯೋಟಿಕ್ ನೀಡಬೇಡಿ. ಹಸುವನ್ನು ಸೂಕ್ಷ್ಮವಾಗಿ ಗಮನಿಸಿ."
        ),
        "milking": (
            "ಹಾಲು ಕರೆಯುವ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು: ಕರೆಯುವ ಮುನ್ನ ಮೊಲೆತೊಟ್ಟುಗಳನ್ನು ತೊಳೆದು ಒರೆಸಿ, "
            "ಶುದ್ಧ ಪಾತ್ರೆಗಳನ್ನು ಬಳಸಿ, ಮತ್ತು ಮೊದಲ ಹಾಲಿನ ಹನಿಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ."
        ),
        "when_vet": (
            "ಕೆಚ್ಚಲಿನಲ್ಲಿ ಊತ, ನೋವು, ಹಾಲಿನಲ್ಲಿ ರಕ್ತ ಅಥವಾ ಗಂಟುಗಳು ಕಂಡಾಗ ಅಥವಾ ಜ್ವರವಿದ್ದಾಗ ಕೂಡಲೇ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."
        ),
        "interpret": (
            "BOVIMED ಸ್ಕ್ಯಾನ್ ಕೇವಲ ಪ್ರಾಥಮಿಕ ತಪಾಸಣಾ ಮಾರ್ಗದರ್ಶನವಾಗಿದೆ. ಕಾನ್ಫಿಡೆನ್ಸ್ ಕೇವಲ AI ಹೋಲಿಕೆಯ ಅಳತೆಯಾಗಿದೆ. "
            "ಪೂರ್ಣ ರೋಗನಿರ್ಣಯಕ್ಕಾಗಿ ಪಶುವೈದ್ಯರನ್ನು ಕಾಣಿರಿ."
        ),
        "find_vet": (
            "ಹತ್ತಿರದ ಪಶುವೈದ್ಯರನ್ನು ಹುಡುಕಲು ರಾಜ್ಯ/ಜಿಲ್ಲೆ/ಪಿನ್‌ಕೋಡ್ ನಮೂದಿಸಿ. "
            "BOVIMED ಎಂದಿಗೂ ನಕಲಿ ಸಂಖ್ಯೆಗಳನ್ನು ನೀಡುವುದಿಲ್ಲ. ಭೇಟಿ ನೀಡುವ ಮುನ್ನ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."
        ),
        "waiting": (
            "ವೈದ್ಯರು ಬರುವವರೆಗೆ: ಹಸುವನ್ನು ಸ್ವಚ್ಛ, ಒಣ ಜಾಗದಲ್ಲಿ ವಿಶ್ರಾಂತಿ ಪಡೆಯಲು ಬಿಡಿ. ಶುದ್ಧ ಕುಡಿಯುವ ನೀರು ನೀಡಿ, "
            "ಮತ್ತು ವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಯಾವುದೇ ಔಷಧಿಯನ್ನು ನೀಡಬೇಡಿ."
        ),
        "medicine": (
            "ನಾನು ಸಾಮಾನ್ಯ ಪಶು ಆರೈಕೆಯ ಬಗ್ಗೆ ಮಾಹಿತಿ ನೀಡಬಲ್ಲೆ, ಆದರೆ BOVIMED ಯಾವುದೇ ಔಷಧ ಅಥವಾ ಡೋಸೇಜ್ ಸೂಚಿಸುವುದಿಲ್ಲ. "
            "ಅರ್ಹ ಪಶುವೈದ್ಯರು ಮಾತ್ರ ಹಸುವನ್ನು ಪರೀಕ್ಷಿಸಿ ಸೂಕ್ತ ಚಿಕಿತ್ಸೆಯನ್ನು ನಿರ್ಧರಿಸಬೇಕು."
        ),
        "antibiotic": (
            "ದಯವಿಟ್ಟು ಕೇವಲ BOVIMED ಫಲಿತಾಂಶವನ್ನು ಆಧರಿಸಿ ಆಂಟಿಬಯೋಟಿಕ್ ಔಷಧಗಳನ್ನು ಪ್ರಾರಂಭಿಸಬೇಡಿ. ಪಶುವೈದ್ಯರ ಸಲಹೆ ಅತ್ಯಗತ್ಯ."
        ),
        "emergency": (
            "ತುರ್ತು ಪರಿಸ್ಥಿತಿಯಲ್ಲಿ ತಕ್ಷಣ ಪಶುವೈದ್ಯಕೀಯ ಆಸ್ಪತ್ರೆಗೆ ಸಂಪರ್ಕಿಸಿ. ವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಯಾವುದೇ ಇಂಜೆಕ್ಷನ್ ನೀಡಬೇಡಿ."
        ),
        "history": (
            "ಹಸುವಿನ ಹಿಂದಿನ ಸ್ಕ್ಯಾನ್ ಇತಿಹಾಸವನ್ನು ಗಮನಿಸುವುದು ಮರುಕಳಿಸುವ ಕೆಚ್ಚಲು ಬಾವಿನ ಲಕ್ಷಣಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಸಹಕಾರಿಯಾಗಿದೆ."
        ),
    },
    "te": {
        "signs": (
            "పొదుగు వాపు (Mastitis) ప్రధాన లక్షణాలు: పొదుగు వేడిగా ఉండటం, వాపు, గట్టిపడటం లేదా నొప్పి, "
            "పాలలో మార్పులు (గడ్డలు కట్టడం, పలచబడటం, రంగు మారడం), పాల దిగుబడి తగ్గడం. "
            "దీనిని పశువైద్యుడు మాత్రమే నిర్ధారించాలి."
        ),
        "prevent": (
            "నివారణ చర్యలు: పొదుగును శుభ్రంగా మరియు పొడిగా ఉంచండి, పాలు పితికే పరికరాలను పరిశుభ్రంగా ఉంచండి, "
            "చేతులు శుభ్రంగా కడుక్కోండి, మరియు పాకలో పరిశుభ్రత పాటించండి."
        ),
        "high_risk": (
            "హై లేదా క్రిటికల్ రిస్క్ కనిపించినప్పుడు వెంటనే పశువైద్యుడిని సంప్రదించండి. "
            "కేవలం AI ఫలితం చూసి యాంటీబయాటిక్స్ వాడకండి. ఆవును పరిశీలనలో ఉంచండి."
        ),
        "milking": (
            "పాలు పితికే సమయంలో: పితికే ముందు పొదుగును శుభ్రపరచి పొడిగా తుడవండి, "
            "పరిశుభ్రమైన పాత్రలు వాడండి మరియు మొదటి పాలను పరిశీలించండి."
        ),
        "when_vet": (
            "పొదుగులో వాపు, వేడి, నొప్పి, పాలలో మార్పులు లేదా జ్వరం వచ్చినప్పుడు వెంటనే పశువైద్యుడిని సంప్రదించండి."
        ),
        "interpret": (
            "BOVIMED స్కానింగ్ అనేది కేవలం ప్రాథమిక స్క్రీనింగ్ మార్గదర్శకం మాత్రమే. "
            "ఖచ్చితమైన రోగ నిర్ధారణ కోసం అర్హత కలిగిన పశువైద్యుడిని సంప్రదించండి."
        ),
        "find_vet": (
            "సమీపంలోని పశువైద్యుడిని కనుగొనడానికి రాష్ట్రం/జిల్లా/పిన్‌కోడ్ నమోదు చేయండి. "
            "వెళ్ళే ముందు వారి లభ్యతను సరిచూసుకోండి."
        ),
        "waiting": (
            "వైద్యుడు వచ్చే వరకు: ఆవును శుభ్రమైన, నీడ ఉన్న ప్రదేశంలో ఉంచండి. పరిశుభ్రమైన నీరు అందించండి, "
            "వైద్యుడి సలహా లేకుండా మందులు వేయకండి."
        ),
        "medicine": (
            "నేను సాధారణ పశు సంరక్షణ పద్ధతుల గురించి వివరించగలను, కానీ BOVIMED ఎలాంటి మందులు లేదా మోతాదును సూచించదు. "
            "అర్హత కలిగిన పశువైద్యుడు మాత్రమే తగిన చికిత్సను నిర్ణయించాలి."
        ),
        "antibiotic": (
            "దయచేసి BOVIMED ఫలితం ఆధారంగా మాత్రమే యాంటీబయాటిక్స్ ప్రారంభించవద్దు. పశువైద్యుడి నిర్ణయం అవసరం."
        ),
        "emergency": (
            "తీవ్రమైన అత్యవసర పరిస్థితుల్లో వెంటనే పశువైద్య సహాయం పొందండి. సలహా లేకుండా మందులు ఇవ్వకండి."
        ),
        "history": (
            "ఆవు ఆరోగ్య చరిత్రను సమీక్షించడం వల్ల పొదుగు సమస్యలను ముందుగానే పసిగట్టవచ్చు."
        ),
    },
    "ta": {
        "signs": (
            "மடி நோய் (Mastitis) அறிகுறிகள்: மடியில் வீக்கம், சூடு, கடினத்தன்மை அல்லது வலி, "
            "பாலில் மாற்றங்கள் (திரிதல், நீர்த்துப்போதல், நிற மாற்றம்), பால் அளவு குறைதல். "
            "இதை கால்நடை மருத்துவரால் மட்டுமே உறுதிப்படுத்த முடியும்."
        ),
        "prevent": (
            "தடுப்பு முறைகள்: மடியை எப்போதும் சுத்தமாகவும் உலர்வாகவும் வைக்கவும், பால் கறக்கும் பாத்திரங்களை சுத்தமாக பராமரிக்கவும், "
            "கைகளை நன்கு கழுவி பால் கறக்கவும், மாட்டுக்கொட்டகையை சுத்தமாக வைத்திருக்கவும்."
        ),
        "high_risk": (
            "அதிக ஆபத்து (High/Critical Risk) காணப்பட்டால் உடனே கால்நடை மருத்துவரை அணுகவும். "
            "AI முடிவை மட்டுமே நம்பி ஆன்டிபயாடிக் மருந்துகளைத் தொடங்க வேண்டாம். மாட்டை கண்காணிப்பில் வைக்கவும்."
        ),
        "milking": (
            "பால் கறக்கும் போது: கறப்பதற்கு முன் மடியை கழுவி துடைக்கவும், சுத்தமான பாத்திரங்களை பயன்படுத்தவும், "
            "முதல் சில சொட்டு பாலை பரிசோதிக்கவும்."
        ),
        "when_vet": (
            "மடியில் வீக்கம், சூடு, வலி, பாலில் ரத்தம் அல்லது திரிவு தென்பட்டால் உடனே கால்நடை மருத்துவரை அழைக்கவும்."
        ),
        "interpret": (
            "BOVIMED ஸ்கேன் என்பது ஒரு முதற்கட்ட வழிகாட்டுதல் மட்டுமே. இது மருத்துவ நோயறிதல் அல்ல. "
            "கண்டிப்பாக கால்நடை மருத்துவரிடம் ஆலோசனை பெறவும்."
        ),
        "find_vet": (
            "அருகிலுள்ள கால்நடை மருத்துவமனையை கண்டறிய மாநிலம்/மாவட்டம்/அஞ்சல் குறியீட்டை உள்ளிடவும். "
            "நேரில் செல்லும் முன் இருப்பதை உறுதிப்படுத்தவும்."
        ),
        "waiting": (
            "மருத்துவர் வரும் வரை: மாட்டை சுத்தமான, நிழலான இடத்தில் வைக்கவும். சுத்தமான குடிநீர் வழங்கவும், "
            "மருத்துவர் ஆலோசனையின்றி மருந்துகளை வழங்க வேண்டாம்."
        ),
        "medicine": (
            "பொதுவான பராமரிப்பு முறைகளை என்னால் விளக்க முடியும், ஆனால் BOVIMED மருந்துகளையோ அல்லது அளவையோ பரிந்துரைக்காது. "
            "தகுதிவாய்ந்த கால்நடை மருத்துவர் மட்டுமே பரிசோதித்து சிகிச்சை அளிக்க வேண்டும்."
        ),
        "antibiotic": (
            "BOVIMED முடிவை மட்டுமே அடிப்படையாகக் கொண்டு ஆன்டிபயாடிக் மருந்துகளைத் தொடங்க வேண்டாம். மருத்துவர் ஆலோசனையே முக்கியம்."
        ),
        "emergency": (
            "அவசர காலங்களில் உடனடியாக கால்நடை மருத்துவ உதவியை நாடவும்."
        ),
        "history": (
            "மாட்டின் முந்தைய பரிசோதனை வரலாற்றை கவனிப்பது மீண்டும் மடி நோய் வருவதைத் தடுக்க உதவும்."
        ),
    },
    "ml": {
        "signs": (
            "അകിടുവീക്കത്തിന്റെ (Mastitis) ലക്ഷണങ്ങൾ: അകിടിൽ വീക്കം, ചൂട്, കട്ടി അല്ലെങ്കിൽ വേദന, "
            "പാലിലെ മാറ്റങ്ങൾ (കട്ടപിടിക്കൽ, നിറംമാറ്റം), പാൽ ഉൽപ്പാദനം കുറയുക. "
            "ഒരു വെറ്ററിനറി ഡോക്ടർ മാത്രമേ ഇത് രോഗനിർണ്ണയം നടത്താവൂ."
        ),
        "prevent": (
            "പ്രതിരോധ മാർഗ്ഗങ്ങൾ: അകിട് എപ്പോഴും വൃത്തിയും ഉണങ്ങിയതുമായി സൂക്ഷിക്കുക, കറവ ഉപകരണങ്ങൾ വൃത്തിയാക്കുക, "
            "കൈകൾ കഴുകി കറക്കുക, തൊഴുത്ത് വൃത്തിയായി സൂക്ഷിക്കുക."
        ),
        "high_risk": (
            "ഉയർന്ന അപകടസാധ്യത (High/Critical) കണ്ടാൽ ഉടൻ വെറ്ററിനറി ഡോക്ടറെ ബന്ധപ്പെടുക. "
            "AI ഫലം മാത്രം അടിസ്ഥാനമാക്കി ആന്റിബയോട്ടിക്കുകൾ നൽകരുത്."
        ),
        "milking": (
            "കറവ സമയത്തെ മുൻകരുതലുകൾ: കറക്കുന്നതിന് മുൻപ് മുലക്കാമ്പുകൾ കഴുകി തുടയ്ക്കുക, "
            "ആദ്യത്തെ കുറച്ചു പാൽ പരിശോധിച്ച് കുഴപ്പമില്ലെന്ന് ഉറപ്പുവരുത്തുക."
        ),
        "when_vet": (
            "അകിടിൽ വീക്കം, ചൂട്, വേദന, പാലിൽ വ്യത്യാസം എന്നിവ കണ്ടാൽ ഉടൻ ഡോക്ടറെ കാണിക്കുക."
        ),
        "interpret": (
            "BOVIMED സ്കാൻ ഒരു പ്രാരംഭ സ്ക്രീനിംഗ് മാർഗ്ഗനിർദ്ദേശം മാത്രമാണ്, അന്തിമ രോഗനിർണ്ണയമല്ല."
        ),
        "find_vet": (
            "അടുത്തുള്ള മൃഗാശുപത്രി കണ്ടെത്താൻ സംസ്ഥാനം/ജില്ല/പിൻകോഡ് നൽകുക."
        ),
        "waiting": (
            "ഡോക്ടർ വരുന്നതുവരെ: പശുവിനെ ശാന്തവും വൃത്തിയുള്ളതുമായ സ്ഥലത്ത് നിർത്തുക. കുടിവെള്ളം നൽകുക."
        ),
        "medicine": (
            "BOVIMED മരുന്നുകളോ അളവോ (dosage) നിർദ്ദേശിക്കില്ല. അംഗീകൃത വെറ്ററിനറി ഡോക്ടർ മാത്രമേ ചികിത്സ നിശ്ചയിക്കാവൂ."
        ),
        "antibiotic": (
            "ദയവായി ഡോക്ടറുടെ നിർദ്ദേശമില്ലാതെ ആന്റിബയോട്ടിക്കുകൾ ആരംഭിക്കരുത്."
        ),
        "emergency": (
            "അടിയന്തര സാഹചര്യങ്ങളിൽ ഉടൻ തന്നെ അടുത്തുള്ള വെറ്ററിനറി ആശുപത്രിയുമായി ബന്ധപ്പെടുക."
        ),
        "history": (
            "പശുവിന്റെ മുൻകാല ആരോഗ്യ ചരിത്രം വെറ്ററിനറി ഡോക്ടറെ കാണിക്കുന്നത് ഉചിതമായ ചികിത്സ നൽകാൻ സഹായിക്കും."
        ),
    },
    "mr": {
        "signs": (
            "स्तनदाह (Mastitis) ची लक्षणे: कासेवर सूज, उष्णता, कडकपणा किंवा वेदना, "
            "दुधात बदल (गाठी, पाणीदार दूध, रंग बदलणे), दुधाचे प्रमाण घटणे. "
            "याचे अचूक निदान पशुवैद्यकीय डॉक्टरांकडूनच करून घ्यावे."
        ),
        "prevent": (
            "प्रतिबंधात्मक उपाय: कास नेहमी स्वच्छ व कोरडी ठेवा, दूध काढण्याची भांडी स्वच्छ ठेवा, "
            "हात धुवून दूध काढा, आणि गोठ्यात स्वच्छता राखा."
        ),
        "high_risk": (
            "उच्च धोका (High/Critical Risk) आढळल्यास ताबडतोब पशुवैद्यांशी संपर्क साधा. "
            "केवळ AI तपासणीवरून परस्पर अँटीबायोटिक्स सुरू करू नका."
        ),
        "milking": (
            "दूध काढताना काळजी: दूध काढण्यापूर्वी सड स्वच्छ धुवून कोरडे करा आणि पहिल्या धारेचे दूध तपासा."
        ),
        "when_vet": (
            "कास सुजल्यास, गरम लागल्यास, दुधात रक्त किंवा गाठी आल्यास त्वरित डॉक्टरांना बोलवा."
        ),
        "interpret": (
            "BOVIMED तपासणी हे केवळ प्राथमिक मार्गदर्शक आहे, वैद्यकीय निदान नाही."
        ),
        "find_vet": (
            "जवळचे पशुवैद्यकीय रुग्णालय शोधण्यासाठी राज्य/जिल्हा/पिनकोड प्रविष्ट करा."
        ),
        "waiting": (
            "डॉक्टर येईपर्यंत: गाईला शांत, कोरड्या व स्वच्छ ठिकाणी ठेवा. डॉक्टरांच्या सल्ल्याशिवाय कोणतेही औषध देऊ नका."
        ),
        "medicine": (
            "BOVIMED औषधे किंवा मात्रा (dosage) लिहून देत नाही. योग्य उपचारासाठी पशुवैद्यांचा सल्ला घ्या."
        ),
        "antibiotic": (
            "कृपया केवळ BOVIMED निकालावर आधारित अँटीबायोटिक्स सुरू करू नका."
        ),
        "emergency": (
            "गंभीर परिस्थितीत तात्काळ पशुवैद्यकीय मदत मिळवा."
        ),
        "history": (
            "गाईच्या आरोग्याचा इतिहास तपासल्यास आजाराची पुनरावृत्ती टाळण्यास मदत होते."
        ),
    },
    "bn": {
        "signs": (
            "ওলান ফোলা বা ম্যাসটাইটিস রোগের লক্ষণ: ওলান গরম হওয়া, ফোলা, শক্ত হওয়া বা ব্যথা, "
            "দুধের পরিবর্তন (দলা বাঁধা, পাতলা দুধ, অস্বাভাবিক রঙ), দুধের উৎপাদন কমে যাওয়া। "
            "পশু চিকিৎসকই এটি নিশ্চিত করতে পারেন।"
        ),
        "prevent": (
            "প্রতিরোধের উপায়: ওলান পরিষ্কার ও শুকনো রাখুন, দুধ দোয়ানোর সরঞ্জাম জীবাণুমুক্ত রাখুন, "
            "হাত ধুয়ে দুধ দোয়ান এবং গোয়ালঘর পরিষ্কার রাখুন।"
        ),
        "high_risk": (
            "উচ্চ ঝুঁকি (High/Critical Risk) দেখা দিলে অবিলম্বে পশু চিকিৎসকের পরামর্শ নিন। "
            "শুধুমাত্র AI ফলের ওপর নির্ভর করে অ্যান্টিবায়োটিক শুরু করবেন না।"
        ),
        "milking": (
            "দুধ দোয়ানোর সতর্কতা: দোয়ানোর আগে ওলানের বাট পরিষ্কার করে মুছে নিন এবং প্রথম দুধ পরীক্ষা করুন।"
        ),
        "when_vet": (
            "ওলানে ফোলা, ব্যথা, দুধে রক্ত বা ছানার মতো অংশ দেখা দিলে দ্রুত পশু চিকিৎসকের শরণাপন্ন হন।"
        ),
        "interpret": (
            "BOVIMED স্ক্যান শুধুমাত্র প্রাথমিক স্ক্রীনিং গাইডেন্স প্রদান করে, এটি চূড়ান্ত ডাক্তারি রোগনির্ণয় নয়।"
        ),
        "find_vet": (
            "নিকটস্থ পশু চিকিৎসক বা হাসপাতাল খুঁজতে রাজ্য/জেলা/পিনকোড ব্যবহার করুন।"
        ),
        "waiting": (
            "চিকিৎসক আসার আগে পর্যন্ত: গরুকে পরিষ্কার ও শুকনো জায়গায় রাখুন। চিকিৎসকের পরামর্শ ছাড়া কোনো ওষুধ দেবেন না।"
        ),
        "medicine": (
            "BOVIMED কোনো ওষুধ বা ডোজ নির্ধারণ করে না। কেবলমাত্র একজন নিবন্ধিত পশু চিকিৎসকই সঠিক চিকিৎসা দিতে পারেন।"
        ),
        "antibiotic": (
            "দয়া করে শুধুমাত্র BOVIMED ফলের ওপর ভিত্তি করে অ্যান্টিবায়োটিক শুরু করবেন না।"
        ),
        "emergency": (
            "জরুরি পরিস্থিতিতে নিকটস্থ পশু হাসপাতালে অবিলম্বে যোগাযোগ করুন।"
        ),
        "history": (
            "গরুর স্বাস্থ্যের পূর্বের ইতিহাস পর্যবেক্ষণ করলে সঠিক চিকিৎসা সহজে নেওয়া যায়।"
        ),
    },
    "gu": {
        "signs": (
            "મસ્ટાઇટિસ (આંચળનો સોજો) ના લક્ષણો: આંચળ ગરમ થવો, સોજો, કડક થવો કે દુખાવો, "
            "દૂધમાં ફેરફાર (ગાંઠો, પાતળું દૂધ, રંગ બદલાવો), દૂધ ઉત્પાદનમાં ઘટાડો. "
            "આનું ચોક્કસ નિદાન ફક્ત પશુચિકિત્સક જ કરી શકે છે."
        ),
        "prevent": (
            "બચાવના પગલાં: આંચળ હંમેશા સ્વચ્છ અને સૂકા રાખો, દોહવાના સાધનો સાફ રાખો, "
            "હાથ ધોઈને દોહન કરો અને ગૌશાળામાં સ્વચ્છતા રાખો."
        ),
        "high_risk": (
            "જો ઉચ્ચ જોખમ (High/Critical Risk) જણાય તો તાત્કાલિક પશુચિકિત્સકનો સંપર્ક કરો. "
            "માત્ર AI પરિણામથી એન્ટિબાયોટિક શરૂ ન કરો."
        ),
        "milking": (
            "દોહન વખતે કાળજી: દોહતા પહેલા આંચળ સાફ કરીને સૂકવો અને પ્રથમ ધાર તપાસો."
        ),
        "when_vet": (
            "આંચળમાં સોજો, દુખાવો, કે દૂધમાં લોહી જણાય ત્યારે તરત જ ડોક્ટરને બોલાવો."
        ),
        "interpret": (
            "BOVIMED સ્કેન માત્ર પ્રાથમિક તપાસનું માર્ગદર્શન છે, તબીબી નિદાન નથી."
        ),
        "find_vet": (
            "નજીકના પશુચિકિત્સક શોધવા માટે રાજ્ય/જિલ્લો/પીનકોડ દાખલ કરો."
        ),
        "waiting": (
            "ડોક્ટર આવે ત્યાં સુધી ગાયને સ્વચ્છ અને શાંત જગ્યાએ રાખો. સલાહ વિના દવા ન આપો."
        ),
        "medicine": (
            "BOVIMED દવા કે ડોઝ નક્કી કરતું નથી. માત્ર લાયકાત ધરાવતા પશુચિકિત્સક જ સારવાર નક્કી કરી શકે છે."
        ),
        "antibiotic": (
            "કૃપા કરીને માત્ર BOVIMED પરિણામ પર આધાર રાખીને એન્ટિબાયોટિક્સ શરૂ કરશો નહીં."
        ),
        "emergency": (
            "તાત્કાલિક પરિસ્થિતિમાં નજીકના પશુ દવાખાને સંપર્ક કરો."
        ),
        "history": (
            "ગાયના આરોગ્યનો ઇતિહાસ તપાસવાથી જૂની બીમારીઓ ઓળખવામાં મદદ મળે છે."
        ),
    },
    "pa": {
        "signs": (
            "ਲੇਵੇ ਦੀ ਸੋਜ (ਮਸਟਾਇਟਿਸ) ਦੇ ਲੱਛਣ: ਲੇਵਾ ਗਰਮ, ਸੁੱਜਿਆ ਜਾਂ ਦਰਦਨਾਕ ਹੋਣਾ, "
            "ਦੁੱਧ ਵਿੱਚ ਫੁੱਟੀਆਂ ਜਾਂ ਪਾਣੀ ਵਰਗਾ ਹੋਣਾ, ਦੁੱਧ ਘਟਣਾ। "
            "ਇਸਦੀ ਪੁਸ਼ਟੀ ਕੇਵਲ ਪਸ਼ੂਆਂ ਦੇ ਡਾਕਟਰ ਦੁਆਰਾ ਹੀ ਕੀਤੀ ਜਾ ਸਕਦੀ ਹੈ।"
        ),
        "prevent": (
            "ਬਚਾਅ ਦੇ ਤਰੀਕੇ: ਲੇਵੇ ਨੂੰ ਸਾਫ਼ ਅਤੇ ਸੁੱਕਾ ਰੱਖੋ, ਚੁਆਈ ਵਾਲੇ ਭਾਂਡੇ ਸਾਫ਼ ਰੱਖੋ, "
            "ਹੱਥ ਧੋ ਕੇ ਚੁਆਈ ਕਰੋ ਅਤੇ ਵਾੜੇ ਵਿੱਚ ਸਫ਼ਾਈ ਰੱਖੋ।"
        ),
        "high_risk": (
            "ਜੇਕਰ ਹਾਈ ਜਾਂ ਕ੍ਰਿਟੀਕਲ ਰਿਸਕ ਆਵੇ ਤਾਂ ਤੁਰੰਤ ਪਸ਼ੂਆਂ ਦੇ ਡਾਕਟਰ ਨਾਲ ਸੰਪਰਕ ਕਰੋ। "
            "ਸਿਰਫ਼ AI ਨਤੀਜੇ ਦੇ ਆਧਾਰ 'ਤੇ ਐਂਟੀਬਾਇਓਟਿਕ ਸ਼ੁਰੂ ਨਾ ਕਰੋ।"
        ),
        "milking": (
            "ਚੁਆਈ ਵੇਲੇ ਸਾਵਧਾਨੀਆਂ: ਚੁਆਈ ਤੋਂ ਪਹਿਲਾਂ ਥਣਾਂ ਨੂੰ ਧੋ ਕੇ ਸੁਕਾਓ ਅਤੇ ਪਹਿਲੀ ਧਾਰ ਦੀ ਜਾਂਚ ਕਰੋ।"
        ),
        "when_vet": (
            "ਲੇਵੇ 'ਤੇ ਸੋਜ, ਦਰਦ ਜਾਂ ਦੁੱਧ ਵਿੱਚ ਖੂਨ ਆਉਣ 'ਤੇ ਤੁਰੰਤ ਡਾਕਟਰ ਨੂੰ ਸੱਦੋ।"
        ),
        "interpret": (
            "BOVIMED ਸਕੈਨ ਸਿਰਫ਼ ਸ਼ੁਰੂਆਤੀ ਜਾਂਚ ਮਾਰਗਦਰਸ਼ਨ ਹੈ, ਡਾਕਟਰੀ ਨਿਦਾਨ ਨਹੀਂ ਹੈ।"
        ),
        "find_vet": (
            "ਨੇੜਲੇ ਪਸ਼ੂ ਹਸਪਤਾਲ ਦੀ ਭਾਲ ਲਈ ਰਾਜ/ਜ਼ਿਲ੍ਹਾ/ਪਿੰਨਕੋਡ ਦਰਜ ਕਰੋ।"
        ),
        "waiting": (
            "ਡਾਕਟਰ ਦੇ ਆਉਣ ਤੱਕ ਗਾਂ ਨੂੰ ਸਾਫ਼ ਤੇ ਸੁੱਕੀ ਥਾਂ ਰੱਖੋ। ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਤੋਂ ਬਿਨਾਂ ਕੋਈ ਦਵਾਈ ਨਾ ਦਿਓ।"
        ),
        "medicine": (
            "BOVIMED ਕੋਈ ਦਵਾਈ ਜਾਂ ਖੁਰਾਕ ਨਹੀਂ ਦਿੰਦਾ। ਸਿਰਫ਼ ਯੋਗ ਪਸ਼ੂ ਡਾਕਟਰ ਹੀ ਇਲਾਜ ਤੈਅ ਕਰ ਸਕਦਾ ਹੈ।"
        ),
        "antibiotic": (
            "ਕਿਰਪਾ ਕਰਕੇ ਸਿਰਫ਼ BOVIMED ਨਤੀਜੇ ਦੇ ਆਧਾਰ 'ਤੇ ਐਂਟੀਬਾਇਓਟਿਕਸ ਨਾ ਦਿਓ।"
        ),
        "emergency": (
            "ਗੰਭੀਰ ਹਾਲਤ ਵਿੱਚ ਤੁਰੰਤ ਨਜ਼ਦੀਕੀ ਪਸ਼ੂ ਹਸਪਤਾਲ ਨਾਲ ਸੰਪਰਕ ਕਰੋ।"
        ),
        "history": (
            "ਗਾਂ ਦਾ ਪੁਰਾਣਾ ਰਿਕਾਰਡ ਡਾਕਟਰ ਨੂੰ ਦਿਖਾਉਣਾ ਬਿਮਾਰੀ ਦੇ ਇਲਾਜ ਵਿੱਚ ਮਦਦਗਾਰ ਹੁੰਦਾ ਹੈ।"
        ),
    },
    "or": {
        "signs": (
            "ବାହୁନା ରୋଗ (Mastitis) ର ଲକ୍ଷଣ: ଓଲଣ ଗରମ, ଫୁଲିବା, ଟାଣ ହେବା ବା ଯନ୍ତ୍ରଣା, "
            "କ୍ଷୀରରେ ପରିବର୍ତ୍ତନ (ଫଟା କ୍ଷୀର, ପତଳା ହେବା), କ୍ଷୀର ପରିମାଣ କମିବା। "
            "ଏହା ପ୍ରାଣୀ ଚିକିତ୍ସକଙ୍କ ଦ୍ୱାରା ନିଶ୍ଚିତ ହେବା ଆବଶ୍ୟକ।"
        ),
        "prevent": (
            "ନିବାରଣ ଉପାୟ: ଓଲଣ ସଫା ଓ ଶୁଖିଲା ରଖନ୍ତୁ, କ୍ଷୀର ଦୁହିଁବା ବାସନ ସଫା ରଖନ୍ତୁ, "
            "ହାତ ଧୋଇ କ୍ଷୀର ଦୁହନ୍ତୁ ଏବଂ ଗୁହାଳ ସଫା ରଖନ୍ତୁ।"
        ),
        "high_risk": (
            "ଉଚ୍ଚ ବିପଦ (High/Critical Risk) ଦେଖାଦେଲେ ତୁରନ୍ତ ପ୍ରାଣୀ ଚିକିତ୍ସକଙ୍କ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ। "
            "କେବଳ AI ରିପୋର୍ଟ ଉପରେ ନିର୍ଭର କରି ଆଣ୍ଟିବାୟୋଟିକ୍ ଦିଅନ୍ତୁ ନାହିଁ।"
        ),
        "milking": (
            "କ୍ଷୀର ଦୁହିଁବା ସମୟରେ ସତର୍କତା: ଦୁହିଁବା ପୂର୍ବରୁ ଓଲଣ ସଫା କରି ପୋଛନ୍ତୁ ଏବଂ ପ୍ରଥମ କ୍ଷୀର ପରୀକ୍ଷା କରନ୍ତୁ।"
        ),
        "when_vet": (
            "ଓଲଣରେ ଫୁଲା, ଯନ୍ତ୍ରଣା ବା କ୍ଷୀରରେ ରକ୍ତ ଦେଖାଦେଲେ ତୁରନ୍ତ ଡାକ୍ତରଙ୍କୁ ଡାକନ୍ତୁ।"
        ),
        "interpret": (
            "BOVIMED ସ୍କାନ୍ କେବଳ ପ୍ରାଥମିକ ସ୍କ୍ରିନିଂ ମାର୍ଗଦର୍ଶନ, ଏହା ଡାକ୍ତରୀ ନିଦାନ ନୁହେଁ।"
        ),
        "find_vet": (
            "ନିକଟସ୍ଥ ପ୍ରାଣୀ ଚିକିତ୍ସାଳୟ ଖୋଜିବା ପାଇଁ ରାଜ୍ୟ/ଜିଲ୍ଲା/ପିନକୋଡ୍ ପ୍ରବେଶ କରନ୍ତୁ।"
        ),
        "waiting": (
            "ଡାକ୍ତର ଆସିବା ପର୍ଯ୍ୟନ୍ତ: ଗାଈକୁ ସଫା ଓ ଶୁଖିଲା ସ୍ଥାନରେ ରଖନ୍ତୁ। ବିନା ପରାମର୍ଶରେ କୌଣସି ଔଷଧ ଦିଅନ୍ତୁ ନାହିଁ।"
        ),
        "medicine": (
            "BOVIMED କୌଣସି ଔଷଧ ବା ଡୋଜ୍ ପ୍ରଦାନ କରେ ନାହିଁ। ଯୋଗ୍ୟ ପ୍ରାଣୀ ଚିକିତ୍ସକ ହିଁ ଉପଯୁକ୍ତ ଚିକିତ୍ସା ସ୍ଥିର କରିବେ।"
        ),
        "antibiotic": (
            "ଦୟାକରି କେବଳ BOVIMED ଫଳାଫଳ ଉପରେ ଆଣ୍ଟିବାୟୋଟିକ୍ ଆରମ୍ଭ କରନ୍ତୁ ନାହିଁ।"
        ),
        "emergency": (
            "ଜରୁରୀ ପରିସ୍ଥିତିରେ ତୁରନ୍ତ ପ୍ରାଣୀ ଚିକିତ୍ସାଳୟ ସହ ଯୋଗାଯୋଗ କରନ୍ତୁ।"
        ),
        "history": (
            "ଗାଈର ପୂର୍ବ ସ୍ୱାସ୍ଥ୍ୟ ଇତିହାସ ପୁନରାବୃତ୍ତି ରୋଗ ଚିହ୍ନଟ କରିବାରେ ସାହାଯ୍ୟ କରେ।"
        ),
    },
    "as": {
        "signs": (
            "স্তন্যপ্ৰদাহ (মেষ্টাইটিছ) ৰ লক্ষণসমূহ: ওহাৰ গৰম হোৱা, ফুলি উঠা, টান বা বিষ হোৱা, "
            "গাখীৰৰ পৰিৱৰ্তন (গাখীৰ ফাটি যোৱা, পনীয়া হোৱা), গাখীৰৰ উৎপাদন হ্ৰাস পোৱা। "
            "পশু চিকিৎসকেহে এই ৰোগ নিশ্চিত কৰিব পাৰে।"
        ),
        "prevent": (
            "প্ৰতিৰোধৰ উপায়: ওহাৰ সদায় পৰিষ্কাৰ আৰু শুকান ৰাখক, গাখীৰ খিৰোৱা সঁজুলিসমূহ পৰিষ্কাৰ ৰাখক, "
            "হাত ধুই গাখীৰ খিৰাওক আৰু গোহালি পৰিষ্কাৰ ৰাখক।"
        ),
        "high_risk": (
            "উচ্চ বিপদ (High/Critical Risk) দেখা দিলে অবিলম্বে পশু চিকিৎসকৰ সৈতে যোগাযোগ কৰক। "
            "কেৱল AI ফলাফলৰ ওপৰত ভিত্তি কৰি এন্টিবায়টিক ব্যৱহাৰ নকৰিব।"
        ),
        "milking": (
            "খিৰোৱাৰ সময়ত সতৰ্কতা: খিৰোৱাৰ পূৰ্বে ওহাৰ ধুই মচি লওক আৰু প্ৰথম গাখীৰ পৰীক্ষা কৰক।"
        ),
        "when_vet": (
            "ওহাৰ ফুলা, বিষ হোৱা বা গাখীৰত তেজ দেখা পালে শীঘ্ৰে চিকিৎসকক জনাওক।"
        ),
        "interpret": (
            "BOVIMED স্কেন কেৱল প্ৰাথমিক পৰীক্ষাৰ নিৰ্দেশনাহে, ই কোনো চূড়ান্ত চিকিৎসা নিদান নহয়।"
        ),
        "find_vet": (
            "ওচৰৰ পশু চিকিৎসালয় বিচাৰিবলৈ ৰাজ্য/জিলা/পিনকোড ব্যৱহাৰ কৰক।"
        ),
        "waiting": (
            "চিকিৎসক নহালৈকে: গৰুজনীক শান্ত আৰু শুকান ঠাইত ৰাখক। চিকিৎসকৰ পৰামৰ্শ অবিহনে কোনো ঔষধ নিদিব।"
        ),
        "medicine": (
            "BOVIMED কোনো ঔষধ বা মাত্ৰা নিৰ্ধাৰণ নকৰে। উপযুক্ত পশু চিকিৎসকেহে চিকিৎসা নিৰ্ধাৰণ কৰিব পাৰিব।"
        ),
        "antibiotic": (
            "অনুগ্ৰহ কৰি কেৱল BOVIMED ফলাফলৰ ওপৰত নিৰ্ভৰ কৰি এন্টিবায়টিক আৰম্ভ নকৰিব।"
        ),
        "emergency": (
            "জৰুৰীকালীন অৱস্থাত তৎক্ষণাৎ পশু চিকিৎসালয়ৰ সৈতে যোগাযোগ কৰক।"
        ),
        "history": (
            "গৰুজনীৰ পূৰ্বৰ স্কেন ইতিহাস পশু চিকিৎসকক দেখুওৱাটো লাভজনক।"
        ),
    },
    "ur": {
        "signs": (
            "تھن کی سوزش (میسٹائٹس) کی اہم علامات: تھن کا گرم، سوجا ہوا، سخت یا دردناک ہونا، "
            "دودھ میں تبدیلی (پھٹکیاں، پتلا دودھ، غیر معمولی رنگ)، دودھ کی مقدار میں کمی۔ "
            "اس کی حتمی تصدیق صرف ایک مستند ویٹرنری ڈاکٹر ہی کر سکتا ہے۔"
        ),
        "prevent": (
            "حفاظتی اقدامات: تھنوں کو ہمیشہ صاف اور خشک رکھیں، دودھ دوہنے کے برتنوں کو جراثیم سے پاک رکھیں، "
            "ہاتھ دھو کر دودھ نکالیں، اور باڑے میں صفائی ستھرائی کا خاص خیال رکھیں۔"
        ),
        "high_risk": (
            "اگر اسکین میں زیادہ یا نازک خطرہ (High/Critical Risk) ظاہر ہو تو فوری طور پر جانوروں کے ڈاکٹر سے رابطہ کریں۔ "
            "صرف AI اسکین کی بنیاد پر اینٹی بائیوٹکس کا استعمال شروع نہ کریں۔"
        ),
        "milking": (
            "دودھ دوہتے وقت احتیاط: دودھ دوہنے سے پہلے تھنوں کو دھو کر خشک کریں اور پہلی دھار کو چیک کریں۔"
        ),
        "when_vet": (
            "تھن میں سوجن، گرمی، درد، یا دودھ میں خون نظر آنے پر فوری ڈاکٹر کو بلائیں۔"
        ),
        "interpret": (
            "BOVIMED اسکین صرف ابتدائی اسکریننگ رہنمائی ہے۔ یہ کوئی حتمی طبی تشخیص نہیں ہے۔"
        ),
        "find_vet": (
            "قریبی جانوروں کے ڈاکٹر کو تلاش کرنے کے لیے ریاست/ضلع/پن کوڈ درج کریں۔"
        ),
        "waiting": (
            "ڈاکٹر کے آنے تک جانور کو صاف اور خشک جگہ پر رکھیں۔ ڈاکٹر کے مشورے کے بغیر کوئی دوا نہ دیں۔"
        ),
        "medicine": (
            "میں عام نگہداشت کے بارے میں معلومات فراہم کر سکتا ہوں، لیکن BOVIMED ادویات یا خوراک (dosage) تجویز نہیں کرتا۔ "
            "صرف ایک مستند ویٹرنری ڈاکٹر ہی معائنے کے بعد صحیح علاج تجویز کر سکتا ہے۔"
        ),
        "antibiotic": (
            "براہ کرم صرف BOVIMED نتائج کی بنیاد پر اینٹی بائیوٹکس شروع نہ کریں۔ ویٹرنری ڈاکٹر کا فیصلہ ضروری ہے۔"
        ),
        "emergency": (
            "ہنگامی صورتحال میں فوری طور پر قریبی ویٹرنری ہسپتال سے رجوع کریں۔"
        ),
        "history": (
            "جانور کے پرانے اسکین ریکارڈز کا جائزہ لینے سے بار بار ہونے والے مسائل کا جلد پتا چلتا ہے۔"
        ),
    },
}

MED_SAFETY_DISCLAIMER = (
    " Medication should only be given under guidance from a qualified veterinarian. "
    "BOVIMED provides AI-assisted screening and care guidance. It is not a veterinary diagnosis and does not replace a qualified veterinarian."
)


def _detect_topic(message: str) -> str:
    m = message.lower()
    if any(k in m for k in ("antibiotic", "penicillin", "amoxicillin", "ceftiofur", "sulfa")):
        return "antibiotic"
    if any(k in m for k in ("medicine", "drug", "dosage", "dose", "tablet", "injection", "syrup", "capsule", "treatment")):
        return "medicine"
    if any(k in m for k in ("emergency", "urgent", "critical", "collapse", "dying", "fever", "blood in milk")):
        return "emergency"
    if any(k in m for k in ("sign", "symptom", "look like", "mastitis sign", "identify", "swelling")):
        return "signs"
    if any(k in m for k in ("prevent", "prevention", "hygiene", "avoid", "protect")):
        return "prevent"
    if any(k in m for k in ("high risk", "critical", "what should i do", "what do i do", "action", "next step")):
        return "high_risk"
    if any(k in m for k in ("milking", "milk", "teat", "parlor", "clean teat")):
        return "milking"
    if any(k in m for k in ("when", "contact", "call vet", "doctor", "veterinar")):
        return "when_vet"
    if any(k in m for k in ("find", "near", "nearby", "hospital", "clinic", "address")):
        return "find_vet"
    if any(k in m for k in ("waiting", "meanwhile", "until")):
        return "waiting"
    if any(k in m for k in ("history", "past", "record", "trend")):
        return "history"
    return "interpret"


def _format_context_note(context: dict | None, cow_id: str | None, lang: str) -> str:
    if not context and not cow_id:
        return ""
    risk = normalize_risk((context or {}).get("risk_level"))
    detection = (context or {}).get("detection") or (context or {}).get("prediction")
    conf = (context or {}).get("confidence")

    items = []
    if cow_id:
        items.append(f"Cow: {cow_id}")
    if risk:
        items.append(f"Screening Risk: {risk}")
    if detection:
        items.append(f"Detected Finding: {detection}")
    if conf is not None:
        try:
            c = float(conf)
            items.append(f"AI Confidence: {c if c > 1 else c * 100:.1f}%")
        except (TypeError, ValueError):
            pass

    if not items:
        return ""
    return f"[{' | '.join(items)}]\n\n"


UNCONFIGURED_MESSAGES = {
    "en": (
        "BOVIMED AI is not configured on the server. "
        "Set BOVIMED_LLM_ENABLED=true and GEMINI_API_KEY or OPENAI_API_KEY in backend .env. "
        "Local safety guidance is available below when you ask a question."
    ),
    "hi": (
        "BOVIMED AI सर्वर पर कॉन्फ़िगर नहीं है। "
        "backend .env में BOVIMED_LLM_ENABLED=true और GEMINI_API_KEY या OPENAI_API_KEY सेट करें।"
    ),
}

LANGUAGE_UNAVAILABLE = {
    "en": (
        "BOVIMED could not provide a reliable answer in your selected language right now. "
        "Please try again or contact a veterinarian for urgent concerns."
    ),
    "hi": (
        "BOVIMED आपकी चुनी भाषा में विश्वसनीय उत्तर नहीं दे सका। "
        "कृपया पुनः प्रयास करें या तत्काल सहायता के लिए पशु चिकित्सक से संपर्क करें।"
    ),
}


class ChatService:
    def reply(
        self,
        message: str,
        *,
        language: str = "en",
        cow_id: str | None = None,
        context: dict | None = None,
        history: list[dict[str, str]] | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        message = (message or "").strip()
        if not message:
            return {
                "answer": "Please type a question about cow health, mastitis screening, precautions, or veterinary care.",
                "language": language or "en",
                "sources": [],
                "safety_notice": True,
                "mode": "local",
            }

        lang = (language or "en").split("-")[0].lower()
        topic = _detect_topic(message)
        ai_status = get_ai_config_status()

        if ai_status.enabled and not ai_status.configured:
            notice = UNCONFIGURED_MESSAGES.get(lang) or UNCONFIGURED_MESSAGES["en"]
            local = self._local_reply(message, lang=lang, cow_id=cow_id, context=context, topic=topic)
            return {
                **local,
                "answer": notice + "\n\n" + local["answer"],
                "mode": "unconfigured",
            }

        if ai_status.enabled and ai_status.configured:
            ai_result = generate_ai_reply(
                message=message,
                language=lang,
                cow_id=cow_id,
                context=context,
                history=history,
            )
            if ai_result and ai_result.text.strip():
                final_answer = ai_result.text.strip() + "\n\n" + MED_SAFETY_DISCLAIMER
                return {
                    "answer": final_answer,
                    "language": lang,
                    "sources": [{"provider": ai_result.provider, "model": ai_result.model}],
                    "safety_notice": True,
                    "mode": "external",
                    "topic": topic,
                }
            logger.warning("LLM call failed for lang=%s; falling back to local guidance", lang)
            local = self._local_reply(message, lang=lang, cow_id=cow_id, context=context, topic=topic)
            fallback_notice = LANGUAGE_UNAVAILABLE.get(lang) or LANGUAGE_UNAVAILABLE["en"]
            return {
                **local,
                "answer": fallback_notice + "\n\n" + local["answer"],
                "mode": "error",
            }

        return self._local_reply(message, lang=lang, cow_id=cow_id, context=context, topic=topic)

    def _local_reply(
        self,
        message: str,
        *,
        lang: str,
        cow_id: str | None,
        context: dict | None,
        topic: str,
    ) -> dict[str, Any]:
        lang_key = lang if lang in FAQ_KNOWLEDGE else "en"
        base_answer = FAQ_KNOWLEDGE[lang_key].get(topic) or FAQ_KNOWLEDGE["en"][topic]
        context_prefix = _format_context_note(context, cow_id, lang)
        answer = context_prefix + base_answer

        if context and context.get("risk_level"):
            care = get_care_guidance(context.get("risk_level"))
            if topic in ("high_risk", "emergency", "interpret") and care.get("next_step"):
                answer += f"\nRecommended next step: {care['next_step']}"

        answer += "\n\n" + MED_SAFETY_DISCLAIMER

        if lang not in SUPPORTED_LOCAL_LANGS and lang != "en":
            notice = (
                "Full local guidance is not available in this language yet. "
                "Showing a safe English answer. Enable BOVIMED AI for multilingual answers.\n\n"
            )
            answer = notice + answer

        return {
            "answer": answer,
            "language": lang if lang in SUPPORTED_LOCAL_LANGS else "en",
            "sources": [],
            "safety_notice": True,
            "mode": "local",
            "topic": topic,
        }


def get_chat_service() -> ChatService:
    return ChatService()

