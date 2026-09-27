import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useI18n } from '../i18n/I18nContext'
import { BrandMark } from '../components/AiModeBadge'
import LanguageSelector from '../components/LanguageSelector'
import { ErrorMessage } from '../components/Status'

export default function LoginPage() {
  const { t, textDir } = useI18n()
  const { login, isAuthenticated, loading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(true)
  const [showPw, setShowPw] = useState(false)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [forgotOpen, setForgotOpen] = useState(false)

  if (!loading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await login(identifier, password, remember)
      navigate(location.state?.from || '/dashboard', { replace: true })
    } catch (err) {
      if (err.isNetworkError) setError(t.common.backendDown)
      else setError(err.message || t.common.error)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-2" dir={textDir}>
      <section className="relative hidden overflow-hidden lg:block">
        <img src="/farm-hero.svg" alt="" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-[#1b4332]/65" />
        <div className="relative z-10 flex h-full flex-col justify-between p-10 text-white">
          <BrandMark to="/login" light />
          <div>
            <p className="font-display text-sm font-semibold tracking-[0.2em] uppercase opacity-90">
              BOVIMED
            </p>
            <h1 className="mt-3 max-w-md font-display text-4xl font-bold leading-tight">
              {t.tagline}
            </h1>
            <p className="mt-4 max-w-md text-base text-white/85">{t.shortDesc}</p>
          </div>
          <p className="max-w-sm text-xs text-white/70">{t.disclaimer}</p>
        </div>
      </section>

      <section className="relative flex items-center justify-center bg-cream px-4 py-10">
        <div
          className="pointer-events-none absolute inset-0 opacity-20 lg:hidden"
          style={{
            backgroundImage: 'url(/farm-hero.svg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <div className="relative z-10 w-full max-w-md rounded-3xl border border-earth bg-white/95 p-6 shadow-lg sm:p-8">
          <div className="mb-6 flex items-center justify-between">
            <BrandMark to="/login" />
            <LanguageSelector compact />
          </div>
          <h2 className="font-display text-2xl font-bold text-[#1b4332]">{t.auth.loginTitle}</h2>
          <p className="mt-1 text-sm text-[#1b4332]/70">{t.auth.loginSubtitle}</p>

          <form onSubmit={onSubmit} className="mt-6 space-y-4">
            <label className="block">
              <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">
                {t.auth.identifier}
              </span>
              <input
                required
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                className="w-full rounded-xl border border-earth bg-white px-4 py-3 text-base text-[#1b4332] outline-none focus:border-[#2d6a4f]"
                autoComplete="username"
              />
            </label>

            <label className="block">
              <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">
                {t.auth.password}
              </span>
              <div className="relative">
                <input
                  required
                  type={showPw ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-xl border border-earth bg-white px-4 py-3 pr-12 text-base text-[#1b4332] outline-none focus:border-[#2d6a4f]"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#1b4332]/70"
                  onClick={() => setShowPw((v) => !v)}
                  aria-label={showPw ? t.auth.hidePassword : t.auth.showPassword}
                >
                  {showPw ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </label>

            <div className="flex items-center justify-between gap-3 text-sm">
              <label className="flex items-center gap-2 text-[#1b4332]">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                />
                {t.auth.rememberMe}
              </label>
              <button
                type="button"
                className="font-medium text-[#2d6a4f] underline"
                onClick={() => setForgotOpen(true)}
              >
                {t.auth.forgot}
              </button>
            </div>

            <ErrorMessage message={error} />

            <button
              type="submit"
              disabled={submitting}
              className="w-full rounded-2xl bg-[#1b4332] px-5 py-3.5 text-base font-semibold text-white disabled:opacity-60"
            >
              {submitting ? t.auth.loggingIn : t.auth.login}
            </button>
          </form>

          {forgotOpen ? (
            <p className="mt-4 rounded-xl bg-cream px-3 py-2 text-xs text-[#1b4332]/80">
              {t.auth.forgotHint}
            </p>
          ) : null}

          <p className="mt-6 text-center text-sm text-[#1b4332]/80">
            {t.auth.noAccount}{' '}
            <Link to="/register" className="font-semibold text-[#2d6a4f] underline">
              {t.auth.createAccount}
            </Link>
          </p>
        </div>
      </section>
    </div>
  )
}
