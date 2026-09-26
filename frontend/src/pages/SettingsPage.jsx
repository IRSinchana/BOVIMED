import { useEffect, useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from '../components/Status'
import { getApiBase } from '../services/api'

export default function SettingsPage() {
  const { t, lang, setLang, languages } = useI18n()
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
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.settings.title}</h1>
      </div>

      <section className="rounded-3xl border border-earth bg-white p-5 shadow-sm sm:p-6">
        <h2 className="font-display text-xl font-semibold text-[#1b4332]">
          {t.settings.language}
        </h2>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.settings.languageSubtitle}</p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
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
                  {l.label}
                </p>
              </button>
            )
          })}
        </div>
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
                const code = e.target.value
                setForm((p) => ({ ...p, preferred_language: code }))
                setLang(code)
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
