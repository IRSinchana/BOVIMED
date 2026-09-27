import { useCallback, useEffect, useState } from 'react'
import { Link, useOutletContext, useParams } from 'react-router-dom'
import AnalysisResult from '../components/AnalysisResult'
import { ErrorMessage } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import { getAnalysis } from '../services/api'

export default function ResultPage() {
  const { t } = useI18n()
  const { analysisId } = useParams()
  const { health } = useOutletContext()
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(Boolean(analysisId))

  const loadResult = useCallback(async () => {
    if (!analysisId) {
      setError(t.common.error)
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const data = await getAnalysis(analysisId)
      setResult(data)
    } catch (e) {
      setResult(null)
      if (e?.isNetworkError) {
        setError(t.common.backendDown)
      } else {
        setError(e?.message || t.common.error)
      }
    } finally {
      setLoading(false)
    }
  }, [analysisId, t.common.backendDown, t.common.error])

  useEffect(() => {
    loadResult()
  }, [loadResult])

  if (loading) {
    return (
      <div className="rounded-3xl border border-earth bg-white p-8 text-center shadow-sm">
        <p className="text-sm text-[#1b4332]/70">{t.common.loading}</p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="mx-auto max-w-lg space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold text-[#1b4332]">{t.result.title}</h1>
        <ErrorMessage message={error || t.common.error} />
        <p className="text-[#1b4332]/70">{t.dashboard.empty}</p>
        <div className="flex flex-wrap justify-center gap-3">
          <button
            type="button"
            onClick={loadResult}
            className="rounded-xl border border-earth bg-white px-5 py-3 text-sm font-semibold text-[#1b4332]"
          >
            {t.common.retry}
          </button>
          <Link to="/dashboard" className="rounded-xl bg-[#1b4332] px-5 py-3 text-sm font-semibold text-white">
            {t.nav.dashboard}
          </Link>
          <Link to="/analyze" className="rounded-xl border border-earth bg-white px-5 py-3 text-sm font-semibold text-[#1b4332]">
            {t.nav.analyze}
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-3">
        <Link to="/analyze" className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]">
          {t.result.newUpload}
        </Link>
        <Link to="/camera" className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]">
          {t.result.newCamera}
        </Link>
        {result.cow_id ? (
          <Link
            to={`/cows/${encodeURIComponent(result.cow_id)}`}
            className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]"
          >
            {t.cowProfile.viewProfile}
          </Link>
        ) : null}
        <Link to="/history" className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]">
          {t.nav.history}
        </Link>
        <Link to="/dashboard" className="rounded-xl bg-[#1b4332] px-4 py-2 text-sm font-semibold text-white">
          {t.nav.dashboard}
        </Link>
      </div>
      <AnalysisResult result={result} health={health} />
    </div>
  )
}
