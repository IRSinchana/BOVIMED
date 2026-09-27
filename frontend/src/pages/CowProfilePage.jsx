import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Activity, MessageCircle, ScanLine, Stethoscope } from 'lucide-react'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { getCow, getCowHistory, mediaUrl } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'

export default function CowProfilePage() {
  const { cowId } = useParams()
  const { t, textDir } = useI18n()
  const [cow, setCow] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!cowId) return
    setLoading(true)
    Promise.all([getCow(cowId), getCowHistory(cowId)])
      .then(([c, h]) => {
        setCow(c)
        setHistory(Array.isArray(h) ? h : [])
      })
      .catch((e) => setError(e.message || t.common.error))
      .finally(() => setLoading(false))
  }, [cowId, t.common.error])

  const latest = history[0]
  const level = normalizeRiskLevel(cow?.current_status || latest?.risk_level)
  const riskText = t.risk?.[level] || level

  if (loading) {
    return <p className="text-sm text-[#1b4332]/60">{t.common.loading}</p>
  }

  return (
    <div className="space-y-6" dir={textDir}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <Link to="/cows" className="text-sm font-semibold text-[#2d6a4f] underline">
            ← {t.cows.title}
          </Link>
          <h1 className="mt-2 font-display text-3xl font-bold text-[#1b4332]">{cowId}</h1>
          <p className="text-sm text-[#1b4332]/70">{cow?.name || cowId}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            to={`/analyze?cowId=${encodeURIComponent(cowId)}`}
            className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-4 py-2 text-sm font-semibold text-white"
          >
            <ScanLine className="h-4 w-4" />
            {t.cows.analyze}
          </Link>
          <Link
            to={`/chat?cowId=${encodeURIComponent(cowId)}&risk=${encodeURIComponent(level)}`}
            className="inline-flex items-center gap-2 rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold"
          >
            <MessageCircle className="h-4 w-4" />
            {t.cows.ask}
          </Link>
        </div>
      </div>

      <ErrorMessage message={error} />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-2xl border border-earth bg-white p-4 shadow-sm">
          <p className="text-xs uppercase text-[#1b4332]/60">{t.cowProfile.currentRisk}</p>
          <div className="mt-2"><RiskBadge risk={level} label={riskText} /></div>
        </div>
        <div className="rounded-2xl border border-earth bg-white p-4 shadow-sm">
          <p className="text-xs uppercase text-[#1b4332]/60">{t.cowProfile.latestDetection}</p>
          <p className="mt-2 font-semibold text-[#1b4332]">{latest?.prediction || '—'}</p>
        </div>
        <div className="rounded-2xl border border-earth bg-white p-4 shadow-sm">
          <p className="text-xs uppercase text-[#1b4332]/60">{t.result.detectionConfidence}</p>
          <p className="mt-2 font-semibold text-[#2d6a4f]">{formatConfidence(latest?.confidence)}</p>
        </div>
        <div className="rounded-2xl border border-earth bg-white p-4 shadow-sm">
          <p className="text-xs uppercase text-[#1b4332]/60">{t.cowProfile.analysisCount}</p>
          <p className="mt-2 font-display text-2xl font-bold text-[#1b4332]">{cow?.analysis_count ?? history.length}</p>
        </div>
      </div>

      <section className="rounded-3xl border border-earth bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-display text-xl font-semibold text-[#1b4332]">{t.cowProfile.timeline}</h2>
          {history.length >= 2 ? (
            <Link
              to={`/compare?ids=${history[0].analysis_id},${history[1].analysis_id}`}
              className="text-sm font-semibold text-[#2d6a4f] underline"
            >
              {t.cowProfile.compareLatest}
            </Link>
          ) : null}
        </div>

        {history.length === 0 ? (
          <p className="mt-4 text-sm text-[#1b4332]/60">{t.cowProfile.noHistory}</p>
        ) : (
          <ol className="mt-5 space-y-4">
            {history.map((item) => {
              const itemLevel = normalizeRiskLevel(item.risk_level)
              return (
                <li key={item.analysis_id} className="flex gap-4 rounded-2xl border border-earth/70 bg-cream/30 p-4">
                  {item.annotated_image_url || item.image_url ? (
                    <img
                      src={mediaUrl(item.annotated_image_url || item.image_url)}
                      alt=""
                      className="h-20 w-20 shrink-0 rounded-xl object-cover bg-stone-100"
                    />
                  ) : (
                    <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-earth/40">
                      <Activity className="h-6 w-6 text-[#2d6a4f]" />
                    </div>
                  )}
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <RiskBadge risk={itemLevel} label={t.risk?.[itemLevel] || itemLevel} />
                      <span className="text-xs text-[#1b4332]/55">
                        {item.timestamp ? new Date(item.timestamp).toLocaleString() : ''}
                      </span>
                    </div>
                    <p className="mt-1 font-semibold text-[#1b4332]">{item.prediction}</p>
                    <p className="text-xs text-[#1b4332]/70">
                      {t.result.detectionConfidence}: {formatConfidence(item.confidence)}
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      <Link
                        to={`/result/${item.analysis_id}`}
                        className="rounded-lg bg-[#1b4332] px-3 py-1.5 text-xs font-semibold text-white"
                      >
                        {t.alerts.viewAnalysis}
                      </Link>
                      <Link
                        to={`/chat?cowId=${encodeURIComponent(cowId)}&risk=${encodeURIComponent(itemLevel)}&detection=${encodeURIComponent(item.prediction || '')}&confidence=${encodeURIComponent(item.confidence ?? '')}`}
                        className="rounded-lg border border-earth bg-white px-3 py-1.5 text-xs font-semibold"
                      >
                        {t.alerts.ask}
                      </Link>
                    </div>
                  </div>
                </li>
              )
            })}
          </ol>
        )}
      </section>

      <Link
        to="/veterinarians"
        className="inline-flex items-center gap-2 rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]"
      >
        <Stethoscope className="h-4 w-4" />
        {t.alerts.findVet}
      </Link>
    </div>
  )
}
