import { useEffect, useState } from 'react'
import { ImageOff } from 'lucide-react'

/**
 * Image with graceful fallback when the URL fails to load.
 * Resets error state when `src` changes.
 */
export default function AnalysisImage({
  src,
  alt = '',
  className = 'max-h-80 w-full object-contain bg-stone-100',
  fallbackLabel,
  onLoad,
  children,
}) {
  const [failed, setFailed] = useState(false)
  const [attemptedUrl, setAttemptedUrl] = useState('')

  useEffect(() => {
    setFailed(false)
    setAttemptedUrl(src || '')
  }, [src])

  if (!src || failed) {
    return (
      <div
        className="flex min-h-[12rem] flex-col items-center justify-center gap-2 bg-stone-100 px-4 py-8 text-center"
        role="img"
        aria-label={fallbackLabel || alt || 'Image unavailable'}
      >
        <ImageOff className="h-8 w-8 text-[#1b4332]/35" aria-hidden />
        <p className="text-sm font-medium text-[#1b4332]/60">
          {fallbackLabel || 'Image unavailable'}
        </p>
        {import.meta.env.DEV && attemptedUrl ? (
          <p className="mt-1 max-w-full break-all text-[10px] text-[#1b4332]/45">
            Attempted: {attemptedUrl}
          </p>
        ) : null}
      </div>
    )
  }

  return (
    <div className="relative bg-stone-100">
      <img
        src={src}
        alt={alt}
        className={className}
        onLoad={onLoad}
        onError={() => {
          if (import.meta.env.DEV) {
            console.warn('[BOVIMED] Image failed to load:', src)
          }
          setFailed(true)
        }}
      />
      {children}
    </div>
  )
}
