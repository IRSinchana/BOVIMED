import { useEffect, useState } from 'react'
import { Link, useOutletContext } from 'react-router-dom'
import {
  AlertTriangle,
  Activity,
  Camera,
  HeartPulse,
  MessageCircle,
  ScanLine,
  Stethoscope,
  Users,
} from 'lucide-react'
import AiModeBadge from '../components/AiModeBadge'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { getDashboard, getHealth, listAlerts } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

function riskLabel(t, risk) {
  const level = normalizeRiskLevel(risk)
  return t.risk?.[level] || level
}

export default function DashboardPage() {
  const { t, lang } = useI18n()
  const { health, setHealth } = useOutletContext()
  const [data, setData] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    Promise.all([getDashboard(), getHealth(), listAlerts()])
      .then(([dash, h, al]) => {
        if (cancelled) return
        setData(dash)
        setHealth?.(h)
        setAlerts(Array.isArray(al) ? al.slice(0, 3) : [])
      })
      .catch((e) => {
        if (!cancelled) setError(e.message || t.common.backendDown)
      })
    return () => {
      cancelled = true
    }
  }, [setHealth, t.common.backendDown])

  const cards = [
    { label: t.dashboard.totalCows, value: data?.total_cows ?? '—', icon: Users },
    { label: t.dashboard.healthy, value: data?.healthy ?? '—', icon: HeartPulse },
    { label: t.dashboard.atRisk, value: data?.at_risk ?? '—', icon: AlertTriangle },
    {
      label: t.dashboard.analysesMonth,
      value: data?.analyses_this_month ?? '—',
      icon: Activity,
    },
  ]

  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-3xl border border-earth bg-[#1b4332] text-white shadow-sm">
        <img src="/farm-hero.svg" alt="" className="absolute inset-0 h-full w-full object-cover opacity-25" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#1b4332] via-[#1b4332]/90 to-[#1b4332]/55" />
        <div className="relative z-10 p-6 sm:p-8">
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <AiModeBadge health={health || { demo_mode: false }} />
            <span className="rounded-full border border-white/30 bg-white/10 px-3 py-1 text-xs font-semibold">
              {t.langIndicator}: {lang.toUpperCase()}
            </span>
          </div>
          <h1 className="font-display text-3xl font-bold sm:text-4xl">{t.dashboard.welcome}</h1>
          <p className="mt-2 max-w-xl text-base text-white/85">{t.dashboard.subtitle}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/analyze" className="inline-flex items-center gap-2 rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-[#1b4332]">
              <ScanLine className="h-4 w-4" />{t.dashboard.analyzeCta}
            </Link>
            <Link to="/camera" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white">
              <Camera className="h-4 w-4" />{t.dashboard.cameraCta}
            </Link>
            <Link to="/chat" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white">
              <MessageCircle className="h-4 w-4" />{t.dashboard.askCta}
            </Link>
            <Link to="/veterinarians" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white">
              <Stethoscope className="h-4 w-4" />{t.dashboard.vetCta}
            </Link>
          </div>
        </div>
      </section>

      <ErrorMessage message={error} />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-2xl border border-earth bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <p className="text-sm text-[#1b4332]/60">{label}</p>
              <Icon className="h-5 w-5 text-[#2d6a4f]" />
            </div>
            <p className="mt-3 font-display text-3xl font-bold text-[#1b4332]">{value}</p>
          </div>
        ))}
      </div>

      {alerts.length > 0 ? (
        <section className="space-y-3">
          <h2 className="font-display text-lg font-semibold">{t.dashboard.recentAlerts}</h2>
          {alerts.map((a) => {
            const level = normalizeRiskLevel(a.risk_level)
            return (
              <div key={a.id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3">
                <div>
                  <RiskBadge risk={level} label={riskLabel(t, level)} />
                  <p className="mt-1 text-sm font-semibold">{a.cow_id} · {a.prediction || a.title}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Link to="/alerts" className="rounded-xl bg-[#1b4332] px-3 py-2 text-xs font-semibold text-white">{t.dashboard.viewAlert}</Link>
                  <Link to="/veterinarians" className="rounded-xl border border-earth bg-white px-3 py-2 text-xs font-semibold">{t.dashboard.findVet}</Link>
                  <Link to={`/chat?cowId=${encodeURIComponent(a.cow_id)}&risk=${encodeURIComponent(level)}`} className="rounded-xl border border-earth bg-white px-3 py-2 text-xs font-semibold">{t.dashboard.askCta}</Link>
                </div>
              </div>
            )
          })}
        </section>
      ) : null}

      <section className="rounded-2xl border border-earth bg-white p-5 shadow-sm">
        <h2 className="font-display text-lg font-semibold">{t.dashboard.recent}</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-[#1b4332]/60">
              <tr>
                <th className="py-2 pr-4 font-medium">{t.dashboard.cowId}</th>
                <th className="py-2 pr-4 font-medium">{t.dashboard.date}</th>
                <th className="py-2 pr-4 font-medium">{t.dashboard.result}</th>
                <th className="py-2 pr-4 font-medium">{t.dashboard.confidence}</th>
                <th className="py-2 pr-4 font-medium">{t.dashboard.risk}</th>
              </tr>
            </thead>
            <tbody>
              {(data?.recent_analyses || []).length === 0 ? (
                <tr><td colSpan={5} className="py-6 text-[#1b4332]/50">{t.dashboard.empty}</td></tr>
              ) : (
                data.recent_analyses.map((a) => (
                  <tr key={a.analysis_id} className="border-t border-earth/70">
                    <td className="py-3 pr-4 font-medium">{a.cow_id}</td>
                    <td className="py-3 pr-4">{a.timestamp ? new Date(a.timestamp).toLocaleString() : '—'}</td>
                    <td className="py-3 pr-4">{a.prediction}</td>
                    <td className="py-3 pr-4">{formatConfidence(a.confidence)}</td>
                    <td className="py-3 pr-4"><RiskBadge risk={a.risk_level} label={riskLabel(t, a.risk_level)} /></td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
