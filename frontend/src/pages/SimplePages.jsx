import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { MessageCircle, ScanLine } from 'lucide-react'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { listCows, listHistory } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

function riskLabel(t, risk) {
  const level = normalizeRiskLevel(risk)
  return t.risk?.[level] || t.risk?.[risk] || level
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
        {cows.map((c) => {
          const level = normalizeRiskLevel(c.current_status)
          return (
          <div
            key={c.cow_id}
            className="rounded-3xl border border-earth bg-white p-5 shadow-sm space-y-3 transition hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <Link to={`/cows/${encodeURIComponent(c.cow_id)}`} className="font-display text-xl font-bold text-[#1b4332] underline">
                {c.cow_id}
              </Link>
              <RiskBadge risk={level} label={riskLabel(t, level)} />
            </div>
            <p className="text-sm text-[#1b4332]/70">{c.name || '—'}</p>
            <div className="rounded-xl bg-cream/50 p-3 text-xs space-y-1 text-[#1b4332]/80">
              <p><strong>{t.cows.breed}:</strong> {c.breed || '—'}</p>
              <p><strong>{t.cowProfile.analysisCount}:</strong> {c.analysis_count ?? 0}</p>
              <p><strong>{t.dashboard.date}:</strong> {c.last_analysis_at ? new Date(c.last_analysis_at).toLocaleString() : '—'}</p>
            </div>
            <div className="pt-1 flex flex-wrap gap-2">
              <Link
                to={`/cows/${encodeURIComponent(c.cow_id)}`}
                className="inline-flex items-center gap-1.5 rounded-xl border border-earth px-4 py-2 text-xs font-semibold text-[#1b4332] hover:bg-cream"
              >
                {t.cowProfile.viewProfile}
              </Link>
              <Link
                to={`/analyze?cowId=${encodeURIComponent(c.cow_id)}`}
                className="inline-flex items-center gap-1.5 rounded-xl bg-[#1b4332] px-4 py-2 text-xs font-semibold text-white shadow-sm hover:bg-[#2d6a4f]"
              >
                <ScanLine className="h-3.5 w-3.5" />
                {t.cows.analyze}
              </Link>
              <Link
                to={`/chat?cowId=${encodeURIComponent(c.cow_id)}&risk=${encodeURIComponent(level)}`}
                className="inline-flex items-center gap-1.5 rounded-xl border border-earth px-4 py-2 text-xs font-semibold text-[#1b4332] hover:bg-cream"
              >
                <MessageCircle className="h-3.5 w-3.5" />
                {t.cows.ask}
              </Link>
            </div>
          </div>
        )})}
      </div>
    </div>
  )
}

export function HistoryPage() {
  const { t } = useI18n()
  const [rows, setRows] = useState([])
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState([])

  useEffect(() => {
    listHistory({ limit: 50 })
      .then(setRows)
      .catch((e) => setError(e.message))
  }, [])

  const compareHref = useMemo(() => {
    if (selected.length !== 2) return null
    return `/compare?ids=${selected.join(',')}`
  }, [selected])

  function toggleSelect(id) {
    setSelected((prev) => {
      if (prev.includes(id)) return prev.filter((x) => x !== id)
      if (prev.length >= 2) return [prev[1], id]
      return [...prev, id]
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.history.title}</h1>
        {compareHref ? (
          <Link to={compareHref} className="rounded-xl bg-[#1b4332] px-4 py-2 text-sm font-semibold text-white">
            {t.compare.action}
          </Link>
        ) : (
          <p className="text-xs text-[#1b4332]/60">{t.compare.selectTwo}</p>
        )}
      </div>
      <ErrorMessage message={error} />
      <div className="overflow-x-auto rounded-3xl border border-earth bg-white p-4 shadow-sm">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-earth/70 text-left text-xs font-semibold uppercase tracking-wider text-[#1b4332]/60">
              <th className="py-3 pr-3">{t.compare.pick}</th>
              <th className="py-3 pr-3">{t.dashboard.cowId}</th>
              <th className="py-3 pr-3">{t.dashboard.date}</th>
              <th className="py-3 pr-3">{t.dashboard.result}</th>
              <th className="py-3 pr-3">{t.result.detectionConfidence}</th>
              <th className="py-3 pr-3">{t.dashboard.risk}</th>
              <th className="py-3">{t.alerts.viewAnalysis}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-earth/40">
            {rows.map((a) => (
              <tr key={a.analysis_id} className="hover:bg-cream/40 transition">
                <td className="py-3 pr-3">
                  <input
                    type="checkbox"
                    checked={selected.includes(a.analysis_id)}
                    onChange={() => toggleSelect(a.analysis_id)}
                    aria-label={`${t.compare.pick} ${a.analysis_id}`}
                  />
                </td>
                <td className="py-3 pr-3 font-semibold text-[#1b4332]">
                  <Link to={`/cows/${encodeURIComponent(a.cow_id)}`} className="text-[#2d6a4f] underline">{a.cow_id}</Link>
                </td>
                <td className="py-3 pr-3 text-[#1b4332]/80">
                  {a.timestamp ? new Date(a.timestamp).toLocaleString() : '—'}
                </td>
                <td className="py-3 pr-3">{a.prediction}</td>
                <td className="py-3 pr-3 font-medium text-[#2d6a4f]">{formatConfidence(a.confidence)}</td>
                <td className="py-3 pr-3">
                  <RiskBadge risk={a.risk_level} label={riskLabel(t, a.risk_level)} />
                </td>
                <td className="py-3">
                  <Link to={`/result/${a.analysis_id}`} className="font-semibold text-[#2d6a4f] underline">
                    {t.alerts.viewAnalysis}
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
