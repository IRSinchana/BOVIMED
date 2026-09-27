# -*- coding: utf-8 -*-
"""Generate complete locale files from hi/bn bases + per-language flat overrides."""
import copy
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"
EN = json.loads((DIR / "en.json").read_text(encoding="utf-8"))
HI = json.loads((DIR / "hi.json").read_text(encoding="utf-8"))
BN = json.loads((DIR / "bn.json").read_text(encoding="utf-8"))


def flatten(obj, p=""):
    o = {}
    for k, v in obj.items():
        nk = f"{p}.{k}" if p else k
        if isinstance(v, dict):
            o.update(flatten(v, nk))
        else:
            o[nk] = v
    return o


def unflatten(flat):
    root = {}
    for k, v in sorted(flat.items()):
        parts = k.split(".")
        cur = root
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


def write_locale(code, flat_map):
    en_keys = flatten(EN)
    missing = [k for k in en_keys if k not in flat_map]
    if missing:
        raise SystemExit(f"{code}: missing {len(missing)} keys: {missing[:8]}")
    flat_map["appName"] = "BOVIMED"
    flat_map["history.live"] = "LIVE"
    flat_map["history.demo"] = "Demo"
    data = unflatten(flat_map)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (DIR / f"{code}.json").write_text(text, encoding="utf-8")
    print(f"wrote {code}.json")


def build_from_base(base_flat, overrides):
    out = dict(base_flat)
    out.update(overrides)
    return out


def hi_to_ne(text):
    """Adapt Hindi string toward Nepali where used in bulk rules."""
    r = [
        ("गाय", "गाई"), ("गायें", "गाईहरू"), ("ज़", "ज"), ("कृपया", "कृपया"),
        ("है", "छ"), ("हैं", "छन्"), ("हूँ", "छु"), ("हो", "हो"),
        ("करें", "गर्नुहोस्"), ("करो", "गर्नुहोस्"), ("कर", "गर्नुहोस्"),
        ("नहीं", "होइन"), ("नहीं है", "छैन"), ("में", "मा"), ("से", "बाट"),
        ("को", "लाई"), ("की", "को"), ("का", "को"), ("की", "को"),
        ("डैशबोर्ड", "ड्यासबोर्ड"), ("सेटिंग्स", "सेटिङ"), ("ज़िला", "जिल्ला"),
        ("राज्य", "प्रदेश"), ("खोजें", "खोज्नुहोस्"), ("लिखें", "लेख्नुहोस्"),
        ("देखें", "हेर्नुहोस्"), ("चुनें", "छान्नुहोस्"), ("भेजें", "पठाउनुहोस्"),
        ("सेव करें", "सेभ गर्नुहोस्"), ("रद्द करें", "रद्द गर्नुहोस्"),
        ("पुष्टि करें", "पुष्टि गर्नुहोस्"), ("फिर कोशिश करें", "फेरि प्रयास गर्नुहोस्"),
        ("लोड हो रहा है", "लोड हुँदैछ"), ("साइन इन हो रहा है", "साइन इन हुँदैछ"),
        ("खाता बन रहा है", "खाता बन्दैछ"), ("सेव हो रहा है", "सेभ हुँदैछ"),
        ("खोज जारी है", "खोजी जारी छ"), ("चल रहा है", "चलिरहेको छ"),
        ("मिल गया", "फेला पर्यो"), ("उपलब्ध नहीं", "उपलब्ध छैन"),
        ("नमस्ते", "नमस्ते"), ("स्वागत है", "स्वागत छ"),
        ("किसान", "किसान"), ("फार्म", "फार्म"), ("डेयरी", "डेरी"),
        ("पशु चिकित्सक", "पशु चिकित्सक"), ("थनैला", "थन"), ("मास्टाइटिस", "मास्टाइटिस"),
        ("भारतीय", "नेपाली"), ("Indian", "Nepali"),
    ]
    for a, b in r:
        text = text.replace(a, b)
    return text


def adapt_hi_flat(fn):
    hf = flatten(HI)
    return {k: fn(v) if isinstance(v, str) else v for k, v in hf.items()}


