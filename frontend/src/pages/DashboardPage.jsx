import { useEffect, useMemo, useState } from 'react'
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
  Eye,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import AiModeBadge from '../components/AiModeBadge'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { getDashboard, getHealth, listAlerts } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

const RISK_COLORS = {
  Low: '#2d6a4f',
  Mild: '#40916c',
  Moderate: '#d4a373',
  High: '#bc4749',
  Critical: '#9d0208',
  Healthy: '#52b788',
  Severe: '#bc4749',
}

function riskLabel(t, risk) {
  const level = normalizeRiskLevel(risk)
  return t.risk?.[level] || level
}

export default function DashboardPage() {
  const { t, lang, revision } = useI18n()
  const { health, setHealth } = useOutletContext()
  const [data, setData] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    Promise.all([getDashboard(), getHealth(), listAlerts({ limit: 5 })])
      .then(([dash, h, al]) => {
        if (cancelled) return
        setData(dash)
        setHealth?.(h)
        setAlerts(Array.isArray(al) ? al : [])
      })
      .catch((e) => {
        if (!cancelled) setError(e.message || t.common.backendDown)
      })
    return () => {
      cancelled = true
    }
  }, [setHealth, t.common.backendDown, lang, revision])

  const cards = useMemo(
    () => [
      { label: t.dashboard.totalCows, value: data?.total_cows ?? '—', icon: Users },
      { label: t.dashboard.healthy, value: data?.healthy ?? '—', icon: HeartPulse },
      { label: t.dashboard.monitoring, value: data?.monitoring ?? '—', icon: Eye },
      { label: t.dashboard.atRisk, value: data?.at_risk ?? '—', icon: AlertTriangle },
      { label: t.dashboard.analysesMonth, value: data?.analyses_this_month ?? '—', icon: Activity },
    ],
    [t, data, lang, revision],
  )

  const riskChartData = useMemo(() => {
    const dist = data?.risk_distribution || {}
    return Object.entries(dist)
      .filter(([, count]) => count > 0)
      .map(([name, value]) => ({
        name: riskLabel(t, name),
        value,
        key: name,
      }))
  }, [data, t, lang, revision])

  const trendData = useMemo(
    () => (data?.monthly_analyses || []).map((m) => ({ name: m.label, scans: m.count })),
    [data],
  )

  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-3xl border border-earth bg-[#1b4332] text-white shadow-sm">
        <img src="/farm-hero.svg" alt="" className="absolute inset-0 h-full w-full object-cover opacity-25" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#1b4332] via-[#1b4332]/90 to-[#1b4332]/55" />
        <div className="relative z-10 p-6 sm:p-8">
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <AiModeBadge health={health || { demo_mode: data?.demo_mode }} />
            <span className="rounded-full border border-white/30 bg-white/10 px-3 py-1 text-xs font-semibold">
              {t.langIndicator}: {lang.toUpperCase()}
            </span>
            {data?.unread_alerts ? (
              <span className="rounded-full bg-red-500/90 px-3 py-1 text-xs font-bold">
                {data.unread_alerts} {t.dashboard.unreadAlerts}
              </span>
            ) : null}
          </div>
          <h1 className="font-display text-3xl font-bold sm:text-4xl">{t.dashboard.welcome}</h1>
          <p className="mt-2 max-w-xl text-base text-white/85">{t.dashboard.subtitle}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/analyze" className="inline-flex items-center gap-2 rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-[#1b4332] transition hover:bg-cream">
              <ScanLine className="h-4 w-4" />{t.dashboard.analyzeCta}
            </Link>
            <Link to="/camera" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/20">
              <Camera className="h-4 w-4" />{t.dashboard.cameraCta}
            </Link>
            <Link to="/chat" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/20">
              <MessageCircle className="h-4 w-4" />{t.dashboard.askCta}
            </Link>
            <Link to="/veterinarians" className="inline-flex items-center gap-2 rounded-2xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/20">
              <Stethoscope className="h-4 w-4" />{t.dashboard.vetCta}
            </Link>
          </div>
        </div>
      </section>

      <ErrorMessage message={error} />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        {cards.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-2xl border border-earth bg-white p-5 shadow-sm transition hover:shadow-md">
            <div className="flex items-center justify-between">
              <p className="text-sm text-[#1b4332]/60">{label}</p>
              <Icon className="h-5 w-5 text-[#2d6a4f]" />
            </div>
            <p className="mt-3 font-display text-3xl font-bold text-[#1b4332]">{value}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-earth bg-white p-5 shadow-sm">
          <h2 className="font-display text-lg font-semibold">{t.dashboard.riskDistribution}</h2>
          {riskChartData.length === 0 ? (
            <p className="mt-6 text-sm text-[#1b4332]/50">{t.dashboard.empty}</p>
          ) : (
            <div className="mt-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={riskChartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
                    {riskChartData.map((entry) => (
                      <Cell key={entry.key} fill={RISK_COLORS[entry.key] || '#95d5b2'} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>

        <section className="rounded-2xl border border-earth bg-white p-5 shadow-sm">
          <h2 className="font-display text-lg font-semibold">{t.dashboard.analysisTrend}</h2>
          {trendData.length === 0 ? (
            <p className="mt-6 text-sm text-[#1b4332]/50">{t.dashboard.empty}</p>
          ) : (
            <div className="mt-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trendData}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="scans" fill="#2d6a4f" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>
      </div>

      {alerts.length > 0 ? (
        <section className="space-y-3">
          <h2 className="font-display text-lg font-semibold">{t.dashboard.recentAlerts}</h2>
          {alerts.slice(0, 3).map((a) => {
            const level = normalizeRiskLevel(a.risk_level)
            return (
              <div key={a.id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 transition hover:shadow-sm">
                <div>
                  <RiskBadge risk={level} label={riskLabel(t, level)} />
                  <p className="mt-1 text-sm font-semibold">{a.cow_id} · {a.prediction || a.title}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {a.analysis_id ? (
                    <Link to={`/result/${a.analysis_id}`} className="rounded-xl bg-[#1b4332] px-3 py-2 text-xs font-semibold text-white">{t.alerts.viewAnalysis}</Link>
                  ) : null}
                  <Link to="/alerts" className="rounded-xl border border-earth bg-white px-3 py-2 text-xs font-semibold">{t.dashboard.viewAlert}</Link>
                  <Link to="/veterinarians" className="rounded-xl border border-earth bg-white px-3 py-2 text-xs font-semibold">{t.dashboard.findVet}</Link>
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
                <th className="py-2 font-medium">{t.alerts.viewAnalysis}</th>
              </tr>
            </thead>
            <tbody>
              {(data?.recent_analyses || []).length === 0 ? (
                <tr><td colSpan={6} className="py-6 text-[#1b4332]/50">{t.dashboard.empty}</td></tr>
              ) : (
                data.recent_analyses.map((a) => (
                  <tr key={a.analysis_id} className="border-t border-earth/70 transition hover:bg-cream/40">
                    <td className="py-3 pr-4 font-medium">
                      <Link to={`/cows/${encodeURIComponent(a.cow_id)}`} className="text-[#2d6a4f] underline">{a.cow_id}</Link>
                    </td>
                    <td className="py-3 pr-4">{a.timestamp ? new Date(a.timestamp).toLocaleString() : '—'}</td>
                    <td className="py-3 pr-4">{a.prediction}</td>
                    <td className="py-3 pr-4">{formatConfidence(a.confidence)}</td>
                    <td className="py-3 pr-4"><RiskBadge risk={a.risk_level} label={riskLabel(t, a.risk_level)} /></td>
                    <td className="py-3">
                      <Link to={`/result/${a.analysis_id}`} className="font-semibold text-[#2d6a4f] underline">{t.alerts.viewAnalysis}</Link>
                    </td>
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
