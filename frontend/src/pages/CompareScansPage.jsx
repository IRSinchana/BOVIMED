import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import AnalysisResult from '../components/AnalysisResult'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { getAnalysis } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

function ScanSummary({ scan, label, t }) {
  if (!scan) return null
  const level = normalizeRiskLevel(scan.risk_level)
  return (
    <div className="rounded-2xl border border-earth bg-white p-4 shadow-sm">
      <p className="text-xs font-bold uppercase tracking-wide text-[#2d6a4f]">{label}</p>
      <p className="mt-2 text-sm text-[#1b4332]/60">{scan.timestamp ? new Date(scan.timestamp).toLocaleString() : ''}</p>
      <p className="mt-2 font-semibold text-[#1b4332]">{scan.prediction}</p>
      <div className="mt-2"><RiskBadge risk={level} label={t.risk?.[level] || level} /></div>
      <p className="mt-2 text-sm">
        {t.result.detectionConfidence}: <strong>{formatConfidence(scan.confidence)}</strong>
      </p>
      {scan.primary_finding?.class_name ? (
        <p className="mt-1 text-sm text-[#1b4332]/70">
          {t.result.detectionLabel}: {scan.primary_finding.class_name}
        </p>
      ) : null}
      <Link to={`/result/${scan.analysis_id}`} className="mt-3 inline-block text-sm font-semibold text-[#2d6a4f] underline">
        {t.alerts.viewAnalysis}
      </Link>
    </div>
  )
}

export default function CompareScansPage() {
  const { t, textDir } = useI18n()
  const [params] = useSearchParams()
  const ids = useMemo(
    () =>
      (params.get('ids') || '')
        .split(',')
        .map((v) => Number(v.trim()))
        .filter((n) => Number.isFinite(n) && n > 0)
        .slice(0, 2),
    [params],
  )
  const [scans, setScans] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (ids.length < 2) {
      setLoading(false)
      return
    }
    setLoading(true)
    Promise.all(ids.map((id) => getAnalysis(id)))
      .then(setScans)
      .catch((e) => setError(e.message || t.common.error))
      .finally(() => setLoading(false))
  }, [ids, t.common.error])

  const [older, newer] = scans.length === 2
    ? [...scans].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    : [null, null]

  const confidenceDelta =
    newer && older ? Number(newer.confidence || 0) - Number(older.confidence || 0) : null

  if (loading) return <p className="text-sm text-[#1b4332]/60">{t.common.loading}</p>

  if (ids.length < 2) {
    return (
      <div className="space-y-4" dir={textDir}>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.compare.title}</h1>
        <p className="text-sm text-[#1b4332]/70">{t.compare.selectTwo}</p>
        <Link to="/history" className="text-sm font-semibold text-[#2d6a4f] underline">{t.history.title}</Link>
      </div>
    )
  }

  return (
    <div className="space-y-6" dir={textDir}>
      <div>
        <Link to="/history" className="text-sm font-semibold text-[#2d6a4f] underline">← {t.history.title}</Link>
        <h1 className="mt-2 font-display text-3xl font-bold text-[#1b4332]">{t.compare.title}</h1>
        <p className="text-sm text-[#1b4332]/70">{t.compare.subtitle}</p>
      </div>

      <ErrorMessage message={error} />

      <div className="grid gap-4 lg:grid-cols-[1fr_auto_1fr] lg:items-center">
        <ScanSummary scan={older} label={t.compare.previous} t={t} />
        <ArrowRight className="mx-auto hidden h-8 w-8 text-[#2d6a4f] lg:block" />
        <ScanSummary scan={newer} label={t.compare.latest} t={t} />
      </div>

      {confidenceDelta != null ? (
        <div className="rounded-2xl border border-earth bg-cream/40 px-4 py-3 text-sm">
          <p className="font-semibold text-[#1b4332]">{t.compare.changeOverTime}</p>
          <p className="mt-1 text-[#1b4332]/80">
            {t.result.detectionConfidence}: {confidenceDelta >= 0 ? '+' : ''}
            {(confidenceDelta * 100).toFixed(1)}%
            {older?.risk_level !== newer?.risk_level
              ? ` · ${t.dashboard.risk}: ${older.risk_level} → ${newer.risk_level}`
              : ''}
          </p>
        </div>
      ) : null}

      {newer ? (
        <section className="space-y-4">
          <h2 className="font-display text-xl font-semibold">{t.compare.latestDetail}</h2>
          <AnalysisResult result={newer} />
        </section>
      ) : null}
    </div>
  )
}
