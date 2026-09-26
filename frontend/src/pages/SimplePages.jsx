import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  AlertTriangle,
  AlertOctagon,
  AlertCircle,
  CheckCircle,
  ShieldAlert,
  MessageCircle,
  Phone,
  Stethoscope,
  ScanLine,
} from 'lucide-react'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { listCows, listHistory, listAlerts } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

function riskLabel(t, risk) {
  const level = normalizeRiskLevel(risk)
  return t.risk?.[level] || t.risk?.[risk] || level
}

function getRiskVisuals(level) {
  switch (level) {
    case 'Critical':
      return {
        icon: ShieldAlert,
        color: '#b91c1c',
        badgeBg: 'bg-red-100 text-red-800 border-red-300',
        cardBorder: 'border-red-300 bg-red-50/20',
      }
    case 'High':
      return {
        icon: AlertOctagon,
        color: '#c2410c',
        badgeBg: 'bg-orange-100 text-orange-800 border-orange-300',
        cardBorder: 'border-orange-200 bg-orange-50/20',
      }
    case 'Moderate':
      return {
        icon: AlertTriangle,
        color: '#b45309',
        badgeBg: 'bg-amber-100 text-amber-800 border-amber-300',
        cardBorder: 'border-amber-200 bg-amber-50/15',
      }
    case 'Mild':
      return {
        icon: AlertCircle,
        color: '#0369a1',
        badgeBg: 'bg-sky-100 text-sky-800 border-sky-300',
        cardBorder: 'border-sky-200 bg-sky-50/15',
      }
    case 'Low':
    default:
      return {
        icon: CheckCircle,
        color: '#15803d',
        badgeBg: 'bg-emerald-100 text-emerald-800 border-emerald-300',
        cardBorder: 'border-emerald-200 bg-emerald-50/15',
      }
  }
}

