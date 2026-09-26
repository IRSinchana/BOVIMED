import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useI18n } from '../i18n/I18nContext'
import { BrandMark } from '../components/AiModeBadge'
import LanguageSelector from '../components/LanguageSelector'
import { ErrorMessage } from '../components/Status'

export default function RegisterPage() {
  const { t } = useI18n()
  const { register, isAuthenticated, loading } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    full_name: '',
    mobile: '',
    email: '',
    password: '',
    confirm_password: '',
    farm_name: '',
    state: '',
    district: '',
  })
  const [showPw, setShowPw] = useState(false)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  if (!loading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  function setField(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    if (form.password !== form.confirm_password) {
      setError('Password and confirm password do not match.')
      return
    }
    setSubmitting(true)
    try {
      await register({
        ...form,
        email: form.email || null,
      })
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err.message || t.common.error)
    } finally {
      setSubmitting(false)
    }
  }

  const fields = [
    ['full_name', t.auth.fullName, 'text', true],
    ['mobile', t.auth.mobile, 'tel', true],
    ['email', t.auth.email, 'email', false],
    ['farm_name', t.auth.farmName, 'text', false],
    ['state', t.auth.state, 'text', false],
    ['district', t.auth.district, 'text', false],
  ]

  return (
    <div className="min-h-screen bg-cream px-4 py-8">
      <div className="mx-auto max-w-xl rounded-3xl border border-earth bg-white p-6 shadow-lg sm:p-8">
        <div className="flex items-center justify-between">
          <BrandMark to="/login" />
          <LanguageSelector compact />
        </div>
        <h1 className="mt-6 font-display text-2xl font-bold text-[#1b4332]">
          {t.auth.registerTitle}
        </h1>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.auth.registerSubtitle}</p>

        <form onSubmit={onSubmit} className="mt-6 grid gap-4 sm:grid-cols-2">
          {fields.map(([key, label, type, required]) => (
            <label key={key} className={`block ${key === 'email' || key === 'full_name' ? 'sm:col-span-2' : ''}`}>
              <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">{label}</span>
              <input
                required={required}
                type={type}
                value={form[key]}
                onChange={(e) => setField(key, e.target.value)}
                className="w-full rounded-xl border border-earth px-4 py-3 text-base text-[#1b4332] outline-none focus:border-[#2d6a4f]"
              />
            </label>
          ))}

          <label className="block sm:col-span-2">
            <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">
              {t.auth.password}
            </span>
            <div className="relative">
              <input
                required
                type={showPw ? 'text' : 'password'}
                value={form.password}
                onChange={(e) => setField('password', e.target.value)}
                className="w-full rounded-xl border border-earth px-4 py-3 pr-12 text-base outline-none focus:border-[#2d6a4f]"
                minLength={6}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#1b4332]/70"
                onClick={() => setShowPw((v) => !v)}
              >
                {showPw ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </label>

          <label className="block sm:col-span-2">
            <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">
              {t.auth.confirmPassword}
            </span>
            <input
              required
              type={showPw ? 'text' : 'password'}
              value={form.confirm_password}
              onChange={(e) => setField('confirm_password', e.target.value)}
              className="w-full rounded-xl border border-earth px-4 py-3 text-base outline-none focus:border-[#2d6a4f]"
              minLength={6}
            />
          </label>

          <div className="sm:col-span-2">
            <ErrorMessage message={error} />
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="sm:col-span-2 w-full rounded-2xl bg-[#1b4332] px-5 py-3.5 text-base font-semibold text-white disabled:opacity-60"
          >
            {submitting ? t.auth.registering : t.auth.register}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-[#1b4332]/80">
          {t.auth.hasAccount}{' '}
          <Link to="/login" className="font-semibold text-[#2d6a4f] underline">
            {t.auth.login}
          </Link>
        </p>
      </div>
    </div>
  )
}
