import { Link, useLocation, useOutletContext } from 'react-router-dom'
import AnalysisResult from '../components/AnalysisResult'
import { useI18n } from '../i18n/I18nContext'

export default function ResultPage() {
  const { t } = useI18n()
  const location = useLocation()
  const { health } = useOutletContext()
  const result = location.state?.result
  const localPreviewUrl = location.state?.localPreviewUrl

  if (!result) {
    return (
      <div className="mx-auto max-w-lg space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold text-[#1b4332]">{t.result.title}</h1>
        <p className="text-[#1b4332]/70">{t.dashboard.empty}</p>
        <div className="flex justify-center gap-3">
          <Link
            to="/analyze"
            className="rounded-xl bg-[#1b4332] px-5 py-3 text-sm font-semibold text-white"
          >
            {t.nav.analyze}
          </Link>
          <Link
            to="/camera"
            className="rounded-xl border border-earth bg-white px-5 py-3 text-sm font-semibold text-[#1b4332]"
          >
            {t.nav.camera}
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-3">
        <Link
          to="/analyze"
          className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]"
        >
          {t.result.newUpload}
        </Link>
        <Link
          to="/camera"
          className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#1b4332]"
        >
          {t.result.newCamera}
        </Link>
        <Link
          to="/dashboard"
          className="rounded-xl bg-[#1b4332] px-4 py-2 text-sm font-semibold text-white"
        >
          {t.nav.dashboard}
        </Link>
      </div>
      <AnalysisResult result={result} localPreviewUrl={localPreviewUrl} health={health} />
    </div>
  )
}
