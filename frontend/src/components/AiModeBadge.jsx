import { Link } from 'react-router-dom'
import { Activity } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'

export default function AiModeBadge({ health, compact = false }) {
  const { t } = useI18n()
  if (!health) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full border border-earth bg-white px-3 py-1 text-xs font-medium text-[#1b4332]/70">
        {t.common.loading}
      </span>
    )
  }

  if (health.demo_mode) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-300 bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-900">
        {t.demoMode}
      </span>
    )
  }

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border border-emerald-300 bg-emerald-50 font-semibold text-emerald-900 ${
        compact ? 'px-2.5 py-1 text-xs' : 'px-3 py-1.5 text-xs sm:text-sm'
      }`}
      title={health.message || 'Real YOLO11'}
    >
      <Activity className="h-3.5 w-3.5" aria-hidden />
      {t.liveAi}
    </span>
  )
}

export function BrandMark({ to = '/dashboard', light = false }) {
  return (
    <Link to={to} className="flex items-center gap-2 no-underline">
      <span
        className={`flex h-9 w-9 items-center justify-center rounded-xl text-sm font-bold ${
          light ? 'bg-white text-[#1b4332]' : 'bg-[#1b4332] text-white'
        }`}
      >
        BM
      </span>
      <span
        className={`font-display text-lg font-bold tracking-tight ${
          light ? 'text-white' : 'text-[#1b4332]'
        }`}
      >
        BOVIMED
      </span>
    </Link>
  )
}

