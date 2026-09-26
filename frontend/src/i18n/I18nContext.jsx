import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import i18n, { LANGUAGE_OPTIONS, RTL_LANGS, applyDocumentDirection } from './index'

const I18nContext = createContext(null)
const STORAGE_KEY = 'bovimed:lang'

function readStoredLang() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) return stored.split('-')[0].toLowerCase()
  } catch {
    // ignore
  }
  return null
}

/** Plain nested dictionary for the active language (rebuilt on each language change). */
function resolveDictionary(langCode) {
  const code = (langCode || 'en').split('-')[0].toLowerCase()
  const enBundle = i18n.getResourceBundle('en', 'translation') || {}
  const active = i18n.getResourceBundle(code, 'translation')
  // Active bundle is already deep-merged with English at init time.
  return active && typeof active === 'object' ? active : enBundle
}

export function I18nProvider({ children }) {
  const { i18n: i18nHook, ready } = useTranslation()
  const [lang, setLangState] = useState(() => {
    return (
      readStoredLang() ||
      (i18nHook.language || 'en').split('-')[0].toLowerCase()
    )
  })

  const setLang = useCallback((code) => {
    const c = (code || 'en').split('-')[0].toLowerCase()
    setLangState(c)
    applyDocumentDirection(c)
    try {
      localStorage.setItem(STORAGE_KEY, c)
    } catch {
      // ignore
    }
    if (i18n.language !== c) {
      void i18n.changeLanguage(c)
    }
  }, [])

  useEffect(() => {
    const onChange = (lng) => {
      const code = (lng || 'en').split('-')[0].toLowerCase()
      setLangState((prev) => (prev === code ? prev : code))
      applyDocumentDirection(code)
      try {
        localStorage.setItem(STORAGE_KEY, code)
      } catch {
        // ignore
      }
    }
    i18nHook.on('languageChanged', onChange)
    // Sync initial language from storage → i18n
    const stored = readStoredLang()
    if (stored && i18nHook.language !== stored) {
      void i18nHook.changeLanguage(stored)
    } else {
      applyDocumentDirection(i18nHook.language || stored || 'en')
    }
    return () => i18nHook.off('languageChanged', onChange)
  }, [i18nHook])

  const value = useMemo(() => {
    const activeLang = (lang || 'en').split('-')[0].toLowerCase()
    return {
      lang: activeLang,
      isRTL: RTL_LANGS.has(activeLang),
      setLang,
      t: resolveDictionary(activeLang),
      languages: LANGUAGE_OPTIONS,
      i18n,
      ready,
    }
  }, [lang, setLang, ready])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n() {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error('useI18n must be used within I18nProvider')
  return ctx
}
