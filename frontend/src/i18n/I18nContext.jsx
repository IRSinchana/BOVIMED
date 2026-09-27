import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import i18n, {
  ENGLISH_DICTIONARY,
  LANGUAGE_OPTIONS,
  LOCALE_BUNDLES,
  RTL_LANGS,
  applyDocumentLanguage,
  getEnglishPath,
  normalizeLocaleCode,
  readStoredLocale,
  STORAGE_KEY,
} from './index'

const I18nContext = createContext(null)

function getPath(obj, path) {
  const parts = path.split('.')
  let cur = obj
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object') return undefined
    cur = cur[p]
  }
  return cur
}

/**
 * Nested dictionary for `t.nav.dashboard` usage.
 * Resolves from the active locale bundle first.
 * Falls back to English only — never to another Indian language.
 */
function buildNestedDictionary(langCode) {
  const code = normalizeLocaleCode(langCode)
  const bundle = LOCALE_BUNDLES[code] || LOCALE_BUNDLES.en || ENGLISH_DICTIONARY
  const enBundle = LOCALE_BUNDLES.en || ENGLISH_DICTIONARY

  function createNode(prefix) {
    return new Proxy(
      {},
      {
        get(_target, prop) {
          if (prop === Symbol.toStringTag) return 'TranslationDictionary'
          if (typeof prop !== 'string') return undefined

          const path = prefix ? `${prefix}.${prop}` : prop
          const shape = getEnglishPath(path)

          if (shape && typeof shape === 'object' && !Array.isArray(shape)) {
            return createNode(path)
          }

          const activeVal = getPath(bundle, path)
          if (activeVal !== undefined && activeVal !== null && activeVal !== '') {
            return activeVal
          }

          if (import.meta.env?.DEV && code !== 'en') {
            console.warn(`[BOVIMED i18n] missing "${path}" in locale "${code}"`)
          }

          const enVal = getPath(enBundle, path)
          return enVal !== undefined ? enVal : path
        },
      },
    )
  }

  return createNode('')
}

export function I18nProvider({ children }) {
  const { i18n: i18nHook, ready } = useTranslation()
  const [lang, setLangState] = useState(() => readStoredLocale() || 'en')
  const [revision, setRevision] = useState(0)

  const setLang = useCallback((code) => {
    const normalized = normalizeLocaleCode(code)
    setLangState(normalized)
    setRevision((r) => r + 1)
    applyDocumentLanguage(normalized)
    try {
      localStorage.setItem(STORAGE_KEY, normalized)
    } catch {
      // ignore
    }
    void i18n.changeLanguage(normalized)
  }, [])

  useEffect(() => {
    const onChange = (lng) => {
      const code = normalizeLocaleCode(lng)
      setLangState((prev) => {
        if (prev === code) return prev
        setRevision((r) => r + 1)
        return code
      })
      applyDocumentLanguage(code)
      try {
        localStorage.setItem(STORAGE_KEY, code)
      } catch {
        // ignore
      }
    }
    i18nHook.on('languageChanged', onChange)
    const stored = readStoredLocale()
    if (stored && normalizeLocaleCode(i18nHook.language) !== stored) {
      void i18nHook.changeLanguage(stored)
    } else {
      applyDocumentLanguage(stored || i18nHook.language || 'en')
    }
    return () => i18nHook.off('languageChanged', onChange)
  }, [i18nHook])

  const value = useMemo(() => {
    const activeLang = normalizeLocaleCode(lang)
    const isRTL = RTL_LANGS.has(activeLang)
    const meta = LANGUAGE_OPTIONS.find((l) => l.code === activeLang)
    return {
      lang: activeLang,
      isRTL,
      /** Text-level direction only — never flips the app shell. */
      textDir: isRTL ? 'rtl' : 'ltr',
      direction: meta?.direction || (isRTL ? 'rtl' : 'ltr'),
      setLang,
      t: buildNestedDictionary(activeLang),
      languages: LANGUAGE_OPTIONS,
      i18n,
      ready,
      revision,
    }
  }, [lang, setLang, ready, revision])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n() {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error('useI18n must be used within I18nProvider')
  return ctx
}
