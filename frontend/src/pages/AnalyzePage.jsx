import { useEffect, useState } from 'react'
import { useNavigate, useOutletContext } from 'react-router-dom'
import AnalysisResult from '../components/AnalysisResult'
import ImageUploader from '../components/ImageUploader'
import AiModeBadge from '../components/AiModeBadge'
import { ErrorMessage, LoadingOverlay } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { analyzeImage, getHealth } from '../services/api'

export default function AnalyzePage() {
  const { t } = useI18n()
  const navigate = useNavigate()
  const { health, setHealth } = useOutletContext()
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [cowId, setCowId] = useState('')
  const [loading, setLoading] = useState(false)
  const [stepIndex, setStepIndex] = useState(0)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const STEPS = [
    t.analyze.analyzing,
    t.analyze.stepScan || 'AI Scan',
    t.dashboard.risk,
    t.result.recommendations,
  ]

  useEffect(() => {
    getHealth()
      .then((h) => setHealth?.(h))
      .catch(() => {})
  }, [setHealth])

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl)
    }
  }, [previewUrl])

  useEffect(() => {
    if (!loading) return undefined
    setStepIndex(0)
    const timers = [
      setTimeout(() => setStepIndex(1), 400),
      setTimeout(() => setStepIndex(2), 1200),
      setTimeout(() => setStepIndex(3), 2000),
    ]
    return () => timers.forEach(clearTimeout)
  }, [loading])

  function onFileChange(next) {
    setResult(null)
    setError(null)
    setFile(next)
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return URL.createObjectURL(next)
    })
  }

  function onClear() {
    setFile(null)
    setResult(null)
    setError(null)
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return null
    })
  }

  async function onAnalyze() {
    if (!file) {
      setError(t.analyze.noImage)
      return
    }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await analyzeImage(file, { cowId })
      setResult(data)
      navigate('/result', { state: { result: data } })
    } catch (e) {
      setError(e.message || t.common.backendDown)
    } finally {
      setLoading(false)
      setStepIndex(0)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="font-display text-3xl font-bold text-[#1b4332]">
            {t.analyze.title}
          </h1>
          <p className="mt-1 text-[#1b4332]/70">{t.analyze.subtitle}</p>
        </div>
        <AiModeBadge health={health} />
      </div>

      <div className="overflow-hidden rounded-3xl border border-earth">
        <img src="/farm-hero.svg" alt="" className="h-28 w-full object-cover opacity-40" />
      </div>

      <label className="block">
        <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">
          {t.analyze.cowId}
        </span>
        <input
          type="text"
          value={cowId}
          onChange={(e) => setCowId(e.target.value)}
          placeholder="e.g. COW-001"
          className="w-full rounded-xl border border-earth bg-white px-4 py-3 text-base outline-none focus:border-[#2d6a4f]"
        />
      </label>

      <ImageUploader
        file={file}
        previewUrl={previewUrl}
        onFileChange={onFileChange}
        onClear={onClear}
      />

      <ErrorMessage message={error} />
      {loading ? <LoadingOverlay steps={STEPS} activeIndex={stepIndex} /> : null}

      <button
        type="button"
        disabled={loading || !file}
        onClick={onAnalyze}
        className="w-full rounded-2xl bg-[#1b4332] px-6 py-4 text-base font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? t.analyze.analyzing : t.analyze.analyzeBtn}
      </button>

      {result && !loading ? (
        <AnalysisResult result={result} localPreviewUrl={previewUrl} health={health} />
      ) : null}
    </div>
  )
}
