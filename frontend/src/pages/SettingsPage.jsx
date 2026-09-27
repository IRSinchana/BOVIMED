import { useEffect, useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useI18n } from '../i18n/I18nContext'
import { normalizeLocaleCode } from '../i18n/languages'
import { ErrorMessage } from '../components/Status'
import {
  getApiBase,
  getNotificationPreferences,
  updateNotificationPreferences,
} from '../services/api'
import {
  getBrowserNotificationPermission,
  isBrowserNotificationSupported,
  requestBrowserNotificationPermission,
} from '../utils/notifications'

export default function SettingsPage() {
  const { t, lang, setLang, languages, textDir } = useI18n()
  const { user, saveProfile } = useAuth()
  const { health } = useOutletContext()
  const [form, setForm] = useState({
    full_name: '',
    farm_name: '',
    state: '',
    district: '',
    preferred_language: 'en',
  })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [notifPrefs, setNotifPrefs] = useState({
    health_alerts: true,
    analysis_completed: false,
    veterinary_reminders: true,
    system_notifications: true,
    browser_notifications: false,
  })
  const [notifSaving, setNotifSaving] = useState(false)
  const [notifMessage, setNotifMessage] = useState(null)
  const [notifError, setNotifError] = useState(null)
  const [browserPerm, setBrowserPerm] = useState('default')

  useEffect(() => {
    setBrowserPerm(getBrowserNotificationPermission())
    getNotificationPreferences()
      .then((prefs) => setNotifPrefs(prefs))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!user) return
    setForm({
      full_name: user.full_name || '',
      farm_name: user.farm_name || '',
      state: user.state || '',
      district: user.district || '',
      // Prefer the live UI language so picking a language is not overwritten
      // by a stale preferred_language from the profile until Save.
      preferred_language: lang || user.preferred_language || 'en',
    })
  }, [user]) // eslint-disable-line react-hooks/exhaustive-deps -- sync profile fields only when user loads

  function onPickLanguage(code) {
    setLang(code)
    setForm((prev) => ({ ...prev, preferred_language: code }))
  }

  async function onSaveNotifPrefs(e) {
    e.preventDefault()
    setNotifSaving(true)
    setNotifError(null)
    setNotifMessage(null)
    try {
      const updated = await updateNotificationPreferences(notifPrefs)
      setNotifPrefs(updated)
      setNotifMessage(t.settings.notifSaved)
    } catch (err) {
      setNotifError(err.message || t.common.error)
    } finally {
      setNotifSaving(false)
    }
  }

  async function onEnableBrowserNotifications() {
    setNotifError(null)
    const perm = await requestBrowserNotificationPermission()
    setBrowserPerm(perm)
    if (perm === 'granted') {
      setNotifPrefs((p) => ({ ...p, browser_notifications: true }))
      setNotifMessage(t.settings.browserNotifEnabled)
    } else if (perm === 'denied') {
      setNotifError(t.settings.browserNotifDenied)
    } else if (perm === 'unsupported') {
      setNotifError(t.settings.browserNotifUnsupported)
    }
  }

  async function onSave(e) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    setMessage(null)
    try {
      await saveProfile(form)
      setLang(form.preferred_language || lang)
      setMessage(t.settings.saved)
    } catch (err) {
      setError(err.message || t.common.error)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]" dir={textDir}>
          {t.settings.title}
        </h1>
      </div>

      <section className="rounded-3xl border border-earth bg-white p-5 shadow-sm sm:p-6" dir="ltr">
        <h2 className="font-display text-xl font-semibold text-[#1b4332]" dir={textDir}>
          {t.settings.language}
        </h2>
        <p className="mt-1 text-sm text-[#1b4332]/70" dir={textDir}>
          {t.settings.languageSubtitle}
        </p>
        {/* Language card grid stays LTR so layout never mirrors for RTL languages. */}
        <div className="mt-5 grid gap-3 sm:grid-cols-2" dir="ltr">
          {languages.map((l) => {
            const active = lang === l.code
            return (
              <button
                key={l.code}
                type="button"
                onClick={() => onPickLanguage(l.code)}
                className={`rounded-2xl border px-4 py-3 text-left transition ${
                  active
                    ? 'border-[#1b4332] bg-[#1b4332] text-white'
                    : 'border-earth bg-cream/50 text-[#1b4332] hover:border-[#2d6a4f]'
                }`}
              >
                <p className="font-semibold">{l.native}</p>
                <p className={`text-xs ${active ? 'text-white/80' : 'text-[#1b4332]/60'}`}>
                  {l.englishName || l.label}
                </p>
              </button>
            )
          })}
        </div>
      </section>

      <section className="rounded-3xl border border-earth bg-white p-5 shadow-sm sm:p-6">
        <h2 className="font-display text-xl font-semibold text-[#1b4332]" dir={textDir}>
          {t.settings.notifications}
        </h2>
        <p className="mt-1 text-sm text-[#1b4332]/70" dir={textDir}>
          {t.settings.notificationsSubtitle}
        </p>
        <form onSubmit={onSaveNotifPrefs} className="mt-4 space-y-3">
          {[
            ['health_alerts', t.settings.notifHealthAlerts],
            ['analysis_completed', t.settings.notifAnalysisCompleted],
            ['veterinary_reminders', t.settings.notifVeterinary],
            ['system_notifications', t.settings.notifSystem],
          ].map(([key, label]) => (
            <label key={key} className="flex items-center justify-between gap-3 rounded-xl border border-earth px-4 py-3">
              <span className="text-sm font-medium" dir={textDir}>{label}</span>
              <input
                type="checkbox"
                checked={Boolean(notifPrefs[key])}
                onChange={(e) => setNotifPrefs((p) => ({ ...p, [key]: e.target.checked }))}
              />
            </label>
          ))}
          <div className="rounded-xl border border-earth px-4 py-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <span className="text-sm font-medium" dir={textDir}>{t.settings.notifBrowser}</span>
              <input
                type="checkbox"
                checked={Boolean(notifPrefs.browser_notifications)}
                onChange={(e) =>
                  setNotifPrefs((p) => ({ ...p, browser_notifications: e.target.checked }))
                }
              />
            </div>
            {isBrowserNotificationSupported() ? (
              <button
                type="button"
                onClick={onEnableBrowserNotifications}
                className="mt-3 rounded-xl border border-[#2d6a4f] px-3 py-2 text-xs font-semibold text-[#2d6a4f]"
              >
                {t.settings.enableBrowserNotifications}
              </button>
            ) : (
              <p className="mt-2 text-xs text-[#1b4332]/65" dir={textDir}>
                {t.settings.browserNotifUnsupported}
              </p>
            )}
            {browserPerm === 'denied' ? (
              <p className="mt-2 text-xs text-amber-800" dir={textDir}>{t.settings.browserNotifDenied}</p>
            ) : null}
          </div>
          <ErrorMessage message={notifError} />
          {notifMessage ? <p className="text-sm font-medium text-[#2d6a4f]">{notifMessage}</p> : null}
          <button
            type="submit"
            disabled={notifSaving}
            className="rounded-2xl bg-[#1b4332] px-5 py-3 text-sm font-semibold text-white disabled:opacity-60"
          >
            {notifSaving ? t.settings.saving : t.settings.saveNotifications}
          </button>
        </form>
      </section>

      <section className="rounded-3xl border border-earth bg-white p-5 shadow-sm sm:p-6">
        <h2 className="font-display text-xl font-semibold text-[#1b4332]">
          {t.settings.profile}
        </h2>
        <form onSubmit={onSave} className="mt-4 grid gap-4 sm:grid-cols-2">
          <label className="block sm:col-span-2">
            <span className="mb-1.5 block text-sm font-medium">{t.settings.name}</span>
            <input
              value={form.full_name}
              onChange={(e) => setForm((p) => ({ ...p, full_name: e.target.value }))}
              className="w-full rounded-xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
              required
            />
          </label>
          <label className="block sm:col-span-2">
            <span className="mb-1.5 block text-sm font-medium">{t.settings.mobile}</span>
            <input
              value={user?.mobile || ''}
              disabled
              className="w-full rounded-xl border border-earth bg-cream px-4 py-3 text-[#1b4332]/70"
            />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">{t.settings.farmName}</span>
            <input
              value={form.farm_name}
              onChange={(e) => setForm((p) => ({ ...p, farm_name: e.target.value }))}
              className="w-full rounded-xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
            />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">{t.settings.state}</span>
            <input
              value={form.state}
              onChange={(e) => setForm((p) => ({ ...p, state: e.target.value }))}
              className="w-full rounded-xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
            />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">{t.settings.district}</span>
            <input
              value={form.district}
              onChange={(e) => setForm((p) => ({ ...p, district: e.target.value }))}
              className="w-full rounded-xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
            />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">
              {t.settings.preferredLanguage}
            </span>
            <select
              value={form.preferred_language}
              onChange={(e) => {
                const locale = normalizeLocaleCode(e.target.value)
                setForm((p) => ({ ...p, preferred_language: locale }))
                setLang(locale)
              }}
              className="w-full rounded-xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
            >
              {languages.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.native} — {l.label}
                </option>
              ))}
            </select>
          </label>

          <div className="sm:col-span-2">
            <ErrorMessage message={error} />
            {message ? (
              <p className="mb-3 text-sm font-medium text-[#2d6a4f]">{message}</p>
            ) : null}
            <button
              type="submit"
              disabled={saving}
              className="rounded-2xl bg-[#1b4332] px-5 py-3 text-sm font-semibold text-white disabled:opacity-60"
            >
              {saving ? t.settings.saving : t.settings.save}
            </button>
          </div>
        </form>
      </section>

      <section className="rounded-2xl border border-earth bg-white p-5 text-sm shadow-sm">
        <p className="font-semibold text-[#1b4332]">{t.settings.api}</p>
        <p className="mt-2 break-all text-[#1b4332]/70">{getApiBase()}</p>
        <p className="mt-2">
          demo_mode: {health ? String(health.demo_mode) : '—'} · model_loaded:{' '}
          {health ? String(health.model_loaded) : '—'}
        </p>
      </section>
    </div>
  )
}