export function CowsPage() {
  const { t } = useI18n()
  const [cows, setCows] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    listCows()
      .then(setCows)
      .catch((e) => setError(e.message))
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.cows.title}</h1>
      </div>
      <div className="overflow-hidden rounded-3xl border border-earth shadow-sm">
        <img src="/farm-hero.svg" alt="" className="h-28 w-full object-cover opacity-35" />
      </div>
      <ErrorMessage message={error} />
      <div className="grid gap-4 sm:grid-cols-2">
        {cows.length === 0 && !error ? (
          <p className="text-[#1b4332]/60">{t.cows.empty}</p>
        ) : null}
        {cows.map((c) => (
          <div
            key={c.cow_id}
            className="rounded-3xl border border-earth bg-white p-5 shadow-sm space-y-3"
          >
            <div className="flex items-center justify-between">
              <p className="font-display text-xl font-bold text-[#1b4332]">{c.cow_id}</p>
              <span className="rounded-full bg-cream px-3 py-1 text-xs font-semibold text-[#2d6a4f]">
                {c.current_status || 'Active'}
              </span>
            </div>
            <p className="text-sm text-[#1b4332]/70">{c.name || '—'}</p>
            <div className="rounded-xl bg-cream/50 p-3 text-xs space-y-1 text-[#1b4332]/80">
              <p>
                <strong>{t.cows.breed}:</strong> {c.breed || '—'}
              </p>
              <p>
                <strong>{t.cows.status}:</strong> {c.current_status || '—'}
              </p>
            </div>
            <div className="pt-1 flex flex-wrap gap-2">
              <Link
                to="/analyze"
                className="inline-flex items-center gap-1.5 rounded-xl bg-[#1b4332] px-4 py-2 text-xs font-semibold text-white shadow-sm hover:bg-[#2d6a4f]"
              >
                <ScanLine className="h-3.5 w-3.5" />
                {t.cows.analyze}
              </Link>
              <Link
                to={`/chat?cowId=${encodeURIComponent(c.cow_id)}&risk=${encodeURIComponent(c.current_status || '')}`}
                className="inline-flex items-center gap-1.5 rounded-xl border border-earth px-4 py-2 text-xs font-semibold text-[#1b4332] hover:bg-cream"
              >
                <MessageCircle className="h-3.5 w-3.5" />
                {t.cows.ask}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export function HistoryPage() {
  const { t } = useI18n()
  const [rows, setRows] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    listHistory(50)
      .then(setRows)
      .catch((e) => setError(e.message))
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.history.title}</h1>
      </div>
      <ErrorMessage message={error} />
      <div className="overflow-x-auto rounded-3xl border border-earth bg-white p-4 shadow-sm">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-earth/70 text-left text-xs font-semibold uppercase tracking-wider text-[#1b4332]/60">
              <th className="py-3 pr-3">{t.dashboard.cowId}</th>
              <th className="py-3 pr-3">{t.dashboard.date}</th>
              <th className="py-3 pr-3">{t.dashboard.result}</th>
              <th className="py-3 pr-3">{t.dashboard.confidence}</th>
              <th className="py-3 pr-3">{t.dashboard.risk}</th>
              <th className="py-3">AI Engine</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-earth/40">
            {rows.map((a) => (
              <tr key={a.analysis_id} className="hover:bg-cream/40 transition">
                <td className="py-3 pr-3 font-semibold text-[#1b4332]">{a.cow_id}</td>
                <td className="py-3 pr-3 text-[#1b4332]/80">
                  {a.timestamp ? new Date(a.timestamp).toLocaleString() : '—'}
                </td>
                <td className="py-3 pr-3">{a.prediction}</td>
                <td className="py-3 pr-3 font-medium text-[#2d6a4f]">{formatConfidence(a.confidence)}</td>
                <td className="py-3 pr-3">
                  <RiskBadge risk={a.risk_level} label={riskLabel(t, a.risk_level)} />
                </td>
                <td className="py-3 text-xs font-semibold">
                  <span className="rounded-full bg-cream px-2.5 py-1 text-[#2d6a4f]">
                    {a.demo_mode ? t.history.demo : t.history.live}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export function AlertsPage() {
  const { t } = useI18n()
  const [alerts, setAlerts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    listAlerts()
      .then(setAlerts)
      .catch((e) => setError(e.message))
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.alerts.title}</h1>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.alerts.subtitle}</p>
      </div>

      <ErrorMessage message={error} />

      <div className="space-y-5">
        {alerts.length === 0 && !error ? (
          <div className="rounded-3xl border border-earth bg-white p-8 text-center shadow-sm">
            <CheckCircle className="mx-auto h-10 w-10 text-emerald-600 mb-2" />
            <p className="text-base font-medium text-[#1b4332]">{t.alerts.empty}</p>
            <p className="mt-1 text-xs text-[#1b4332]/60">All monitored cows are currently within safe observation thresholds.</p>
          </div>
        ) : null}

        {alerts.map((a) => {
          const level = normalizeRiskLevel(a.risk_level)
          const visuals = getRiskVisuals(level)
          const RiskIcon = visuals.icon
          const care = a.care_guidance || {}
          const chatQs = new URLSearchParams({
            cowId: a.cow_id || '',
            risk: level,
            detection: a.prediction || a.yolo_class || '',
            confidence: String(a.confidence ?? ''),
          })

          return (
            <article
              key={a.id}
              className={`rounded-3xl border p-6 shadow-sm transition hover:shadow-md bg-white ${visuals.cardBorder}`}
              aria-label={`${level} alert for ${a.cow_id}`}
            >
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-earth/60 pb-3">
                <div className="flex items-center gap-2.5">
                  <RiskIcon className="h-6 w-6" aria-hidden color={visuals.color} />
                  <span className={`inline-flex items-center rounded-xl border px-3 py-1 text-xs font-bold uppercase tracking-wider ${visuals.badgeBg}`}>
                    {riskLabel(t, level)}
                  </span>
                  <span className="text-xs font-semibold text-[#1b4332]/60">
                    ({level})
                  </span>
                </div>
                <p className="text-xs font-medium text-[#1b4332]/60">
                  {a.created_at ? new Date(a.created_at).toLocaleString() : ''}
                </p>
              </div>

              <div className="mt-4 flex flex-wrap items-baseline justify-between gap-2">
                <h2 className="font-display text-2xl font-bold text-[#1b4332]">
                  {care.title || a.title}
                </h2>
                <div className="text-sm font-semibold text-[#1b4332]">
                  <span>{t.dashboard.cowId}: </span>
                  <span className="rounded-lg bg-cream px-2 py-0.5 text-[#2d6a4f]">{a.cow_id}</span>
                  {a.cow_name ? <span className="ml-1.5 text-xs text-[#1b4332]/70 font-normal">({a.cow_name})</span> : null}
                </div>
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-2 rounded-2xl bg-cream/40 p-4 text-xs">
                <div>
                  <span className="text-[#1b4332]/60 uppercase tracking-wider font-semibold block">{t.result.prediction}:</span>
                  <span className="text-sm font-bold text-[#1b4332]">{a.prediction || a.yolo_class || 'Abnormal signs detected'}</span>
                </div>
                <div>
                  <span className="text-[#1b4332]/60 uppercase tracking-wider font-semibold block">{t.dashboard.confidence}:</span>
                  <span className="text-sm font-bold text-[#2d6a4f]">{formatConfidence(a.confidence)}</span>
                </div>
                {a.yolo_class && (
                  <div>
                    <span className="text-[#1b4332]/60 uppercase tracking-wider font-semibold block">{t.alerts.yoloClass}:</span>
                    <span className="font-medium text-[#1b4332]">{a.yolo_class}</span>
                  </div>
                )}
                <div>
                  <span className="text-[#1b4332]/60 uppercase tracking-wider font-semibold block">{t.alerts.urgency}:</span>
                  <span className="font-medium text-[#1b4332]">{care.urgency || 'Evaluate condition'}</span>
                </div>
              </div>

              <div className="mt-4 space-y-3">
                <div className="rounded-2xl border border-earth/80 bg-white p-4 text-xs">
                  <p className="font-bold text-[#1b4332] flex items-center gap-1.5">
                    <AlertTriangle className="h-4 w-4 text-amber-600" />
                    {t.alerts.why}
                  </p>
                  <p className="mt-1 text-[#1b4332]/85 text-sm">{care.why || a.message}</p>
                </div>

                <div className="rounded-2xl border border-earth/80 bg-cream/30 p-4 text-xs">
                  <p className="font-bold text-[#1b4332] uppercase tracking-wider">{t.alerts.careLabel}</p>
                  <ul className="mt-2 list-disc space-y-1.5 pl-5 text-sm text-[#1b4332]/85">
                    {(care.guidance || []).map((point, idx) => (
                      <li key={idx}>{point}</li>
                    ))}
                  </ul>
                  <div className="mt-3 pt-3 border-t border-earth/50">
                    <p className="text-xs font-bold text-[#1b4332]">
                      {t.alerts.nextStep}: <span className="font-normal text-[#1b4332]/90">{care.next_step}</span>
                    </p>
                  </div>
                  <p className="mt-2 text-[11px] font-semibold text-amber-900 bg-amber-50 rounded-lg p-2 border border-amber-200">
                    ⚠️ {t.alerts.medSafety}
                  </p>
                </div>
              </div>

              <div className="mt-5 flex flex-wrap items-center gap-3 pt-3 border-t border-earth/60">
                <Link
                  to="/veterinarians"
                  className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-4 py-2.5 text-xs font-semibold text-white shadow-sm transition hover:bg-[#2d6a4f]"
                >
                  <Stethoscope className="h-4 w-4" />
                  {t.alerts.findVet}
                </Link>

                {a.phone ? (
                  <a
                    href={`tel:${a.phone}`}
                    className="inline-flex items-center gap-2 rounded-xl border border-earth bg-white px-4 py-2.5 text-xs font-semibold text-[#1b4332] shadow-sm hover:bg-cream"
                  >
                    <Phone className="h-4 w-4 text-[#2d6a4f]" />
                    {t.alerts.callVet}
                  </a>
                ) : (
                  <span className="inline-flex items-center gap-1.5 rounded-xl border border-dashed border-earth/80 bg-cream/40 px-3 py-2 text-[11px] text-[#1b4332]/65">
                    <Phone className="h-3.5 w-3.5 opacity-50" />
                    {t.alerts.noPhone}
                  </span>
                )}

                <Link
                  to={`/chat?${chatQs.toString()}`}
                  className="inline-flex items-center gap-2 rounded-xl border border-[#2d6a4f] bg-[#2d6a4f]/10 px-4 py-2.5 text-xs font-semibold text-[#1b4332] hover:bg-[#2d6a4f]/20"
                >
                  <MessageCircle className="h-4 w-4 text-[#2d6a4f]" />
                  {t.alerts.ask}
                </Link>
              </div>

              <p className="mt-4 text-[10px] text-[#1b4332]/50 italic">
                {t.disclaimer}
              </p>
            </article>
          )
        })}
      </div>
    </div>
  )
}
