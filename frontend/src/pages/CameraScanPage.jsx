import { useEffect, useState } from 'react'
import { Link, useNavigate, useOutletContext } from 'react-router-dom'
import { Camera, RefreshCcw, ScanLine, Square } from 'lucide-react'
import AiModeBadge from '../components/AiModeBadge'
import { ErrorMessage, LoadingOverlay } from '../components/Status'
import { useCamera } from '../hooks/useCamera'
import { useI18n } from '../i18n/I18nContext'
import { analyzeImage, getHealth } from '../services/api'

export default function CameraScanPage() {
  const { t } = useI18n()
  const navigate = useNavigate()
  const { health, setHealth } = useOutletContext()
  const {
    videoRef,
    isOpen,
    error: cameraError,
    setError: setCameraError,
    capturedUrl,
    capturedBlob,
    openCamera,
    stopCamera,
    captureImage,
    retake,
  } = useCamera()

  const [cowId, setCowId] = useState('')
  const [loading, setLoading] = useState(false)
  const [stepIndex, setStepIndex] = useState(0)
  const [analyzeError, setAnalyzeError] = useState(null)

  const STEPS = [t.analyze.analyzing, t.analyze.stepScan || 'AI Scan', t.dashboard.risk, t.result.recommendations]

  useEffect(() => {
    getHealth()
      .then((h) => setHealth?.(h))
      .catch(() => {})
    return () => stopCamera()
  }, [setHealth, stopCamera])

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

  async function onCapture() {
    setAnalyzeError(null)
    await captureImage()
  }

  async function onAnalyze() {
    if (!capturedBlob) {
      setAnalyzeError(t.analyze.noImage)
      return
    }
    setLoading(true)
    setAnalyzeError(null)
    stopCamera()
    try {
      const data = await analyzeImage(capturedBlob, {
        cowId,
        filename: 'camera-capture.jpg',
      })
      navigate(`/result/${data.analysis_id}`, { state: { result: data } })
    } catch (e) {
      let message = e?.message || t.common.backendDown
      if (e?.isTimeoutError) {
        message = 'Starting BOVIMED AI service… This may take a few seconds. Please wait a moment and try again.'
      } else if (e?.isNetworkError) {
        message = 'Unable to reach the BOVIMED server. Please check your connection and try again.'
      } else if (e?.status === 401) {
        message = 'Please log in again to continue.'
      } else if (e?.status === 404) {
        message = 'AI scan endpoint is unavailable. Please try again in a moment.'
      } else if (e?.status >= 500) {
        message = 'The AI scan failed on the server. Please try again in a moment.'
      } else if (e?.isValidationError) {
        message = 'Image validation failed. Please try a different cow photo.'
      }
      setAnalyzeError(message)
    } finally {
      setLoading(false)
      setStepIndex(0)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.camera.title}</h1>
          <p className="mt-1 text-[#1b4332]/70">{t.camera.subtitle}</p>
        </div>
        <AiModeBadge health={health} />
      </div>

      <label className="block">
        <span className="mb-1.5 block text-sm font-medium text-[#1b4332]">{t.analyze.cowId}</span>
        <input
          type="text"
          value={cowId}
          onChange={(e) => setCowId(e.target.value)}
          placeholder="e.g. COW-001"
          className="w-full rounded-xl border border-earth bg-white px-4 py-3 text-base outline-none focus:border-[#2d6a4f]"
        />
      </label>

      <div className="overflow-hidden rounded-3xl border border-earth bg-stone-900 shadow-sm">
        {capturedUrl ? (
          <img src={capturedUrl} alt="Captured" className="max-h-[480px] w-full object-contain" />
        ) : (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className={`max-h-[480px] w-full object-contain ${isOpen ? 'block' : 'hidden'}`}
          />
        )}
        {!isOpen && !capturedUrl ? (
          <div className="flex h-64 flex-col items-center justify-center gap-3 px-6 text-center text-white/80">
            <Camera className="h-10 w-10 opacity-70" />
            <p>{t.camera.open}</p>
          </div>
        ) : null}
      </div>

      <ErrorMessage
        message={cameraError || analyzeError}
        onRetry={
          cameraError
            ? () => {
                setCameraError(null)
                openCamera()
              }
            : undefined
        }
      />

      {loading ? (
        <LoadingOverlay
          steps={STEPS}
          activeIndex={stepIndex}
          title="Starting BOVIMED AI service…"
          subtitle="This may take a few seconds while the AI service wakes up."
        />
      ) : null}

      <div className="flex flex-wrap gap-3">
        {!isOpen && !capturedUrl ? (
          <button
            type="button"
            onClick={openCamera}
            className="inline-flex min-w-[140px] flex-1 items-center justify-center gap-2 rounded-2xl bg-[#1b4332] px-5 py-4 text-base font-semibold text-white"
          >
            <Camera className="h-5 w-5" />
            {t.camera.open}
          </button>
        ) : null}

        {isOpen && !capturedUrl ? (
          <>
            <button
              type="button"
              onClick={onCapture}
              className="inline-flex min-w-[140px] flex-1 items-center justify-center gap-2 rounded-2xl bg-[#2d6a4f] px-5 py-4 text-base font-semibold text-white"
            >
              <ScanLine className="h-5 w-5" />
              {t.camera.capture}
            </button>
            <button
              type="button"
              onClick={stopCamera}
              className="inline-flex items-center justify-center gap-2 rounded-2xl border border-earth bg-white px-5 py-4 text-base font-semibold text-[#1b4332]"
            >
              <Square className="h-5 w-5" />
              {t.camera.close}
            </button>
          </>
        ) : null}

        {capturedUrl ? (
          <>
            <button
              type="button"
              onClick={retake}
              disabled={loading}
              className="inline-flex min-w-[140px] flex-1 items-center justify-center gap-2 rounded-2xl border border-earth bg-white px-5 py-4 text-base font-semibold text-[#1b4332]"
            >
              <RefreshCcw className="h-5 w-5" />
              {t.camera.retake}
            </button>
            <button
              type="button"
              onClick={onAnalyze}
              disabled={loading}
              className="inline-flex min-w-[140px] flex-1 items-center justify-center gap-2 rounded-2xl bg-[#1b4332] px-5 py-4 text-base font-semibold text-white"
            >
              {t.camera.analyze}
            </button>
          </>
        ) : null}
      </div>

      <p className="text-sm text-[#1b4332]/60">
        {t.camera.permission}{' '}
        <Link to="/analyze" className="font-semibold text-[#2d6a4f] underline">
          {t.camera.useUpload}
        </Link>
        .
      </p>
    </div>
  )
}
