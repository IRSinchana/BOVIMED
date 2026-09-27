import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import {
  fetchMe,
  getToken,
  loginFarmer,
  logoutFarmer,
  registerFarmer,
  setToken,
  updateProfile,
} from '../services/api'
import { useI18n } from '../i18n/I18nContext'
import { STORAGE_KEY, normalizeLocaleCode } from '../i18n/languages'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const { setLang } = useI18n()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  /**
   * Apply profile language only when appropriate.
   * Never override an explicit UI language already chosen in localStorage —
   * Settings / LanguageSelector always win for the live UI.
   */
  const applyUserLang = useCallback(
    (u, { force = false } = {}) => {
      if (!u?.preferred_language) return
      const profileLocale = normalizeLocaleCode(u.preferred_language)
      try {
        if (!force && localStorage.getItem(STORAGE_KEY)) return
      } catch {
        if (!force) return
      }
      setLang(profileLocale)
    },
    [setLang],
  )

  const refresh = useCallback(async () => {
    const token = getToken()
    if (!token) {
      setUser(null)
      setLoading(false)
      return null
    }
    try {
      const me = await fetchMe()
      setUser(me)
      // Do not force language on session restore — respect localStorage choice.
      applyUserLang(me, { force: false })
      return me
    } catch {
      setToken(null)
      setUser(null)
      return null
    } finally {
      setLoading(false)
    }
  }, [applyUserLang])

  useEffect(() => {
    refresh()
    // Intentionally run once on mount — refresh identity is stable enough via applyUserLang.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const login = useCallback(
    async (identifier, password, rememberMe = true) => {
      const data = await loginFarmer({
        identifier,
        password,
        remember_me: rememberMe,
      })
      setToken(data.access_token)
      setUser(data.user)
      // On login, prefer profile language only if user has not already picked one this session.
      applyUserLang(data.user, { force: false })
      return data.user
    },
    [applyUserLang],
  )

  const register = useCallback(
    async (payload) => {
      const data = await registerFarmer(payload)
      setToken(data.access_token)
      setUser(data.user)
      applyUserLang(data.user, { force: true })
      return data.user
    },
    [applyUserLang],
  )

  const logout = useCallback(async () => {
    await logoutFarmer()
    setUser(null)
  }, [])

  const saveProfile = useCallback(
    async (payload) => {
      const updated = await updateProfile(payload)
      setUser(updated)
      // Profile save explicitly includes preferred_language from Settings.
      if (payload?.preferred_language) {
        setLang(normalizeLocaleCode(payload.preferred_language))
      }
      return updated
    },
    [setLang],
  )

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      login,
      register,
      logout,
      refresh,
      saveProfile,
    }),
    [user, loading, login, register, logout, refresh, saveProfile],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
