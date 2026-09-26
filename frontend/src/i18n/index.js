import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import en from './locales/en.json'
import hi from './locales/hi.json'
import kn from './locales/kn.json'
import te from './locales/te.json'
import ta from './locales/ta.json'
import ml from './locales/ml.json'
import mr from './locales/mr.json'
import bn from './locales/bn.json'
import gu from './locales/gu.json'
import pa from './locales/pa.json'
import or from './locales/or.json'
import as from './locales/as.json'
import ur from './locales/ur.json'
import ks from './locales/ks.json'
import kok from './locales/kok.json'
import ne from './locales/ne.json'
import sd from './locales/sd.json'
import sa from './locales/sa.json'
import brx from './locales/brx.json'
import doi from './locales/doi.json'
import mai from './locales/mai.json'
import mni from './locales/mni.json'

export const LANGUAGE_OPTIONS = [
  { code: 'en', label: 'English', native: 'English' },
  { code: 'hi', label: 'Hindi', native: 'हिन्दी' },
  { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'te', label: 'Telugu', native: 'తెలుగు' },
  { code: 'ta', label: 'Tamil', native: 'தமிழ்' },
  { code: 'ml', label: 'Malayalam', native: 'മലയാളം' },
  { code: 'mr', label: 'Marathi', native: 'मराठी' },
  { code: 'bn', label: 'Bengali', native: 'বাংলা' },
  { code: 'gu', label: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'pa', label: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'or', label: 'Odia', native: 'ଓଡ଼ିଆ' },
  { code: 'as', label: 'Assamese', native: 'অসমীয়া' },
  { code: 'ur', label: 'Urdu', native: 'اردو' },
  { code: 'ks', label: 'Kashmiri', native: 'کٲشُر' },
  { code: 'kok', label: 'Konkani', native: 'कोंकणी' },
  { code: 'ne', label: 'Nepali', native: 'नेपाली' },
  { code: 'sd', label: 'Sindhi', native: 'سنڌي' },
  { code: 'sa', label: 'Sanskrit', native: 'संस्कृतम्' },
  { code: 'brx', label: 'Bodo', native: 'बड़ो' },
  { code: 'doi', label: 'Dogri', native: 'डोगरी' },
  { code: 'mai', label: 'Maithili', native: 'मैथिली' },
  { code: 'mni', label: 'Manipuri', native: 'মৈতৈলোন্' },
]

export const RTL_LANGS = new Set(['ur', 'sd', 'ks'])

/** Deep-merge overlay onto base so missing keys honestly fall back to English. */
function deepMerge(base, overlay) {
  if (!overlay || typeof overlay !== 'object' || Array.isArray(overlay)) {
    return overlay === undefined ? base : overlay
  }
  const out = { ...base }
  for (const [k, v] of Object.entries(overlay)) {
    if (
      v &&
      typeof v === 'object' &&
      !Array.isArray(v) &&
      base?.[k] &&
      typeof base[k] === 'object' &&
      !Array.isArray(base[k])
    ) {
      out[k] = deepMerge(base[k], v)
    } else if (v !== undefined && v !== null && v !== '') {
      out[k] = v
    }
  }
  return out
}

const overlays = {
  hi,
  kn,
  te,
  ta,
  ml,
  mr,
  bn,
  gu,
  pa,
  or,
  as,
  ur,
  ks,
  kok,
  ne,
  sd,
  sa,
  brx,
  doi,
  mai,
  mni,
}

const resources = {
  en: { translation: en },
}

for (const [code, overlay] of Object.entries(overlays)) {
  resources[code] = { translation: deepMerge(en, overlay) }
}

void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    supportedLngs: LANGUAGE_OPTIONS.map((l) => l.code),
    nonExplicitSupportedLngs: true,
    load: 'languageOnly',
    interpolation: { escapeValue: false },
    detection: {
      order: ['localStorage', 'navigator'],
      lookupLocalStorage: 'bovimed:lang',
      caches: ['localStorage'],
    },
    returnNull: false,
    returnEmptyString: false,
    keySeparator: '.',
    nsSeparator: false,
  })

export function applyDocumentDirection(lang) {
  const code = (lang || 'en').split('-')[0].toLowerCase()
  const rtl = RTL_LANGS.has(code)
  document.documentElement.lang = code
  document.documentElement.dir = rtl ? 'rtl' : 'ltr'
}

i18n.on('languageChanged', applyDocumentDirection)
applyDocumentDirection(i18n.language || 'en')

export default i18n
