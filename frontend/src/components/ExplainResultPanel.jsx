import { useState } from 'react'
import { Loader2, Sparkles } from 'lucide-react'
import { sendChatMessage } from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from './Status'

export default function ExplainResultPanel({ result }) {
  const { t, lang, textDir } = useI18n()
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  if (!result) return null

  const level = normalizeRiskLevel(result.risk_level)
  const primary = result.primary_finding
  const detectionName = primary?.class_name || result.prediction || ''
  const detectionConfidence = primary?.confidence ?? result.confidence

  async function explain() {
    setLoading(true)
    setError(null)
    const prompt = [
      `Explain this BOVIMED cow scan to a dairy farmer in simple language.`,
      `Cow ID: ${result.cow_id || 'unknown'}`,
      `Finding: ${result.prediction || 'none'}`,
      `YOLO detection: ${detectionName}`,
      `Detection confidence: ${formatConfidence(detectionConfidence)}`,
      `Risk level: ${level}`,
      result.risk_explanation ? `Risk note: ${result.risk_explanation}` : '',
      `Do not diagnose with certainty. Do not prescribe medication. Recommend veterinary care when appropriate.`,
    ]
      .filter(Boolean)
      .join('\n')

    try {
      const res = await sendChatMessage({
        message: prompt,
        language: lang,
        cow_id: result.cow_id || null,
        risk: level,
        detection: result.prediction || detectionName,
        confidence: detectionConfidence,
        context: {
          risk_level: level,
          detection: result.prediction || detectionName,
          confidence: detectionConfidence,
        },
      })
      setExplanation(res.answer)
    } catch (e) {
      setError(e.message || t.common.error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="rounded-2xl border border-[#2d6a4f]/30 bg-gradient-to-br from-emerald-50 to-white p-5 shadow-sm" dir={textDir}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide text-[#2d6a4f]">{t.result.explainTitle}</p>
          <p className="mt-1 text-sm text-[#1b4332]/70">{t.result.explainSubtitle}</p>
        </div>
        <button
          type="button"
          onClick={explain}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#2d6a4f] disabled:opacity-60"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
          {loading ? t.result.explaining : t.result.explainAction}
        </button>
      </div>

      {result.risk_explanation ? (
        <p className="mt-4 rounded-xl bg-white/80 px-4 py-3 text-sm text-[#1b4332]/85">{result.risk_explanation}</p>
      ) : null}

      {result.care_guidance?.next_step ? (
        <div className="mt-3 rounded-xl border border-earth bg-cream/50 px-4 py-3 text-sm">
          <p className="font-semibold text-[#1b4332]">{t.alerts.nextStep}</p>
          <p className="mt-1 text-[#1b4332]/85">{result.care_guidance.next_step}</p>
        </div>
      ) : null}

      <ErrorMessage message={error} />

      {explanation ? (
        <div className="mt-4 rounded-xl border border-earth bg-white px-4 py-3 text-sm whitespace-pre-wrap text-[#1b4332]">
          {explanation}
        </div>
      ) : null}
    </section>
  )
}
