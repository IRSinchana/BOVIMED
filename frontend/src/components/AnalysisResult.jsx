import { Link } from 'react-router-dom'
import { mediaUrl } from '../services/api'
import { formatBBox, formatConfidence, normalizeRiskLevel } from '../utils/analysis'
import { useI18n } from '../i18n/I18nContext'
import AiModeBadge from './AiModeBadge'
import { ConfidenceBar, RiskBadge } from './Status'

export default function AnalysisResult({ result, localPreviewUrl, health }) {
  const { t } = useI18n()
  if (!result) return null

  const originalSrc = localPreviewUrl || mediaUrl(result.image_url)
  const annotatedSrc = mediaUrl(result.annotated_image_url)
  const detections = Array.isArray(result.detections) ? result.detections : []
  const recommendations = Array.isArray(result.recommendations) ? result.recommendations : []
  const level = normalizeRiskLevel(result.risk_level)
  const riskText = t.risk?.[level] || level

  return (
    <div className="space-y-6 animate-[fadeIn_0.35s_ease]">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="font-display text-2xl font-bold text-[#1b4332]">{t.result.title}</h2>
          <p className="mt-1 text-sm text-[#1b4332]/70">{result.screening_type || t.result.screening}</p>
        </div>
        <AiModeBadge
          health={health || { demo_mode: result.demo_mode, message: result.demo_mode ? t.demoMode : t.liveAi }}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <figure className="overflow-hidden rounded-2xl border border-earth bg-white shadow-sm">
            <figcaption className="border-b border-earth px-4 py-2 text-sm font-medium">{t.result.original}</figcaption>
            {originalSrc ? (
              <img src={originalSrc} alt="" className="max-h-80 w-full object-contain bg-stone-100" />
            ) : (
              <div className="flex h-48 items-center justify-center text-sm text-[#1b4332]/50">—</div>
            )}
          </figure>
          <figure className="overflow-hidden rounded-2xl border border-earth bg-white shadow-sm">
            <figcaption className="border-b border-earth px-4 py-2 text-sm font-medium">{t.result.annotated}</figcaption>
            {annotatedSrc ? (
              <img src={annotatedSrc} alt="" className="max-h-80 w-full object-contain bg-stone-100" />
            ) : (
              <div className="flex h-48 items-center justify-center text-sm text-[#1b4332]/50">—</div>
            )}
          </figure>
        </div>

        <div className="space-y-4 rounded-2xl border border-earth bg-white p-5 shadow-sm">
          <div>
            <p className="text-sm text-[#1b4332]/60">{t.result.prediction}</p>
            <p className="mt-1 font-display text-xl font-semibold">{result.prediction}</p>
          </div>
          <ConfidenceBar value={result.confidence} label={t.result.confidence} />
          <div>
            <p className="mb-2 text-sm text-[#1b4332]/60">{t.result.risk}</p>
            <RiskBadge risk={level} label={riskText} />
          </div>
          {result.primary_finding ? (
            <div className="rounded-xl bg-cream px-4 py-3 text-sm">
              <p className="font-semibold">{t.result.primary}</p>
              <p className="mt-1">{result.primary_finding.class_name} ({formatConfidence(result.primary_finding.confidence)})</p>
            </div>
          ) : (
            <div className="rounded-xl bg-cream px-4 py-3 text-sm">{t.result.noPrimary}</div>
          )}
          <div>
            <p className="mb-2 text-sm font-semibold">{t.result.detections}</p>
            {detections.length === 0 ? (
              <p className="text-sm text-[#1b4332]/70">{t.result.noDetections}</p>
            ) : (
              <ul className="space-y-2">
                {detections.map((d, i) => (
                  <li key={`${d.class_name}-${i}`} className="rounded-xl border border-earth px-3 py-2 text-sm">
                    <div className="flex justify-between gap-2">
                      <span className="font-medium">{d.class_name}</span>
                      <span className="text-[#2d6a4f]">{formatConfidence(d.confidence)}</span>
                    </div>
                    {formatBBox(d.bbox) ? <p className="mt-1 text-xs text-[#1b4332]/55">BBox: [{formatBBox(d.bbox)}]</p> : null}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div>
            <p className="mb-2 text-sm font-semibold">{t.result.careGuidance}</p>
            <ul className="list-disc space-y-1 pl-5 text-sm text-[#1b4332]/80">
              {(result.care_guidance?.guidance || recommendations).map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
            <p className="mt-2 text-xs font-medium text-amber-900">{t.alerts.medSafety}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link
              to={`/chat?cowId=${encodeURIComponent(result.cow_id || '')}&risk=${encodeURIComponent(level)}&detection=${encodeURIComponent(result.prediction || '')}&confidence=${encodeURIComponent(result.confidence ?? '')}`}
              className="inline-flex rounded-xl bg-[#2d6a4f] px-4 py-2 text-sm font-semibold text-white"
            >
              {t.result.askBovimed}
            </Link>
            <Link
              to="/veterinarians"
              className="inline-flex rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]"
            >
              {t.alerts.findVet}
            </Link>
          </div>
          <p className="border-t border-earth pt-3 text-xs text-[#1b4332]/55">{result.disclaimer || t.disclaimer}</p>
        </div>
      </div>
    </div>
  )
}
