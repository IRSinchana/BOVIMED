import { formatConfidence, riskBadgeClass } from '../utils/analysis'

export function RiskBadge({ risk, label }) {
  return (
    <span
      className={`inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${riskBadgeClass(risk)}`}
    >
      {label || risk || 'Unknown'}
    </span>
  )
}

export function ConfidenceBar({ value, label = 'AI Confidence' }) {
  const pct = value == null ? 0 : value <= 1 ? value * 100 : value
  return (
    <div className="w-full">
      <div className="mb-1 flex justify-between text-sm">
        <span className="text-[#1b4332]/70">{label}</span>
        <span className="font-semibold text-[#1b4332]">{formatConfidence(value)}</span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-earth/60">
        <div
          className="h-full rounded-full bg-[#2d6a4f] transition-all duration-500"
          style={{ width: `${Math.min(100, Math.max(0, pct))}%` }}
        />
      </div>
    </div>
  )
}

export function ErrorMessage({ message, onRetry }) {
  if (!message) return null
  return (
    <div
      role="alert"
      className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-900"
    >
      <p className="font-medium">{message}</p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 text-sm font-semibold text-red-800 underline"
        >
          Try again
        </button>
      ) : null}
    </div>
  )
}

export function LoadingOverlay({ steps = [], activeIndex = 0, title = 'AI Scan', subtitle = 'Checking your cow photo…' }) {
  return (
    <div className="rounded-2xl border border-earth bg-white p-6 shadow-sm">
      <p className="font-display text-lg font-semibold text-[#1b4332]">{title}</p>
      <p className="mt-1 text-sm text-[#1b4332]/70">{subtitle}</p>
      <ul className="mt-5 space-y-3">
        {steps.map((step, i) => {
          const done = i < activeIndex
          const active = i === activeIndex
          return (
            <li key={`${step}-${i}`} className="flex items-center gap-3 text-sm">
              <span
                className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${
                  done
                    ? 'bg-[#2d6a4f] text-white'
                    : active
                      ? 'animate-pulse bg-[#40916c] text-white'
                      : 'bg-[#d8cfc4] text-[#1b4332]/50'
                }`}
              >
                {done ? '✓' : active ? '●' : '○'}
              </span>
              <span className={active || done ? 'text-[#1b4332]' : 'text-[#1b4332]/50'}>
                {step}
              </span>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
