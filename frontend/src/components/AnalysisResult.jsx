import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronDown } from 'lucide-react'
import { getModelInfo } from '../services/api'
import {
  formatBBox,
  formatConfidence,
  getFindingDisplayLabel,
  getPrimaryDetection,
  hasHealthFinding,
  normalizeRiskLevel,
  resolveAnnotatedImageSrc,
  resolveOriginalImageSrc,
} from '../utils/analysis'
import { useI18n } from '../i18n/I18nContext'
import AiModeBadge from './AiModeBadge'
import AnalysisImage from './AnalysisImage'
import DetectionImageOverlay from './DetectionImageOverlay'
import ExplainResultPanel from './ExplainResultPanel'
import { ConfidenceBar, RiskBadge } from './Status'

function formatMetric(value) {
  if (value == null || Number.isNaN(Number(value))) return '—'
  return `${(Number(value) * 100).toFixed(2)}%`
}

export default function AnalysisResult({ result, health }) {
  const { t, textDir } = useI18n()
  const [modelInfo, setModelInfo] = useState(null)

  useEffect(() => {
    getModelInfo()
      .then(setModelInfo)
      .catch(() => setModelInfo(null))
  }, [])

  if (!result) return null

  const originalSrc = resolveOriginalImageSrc(result)
  const annotatedSrc = resolveAnnotatedImageSrc(result)
  const detections = Array.isArray(result.detections) ? result.detections : []
  const recommendations = Array.isArray(result.recommendations) ? result.recommendations : []
  const level = normalizeRiskLevel(result.risk_level)
  const riskText = t.risk?.[level] || level
  const demoMode = result.demo_mode ?? health?.demo_mode
  const modelName = result.model_name || modelInfo?.model_name || 'BOVIMED YOLO11n'
  const metrics = modelInfo?.validation_metrics
  const primaryDetection = getPrimaryDetection(result)
  const findingLabel = getFindingDisplayLabel(result, t)
  const detectionConfidence = primaryDetection?.confidence ?? result.confidence
  const showFinding = hasHealthFinding(result)

  return (
    <div className="space-y-6 animate-[fadeIn_0.35s_ease]">
      <div className="flex flex-wrap items-center justify-between gap-3" dir={textDir}>
        <div>
          <h2 className="font-display text-2xl font-bold text-[#1b4332]">{t.result.title}</h2>
          <p className="mt-1 text-sm text-[#1b4332]/70">{result.screening_type || t.result.screening}</p>
        </div>
        <AiModeBadge
          health={health || { demo_mode: demoMode, message: demoMode ? t.demoMode : t.liveAi }}
        />
      </div>

      <section className="rounded-2xl border border-emerald-200 bg-emerald-50/80 p-4" dir={textDir}>
        <p className="text-xs font-bold uppercase tracking-wide text-[#2d6a4f]">{t.result.modelSection}</p>
        <div className="mt-2 flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="font-display text-xl font-bold text-[#1b4332]">{modelName}</p>
            <p className="text-sm text-[#1b4332]/70">{t.result.modelSubtitle}</p>
            <p className="mt-1 text-xs text-[#1b4332]/55">
              {result.model_loaded ? t.result.modelLoaded : t.result.modelNotLoaded}
              {demoMode ? ` · ${t.demoMode}` : ` · ${t.liveAi}`}
            </p>
          </div>
          <AiModeBadge health={{ demo_mode: demoMode }} compact />
        </div>
        {primaryDetection ? (
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl bg-white/80 px-3 py-2">
              <p className="text-xs font-semibold uppercase text-[#1b4332]/60">{t.result.detectionLabel}</p>
              <p className="mt-1 font-semibold text-[#1b4332]">{primaryDetection.class_name}</p>
              {primaryDetection.class_id != null ? (
                <p className="text-xs text-[#1b4332]/55">
                  {t.result.classId}: {primaryDetection.class_id}
                </p>
              ) : null}
            </div>
            <div className="rounded-xl bg-white/80 px-3 py-2">
              <p className="text-xs font-semibold uppercase text-[#1b4332]/60">{t.result.detectionConfidence}</p>
              <p className="mt-1 font-semibold text-[#2d6a4f]">{formatConfidence(detectionConfidence)}</p>
            </div>
          </div>
        ) : null}
      </section>

      <figure className="overflow-hidden rounded-3xl border-2 border-[#2d6a4f]/20 bg-white shadow-md">
        <figcaption className="flex flex-wrap items-center justify-between gap-2 border-b border-earth bg-cream/50 px-4 py-3">
          <span className="text-sm font-semibold text-[#1b4332]">{t.result.annotated}</span>
          {primaryDetection ? (
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-[#1b4332]">
              {primaryDetection.class_name} · {formatConfidence(detectionConfidence)}
            </span>
          ) : null}
        </figcaption>
        {annotatedSrc ? (
          <AnalysisImage
            src={annotatedSrc}
            alt={t.result.annotated}
            fallbackLabel={t.result.imageUnavailable}
            className="max-h-[28rem] w-full object-contain bg-stone-100"
          />
        ) : (
          <DetectionImageOverlay
            src={originalSrc}
            detections={detections}
            alt={t.result.annotated}
            fallbackLabel={t.result.imageUnavailable}
            maxHeightClass="max-h-[28rem]"
          />
        )}
      </figure>

      <ExplainResultPanel result={result} />

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <figure className="overflow-hidden rounded-2xl border border-earth bg-white shadow-sm">
            <figcaption className="border-b border-earth px-4 py-2 text-sm font-medium">{t.result.original}</figcaption>
            <DetectionImageOverlay
              src={originalSrc}
              detections={detections}
              alt={t.result.original}
              fallbackLabel={t.result.imageUnavailable}
            />
          </figure>
          <figure className="overflow-hidden rounded-2xl border border-earth bg-white shadow-sm">
            <figcaption className="border-b border-earth px-4 py-2 text-sm font-medium">{t.result.annotated}</figcaption>
            {annotatedSrc ? (
              <AnalysisImage
                src={annotatedSrc}
                alt={t.result.annotated}
                fallbackLabel={t.result.imageUnavailable}
              />
            ) : (
              <DetectionImageOverlay
                src={originalSrc}
                detections={detections}
                alt={t.result.annotated}
                fallbackLabel={t.result.imageUnavailable}
              />
            )}
          </figure>
        </div>

        <div className="space-y-4 rounded-2xl border border-earth bg-white p-5 shadow-sm" dir={textDir}>
          <div>
            <p className="text-sm text-[#1b4332]/60">{t.result.prediction}</p>
            <p className="mt-1 font-display text-xl font-semibold">{findingLabel}</p>
          </div>
          <ConfidenceBar value={detectionConfidence} label={t.result.detectionConfidence} />
          <div>
            <p className="mb-2 text-sm text-[#1b4332]/60">{t.result.risk}</p>
            <RiskBadge risk={level} label={riskText} />
          </div>
          <div className="rounded-xl bg-cream px-4 py-3 text-sm">
            <p className="font-semibold">{t.result.primary}</p>
            {showFinding ? (
              <p className="mt-1">
                {primaryDetection?.class_name ? (
                  <>
                    {primaryDetection.class_name} ({formatConfidence(detectionConfidence)})
                  </>
                ) : (
                  findingLabel
                )}
              </p>
            ) : (
              <p className="mt-1">{t.result.noPrimaryDetected}</p>
            )}
          </div>
          <div>
            <p className="mb-2 text-sm font-semibold">{t.result.detections}</p>
            {detections.length === 0 ? (
              <p className="text-sm text-[#1b4332]/70">
                {showFinding ? t.result.detectionSummaryOnly : t.result.noDetections}
              </p>
            ) : (
              <ul className="space-y-2">
                {detections.map((d, i) => (
                  <li key={`${d.class_name}-${i}`} className="rounded-xl border border-earth px-3 py-2 text-sm">
                    <div className="flex justify-between gap-2">
                      <span className="font-medium">{d.class_name}</span>
                      <span className="text-[#2d6a4f]">{formatConfidence(d.confidence)}</span>
                    </div>
                    <p className="mt-1 text-xs text-[#1b4332]/55">
                      {d.class_id != null ? `${t.result.classId}: ${d.class_id} · ` : ''}
                      {t.result.detectionConfidence}: {formatConfidence(d.confidence)}
                    </p>
                    {formatBBox(d.bbox) ? (
                      <p className="mt-1 text-xs text-[#1b4332]/55">BBox: [{formatBBox(d.bbox)}]</p>
                    ) : null}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {metrics ? (
            <details className="rounded-xl border border-earth bg-cream/40">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-2 px-4 py-3 text-sm font-semibold text-[#1b4332]">
                <span>{t.result.modelPerformance}</span>
                <ChevronDown className="h-4 w-4 shrink-0 opacity-60" />
              </summary>
              <div className="border-t border-earth px-4 py-3 text-sm">
                <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-[#1b4332]/60">
                  {t.result.validationPerformance}
                </p>
                <dl className="grid grid-cols-2 gap-3">
                  <div>
                    <dt className="text-xs text-[#1b4332]/60">{t.result.map50}</dt>
                    <dd className="font-semibold text-[#1b4332]">{formatMetric(metrics.mAP50)}</dd>
                  </div>
                  <div>
                    <dt className="text-xs text-[#1b4332]/60">{t.result.map5095}</dt>
                    <dd className="font-semibold text-[#1b4332]">{formatMetric(metrics.mAP50_95)}</dd>
                  </div>
                  <div>
                    <dt className="text-xs text-[#1b4332]/60">{t.result.precision}</dt>
                    <dd className="font-semibold text-[#1b4332]">{formatMetric(metrics.precision)}</dd>
                  </div>
                  <div>
                    <dt className="text-xs text-[#1b4332]/60">{t.result.recall}</dt>
                    <dd className="font-semibold text-[#1b4332]">{formatMetric(metrics.recall)}</dd>
                  </div>
                </dl>
              </div>
            </details>
          ) : null}

          <div>
            <p className="mb-2 text-sm font-semibold">{t.result.careGuidance}</p>
            <ul className="list-disc space-y-1 pl-5 text-sm text-[#1b4332]/80">
              {(result.care_guidance?.guidance || recommendations).map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
            {result.care_guidance?.next_step ? (
              <p className="mt-3 rounded-xl bg-emerald-50 px-3 py-2 text-sm text-[#1b4332]">
                <strong>{t.alerts.nextStep}:</strong> {result.care_guidance.next_step}
              </p>
            ) : null}
            <p className="mt-2 text-xs font-medium text-amber-900">{t.alerts.medSafety}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link
              to={`/chat?cowId=${encodeURIComponent(result.cow_id || '')}&risk=${encodeURIComponent(level)}&detection=${encodeURIComponent(findingLabel)}&confidence=${encodeURIComponent(detectionConfidence ?? '')}`}
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
          <p className="border-t border-earth pt-3 text-xs text-[#1b4332]/55">
            {t.result.screeningDisclaimer}
          </p>
          <p className="text-xs text-[#1b4332]/55">{result.disclaimer || t.disclaimer}</p>
        </div>
      </div>
    </div>
  )
}
