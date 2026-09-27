import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import {
  LANGUAGES,
  RTL_LANGS,
  STORAGE_KEY,
  normalizeLocaleCode,
  readStoredLocale,
} from './languages'

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
import sat from './locales/sat.json'

/** Canonical language list — imported from languages.js (single source of truth). */
export const LANGUAGE_OPTIONS = LANGUAGES
export { LANGUAGES, RTL_LANGS, normalizeLocaleCode, readStoredLocale, STORAGE_KEY }

function flatten(obj, prefix = '') {
  const out = {}
  for (const [k, v] of Object.entries(obj || {})) {
    const key = prefix ? `${prefix}.${k}` : k
    if (v && typeof v === 'object' && !Array.isArray(v)) Object.assign(out, flatten(v, key))
    else out[key] = v
  }
  return out
}

export const LOCALE_BUNDLES = {
  en,
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
  sat,
}

/**
 * Dev helper: detect missing keys so they do not silently become English.
 * Call validateTranslationCoverage() from the browser console or during boot in DEV.
 */
export function validateTranslationCoverage() {
  const enFlat = flatten(en)
  const report = {}
  for (const [code, dict] of Object.entries(LOCALE_BUNDLES)) {
    if (code === 'en') continue
    const flat = flatten(dict)
    const missing = Object.keys(enFlat).filter((k) => !(k in flat) || flat[k] === '' || flat[k] == null)
    report[code] = { missingCount: missing.length, missing: missing.slice(0, 40) }
    if (missing.length && typeof console !== 'undefined') {
      console.warn(`[BOVIMED i18n] ${code}: ${missing.length} missing keys`, missing.slice(0, 12))
    }
  }
  return report
}

const resources = {}
for (const [code, dict] of Object.entries(LOCALE_BUNDLES)) {
  // Full dictionaries — every locale must ship the same keys as English.
  resources[code] = { translation: dict }
}

const initialLocale = readStoredLocale() || 'en'

void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    lng: initialLocale,
    // Safety net only; supported locales are expected to be complete.
    // Missing keys are surfaced by validateTranslationCoverage() in DEV.
    fallbackLng: 'en',
    supportedLngs: LANGUAGE_OPTIONS.map((l) => l.code),
    nonExplicitSupportedLngs: false,
    load: 'languageOnly',
    interpolation: { escapeValue: false },
    detection: {
      order: ['localStorage'],
      lookupLocalStorage: STORAGE_KEY,
      caches: ['localStorage'],
    },
    returnNull: false,
    returnEmptyString: false,
    parseMissingKeyHandler: (key) => {
      if (import.meta.env?.DEV) {
        console.warn(`[BOVIMED i18n] missing key: ${key}`)
      }
      return key
    },
    keySeparator: '.',
    nsSeparator: false,
  })

/**
 * Keep the APPLICATION SHELL always LTR.
 * Only set lang= for accessibility / fonts. Never flip document.dir.
 */
export function applyDocumentLanguage(lang) {
  const code = normalizeLocaleCode(lang)
  document.documentElement.lang = code
  document.documentElement.dir = 'ltr'
  document.documentElement.dataset.textDir = RTL_LANGS.has(code) ? 'rtl' : 'ltr'
  if (RTL_LANGS.has(code)) {
    document.documentElement.classList.add('bovimed-rtl-text')
  } else {
    document.documentElement.classList.remove('bovimed-rtl-text')
  }
}

/** @deprecated use applyDocumentLanguage — kept so older imports do not break */
export function applyDocumentDirection(lang) {
  applyDocumentLanguage(lang)
}

i18n.on('languageChanged', applyDocumentLanguage)
applyDocumentLanguage(i18n.language || 'en')

if (import.meta.env?.DEV) {
  validateTranslationCoverage()
}

/** Read a nested path from the English structure (for Proxy shape). */
export function getEnglishPath(path) {
  if (!path) return en
  const parts = path.split('.')
  let cur = en
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object') return undefined
    cur = cur[p]
  }
  return cur
}

export { en as ENGLISH_DICTIONARY }
export default i18n
