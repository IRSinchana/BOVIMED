/**
 * Canonical BOVIMED language configuration — single source of truth.
 * All selectors and locale resolution must use these stable ISO-style codes.
 */

export const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English', label: 'English', native: 'English', englishName: 'English', direction: 'ltr' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', label: 'Hindi', native: 'हिन्दी', englishName: 'Hindi', direction: 'ltr' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', label: 'Kannada', native: 'ಕನ್ನಡ', englishName: 'Kannada', direction: 'ltr' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', label: 'Telugu', native: 'తెలుగు', englishName: 'Telugu', direction: 'ltr' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', label: 'Tamil', native: 'தமிழ்', englishName: 'Tamil', direction: 'ltr' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം', label: 'Malayalam', native: 'മലയാളം', englishName: 'Malayalam', direction: 'ltr' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', label: 'Marathi', native: 'मराठी', englishName: 'Marathi', direction: 'ltr' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', label: 'Bengali', native: 'বাংলা', englishName: 'Bengali', direction: 'ltr' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', label: 'Gujarati', native: 'ગુજરાતી', englishName: 'Gujarati', direction: 'ltr' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', label: 'Punjabi', native: 'ਪੰਜਾਬੀ', englishName: 'Punjabi', direction: 'ltr' },
  { code: 'or', name: 'Odia', nativeName: 'ଓଡ଼ିଆ', label: 'Odia', native: 'ଓଡ଼ିଆ', englishName: 'Odia', direction: 'ltr' },
  { code: 'as', name: 'Assamese', nativeName: 'অসমীয়া', label: 'Assamese', native: 'অসমীয়া', englishName: 'Assamese', direction: 'ltr' },
  { code: 'ur', name: 'Urdu', nativeName: 'اردو', label: 'Urdu', native: 'اردو', englishName: 'Urdu', direction: 'rtl' },
  { code: 'sa', name: 'Sanskrit', nativeName: 'संस्कृतम्', label: 'Sanskrit', native: 'संस्कृतम्', englishName: 'Sanskrit', direction: 'ltr' },
  { code: 'sd', name: 'Sindhi', nativeName: 'سنڌي', label: 'Sindhi', native: 'سنڌي', englishName: 'Sindhi', direction: 'rtl' },
  { code: 'ks', name: 'Kashmiri', nativeName: 'کٲشُر', label: 'Kashmiri', native: 'کٲشُر', englishName: 'Kashmiri', direction: 'rtl' },
  { code: 'ne', name: 'Nepali', nativeName: 'नेपाली', label: 'Nepali', native: 'नेपाली', englishName: 'Nepali', direction: 'ltr' },
  { code: 'kok', name: 'Konkani', nativeName: 'कोंकणी', label: 'Konkani', native: 'कोंकणी', englishName: 'Konkani', direction: 'ltr' },
  { code: 'mai', name: 'Maithili', nativeName: 'मैथिली', label: 'Maithili', native: 'मैथिली', englishName: 'Maithili', direction: 'ltr' },
  { code: 'doi', name: 'Dogri', nativeName: 'डोगरी', label: 'Dogri', native: 'डोगरी', englishName: 'Dogri', direction: 'ltr' },
  { code: 'mni', name: 'Manipuri', nativeName: 'মৈতৈলোন্', label: 'Manipuri', native: 'মৈতৈলোন্', englishName: 'Manipuri', direction: 'ltr' },
  { code: 'sat', name: 'Santhali', nativeName: 'ᱥᱟᱱᱛᱟᱲᱤ', label: 'Santhali', native: 'ᱥᱟᱱᱛᱟᱲᱤ', englishName: 'Santhali', direction: 'ltr' },
  { code: 'brx', name: 'Bodo', nativeName: 'बड़ो', label: 'Bodo', native: 'बड़ो', englishName: 'Bodo', direction: 'ltr' },
]

/** Legacy / alternate codes → canonical locale file codes. */
export const LOCALE_ALIASES = {
  bo: 'brx',
}

export const SUPPORTED_LOCALE_CODES = new Set(LANGUAGES.map((l) => l.code))

export const RTL_LANGS = new Set(
  LANGUAGES.filter((l) => l.direction === 'rtl').map((l) => l.code),
)

export const STORAGE_KEY = 'bovimed:lang'

export function readStoredLocale() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) return normalizeLocaleCode(stored)
  } catch {
    // ignore
  }
  return null
}

/** Map any input to a supported locale code; unknown codes fall back to English. */
export function normalizeLocaleCode(code) {
  const raw = String(code || 'en').split('-')[0].toLowerCase()
  const mapped = LOCALE_ALIASES[raw] || raw
  return SUPPORTED_LOCALE_CODES.has(mapped) ? mapped : 'en'
}