def adapt_bn_to_as(flat_bn):
    """Assamese adaptations from Bengali base."""
    out = dict(flat_bn)
    repl = [
        ("য়", "য়"), ("র", "ৰ"), ("ন", "ন"), ("ল", "ল"),
        ("স্বাগতম", "স্বাগত"), ("ড্যাশবোর্ড", "ডেশ্ববৰ্ড"),
        ("সেটিংস", "ছেটিংছ"), ("অ্যাকাউন্ট", "একাউণ্ট"),
        ("খামার", "খেতি"), ("গরু", "গৰু"), ("গরুর", "গৰুৰ"),
        ("জেলা", "জিলা"), ("শহর", "চহৰ"), ("বেছে নিন", "বাছক"),
        ("আপনার", "আপোনাৰ"), ("আপনি", "আপুনি"), ("করুন", "কৰক"),
        ("হচ্ছে", "হৈছে"), ("নেই", "নাই"), ("দেখুন", "চাওক"),
        ("খুঁজুন", "সন্ধান কৰক"), ("লিখুন", "লিখক"), ("পাঠান", "পঠিয়াওক"),
        ("সংরক্ষণ", "সঞ্চয়"), ("বাতিল", "বাতিল"), ("বন্ধ", "বন্ধ"),
        ("সতর্কতা", "সতৰ্কবাৰ্তা"), ("ইতিহাস", "ইতিহাস"),
        ("পশুচিকিৎসক", "পশু চিকিৎসক"), ("মাস্টাইটিস", "মাষ্টাইটিছ"),
        ("দুগ্ধ", "দুগ্ধ"), ("কৃষক", "কৃষক"), ("রিপোর্ট", "প্ৰতিবেদন"),
        ("হোম", "ঘৰ"), ("ভাষা", "ভাষা"),
    ]
    for k, v in out.items():
        if not isinstance(v, str):
            continue
        s = v
        for a, b in repl:
            s = s.replace(a, b)
        out[k] = s
    return out


def adapt_bn_to_mni(flat_bn):
    """Manipuri/Meitei in Bengali script — adapted vocabulary."""
    out = dict(flat_bn)
    repl = [
        ("স্বাগতম", "তꯥꯡꯈꯨꯗꯤ"), ("ড্যাশবোর্ড", "ড্যাশবোর্ড"),
        ("গরু", "ꯁꯥꯡꯕꯣ"), ("গরুর", "ꯁꯥꯡꯕꯣꯒꯤ"), ("গরু", "ꯁꯥꯡꯕꯣ"),
        ("কৃষক", "ꯂꯣꯏꯁꯤꯡ"), ("খামার", "ꯂꯣꯏ"), ("পশুচিকিৎসক", "ꯚꯦꯇꯔꯤꯅꯥꯔꯤ"),
        ("স্বাস্থ্য", "ꯑꯥꯔꯣꯛ"), ("পরীক্ষা", "ꯌꯦꯡꯅꯕ"), ("সেটিংস", "ꯁꯦꯠꯤꯡ"),
        ("ভাষা", "ꯂꯣꯟ"), ("হোম", "ꯌꯨꯝ"), ("লগ আউট", "ꯂꯣꯒ ꯑꯥꯎꯠ"),
        ("অ্যাকাউন্ট", "ꯑꯦꯀꯥꯎꯟꯠ"), ("পাসওয়ার্ড", "ꯄꯥꯁꯋꯥꯔꯗ"),
        ("মোবাইল", "ꯃꯣꯕꯥꯏꯜ"), ("রাজ্য", "ꯁ꯭ꯇꯦꯠ"), ("জেলা", "ꯖꯤꯂꯥ"),
        ("স্ক্যান", "ꯁ꯭ꯀꯥꯟ"), ("চ্যাট", "ꯆꯥꯠ"), ("সতর্কতা", "ꯑꯦꯂꯔꯠ"),
        ("খুঁজুন", "ꯊꯤꯕ"), ("সংরক্ষণ", "ꯁꯦꯚ"), ("বাতিল", "ꯀꯥꯟꯁꯦꯜ"),
        ("লোড হচ্ছে", "ꯂꯣꯗ ꯇꯧꯔꯤ"), ("সফল", "ꯑꯃꯨꯛꯇ"),
    ]
    for k, v in out.items():
        if not isinstance(v, str):
            continue
        s = v
        for a, b in repl:
            s = s.replace(a, b)
        out[k] = s
    # Meitei uses Bengali script per spec — keep mostly Bengali with Meitei terms where marked
    return out


# Import full flat maps from companion module
from locale_maps import LOCALE_MAPS  # noqa: E402


def main():
    hi_f = flatten(HI)
    bn_f = flatten(BN)

    for code, spec in LOCALE_MAPS.items():
        base = spec.get("base", "hi")
        base_flat = bn_f if base == "bn" else hi_f
        if spec.get("adapt") == "ne":
            flat = adapt_hi_flat(hi_to_ne)
        elif spec.get("adapt") == "as":
            flat = adapt_bn_to_as(bn_f)
        elif spec.get("adapt") == "mni":
            flat = adapt_bn_to_mni(bn_f)
        else:
            flat = dict(base_flat)
        flat.update(spec.get("overrides", {}))
        write_locale(code, flat)

    # Patch mr demoMode only
    mr_path = DIR / "mr.json"
    mr = json.loads(mr_path.read_text(encoding="utf-8"))
    mr["demoMode"] = "डेमो मोड"
    mr_path.write_text(json.dumps(mr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched mr.json demoMode")


if __name__ == "__main__":
    main()
