import { useCallback, useRef, useState } from 'react'
import { ImagePlus, Trash2, Upload } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'

const ACCEPT = 'image/jpeg,image/jpg,image/png,image/webp,.jpg,.jpeg,.png,.webp'
const MAX_MB = 10

export default function ImageUploader({ file, previewUrl, onFileChange, onClear }) {
  const { t } = useI18n()
  const inputRef = useRef(null)
  const [dragOver, setDragOver] = useState(false)
  const [localError, setLocalError] = useState(null)

  const handleFiles = useCallback(
    (list) => {
      setLocalError(null)
      const next = list?.[0]
      if (!next) return
      const okType =
        /image\/(jpeg|jpg|png|webp)/i.test(next.type) ||
        /\.(jpe?g|png|webp)$/i.test(next.name)
      if (!okType) {
        setLocalError('Please choose a JPG, PNG, or WEBP image.')
        return
      }
      if (next.size > MAX_MB * 1024 * 1024) {
        setLocalError(`Image must be under ${MAX_MB} MB.`)
        return
      }
      onFileChange(next)
    },
    [onFileChange],
  )

  return (
    <div className="space-y-3">
      {!previewUrl ? (
        <div
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') inputRef.current?.click()
          }}
          onDragOver={(e) => {
            e.preventDefault()
            setDragOver(true)
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault()
            setDragOver(false)
            handleFiles(e.dataTransfer.files)
          }}
          onClick={() => inputRef.current?.click()}
          className={`flex cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed px-6 py-14 text-center transition ${
            dragOver
              ? 'border-[#2d6a4f] bg-[#2d6a4f]/5'
              : 'border-earth bg-white hover:border-[#40916c]'
          }`}
          aria-label={t.analyze.title}
        >
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-cream text-[#2d6a4f]">
            <Upload className="h-7 w-7" />
          </div>
          <p className="font-display text-lg font-semibold text-[#1b4332]">
            {t.analyze.drop}
          </p>
          <p className="mt-1 text-sm text-[#1b4332]/70">{t.analyze.clickBrowse}</p>
          <p className="mt-3 text-xs text-[#1b4332]/50">{t.analyze.formatHint}</p>
          <button
            type="button"
            className="mt-5 inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-5 py-3 text-sm font-semibold text-white"
            onClick={(e) => {
              e.stopPropagation()
              inputRef.current?.click()
            }}
          >
            <ImagePlus className="h-4 w-4" />
            {t.analyze.browse}
          </button>
        </div>
      ) : (
        <div className="overflow-hidden rounded-3xl border border-earth bg-white shadow-sm">
          <img
            src={previewUrl}
            alt="Selected cow preview"
            className="max-h-[420px] w-full object-contain bg-stone-100"
          />
          <div className="flex items-center justify-between gap-3 px-4 py-3">
            <p className="truncate text-sm text-[#1b4332]/80">{file?.name || 'Selected image'}</p>
            <button
              type="button"
              onClick={onClear}
              className="inline-flex items-center gap-1.5 rounded-lg border border-earth px-3 py-2 text-sm font-medium text-[#1b4332] hover:bg-cream"
            >
              <Trash2 className="h-4 w-4" />
              {t.analyze.remove}
            </button>
          </div>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />

      {localError ? (
        <p role="alert" className="text-sm text-red-700">
          {localError}
        </p>
      ) : null}
    </div>
  )
}
