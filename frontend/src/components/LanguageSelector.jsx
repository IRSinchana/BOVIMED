import { useState, useRef, useEffect } from 'react'
import { Globe, Check, ChevronDown } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { normalizeLocaleCode } from '../i18n/languages'

export default function LanguageSelector({ compact = false }) {
  const { lang, setLang, languages } = useI18n()
  const [open, setOpen] = useState(false)
  const menuRef = useRef(null)

  const current = languages.find((l) => l.code === lang) || languages[0]

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative inline-block text-left" ref={menuRef} dir="ltr">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="inline-flex items-center gap-2 rounded-xl border border-earth bg-white/90 px-3 py-2 text-xs font-semibold text-[#1b4332] shadow-sm transition hover:bg-cream/60 focus:outline-none"
        aria-expanded={open}
        aria-label="Select language"
      >
        <Globe className="h-4 w-4 text-[#2d6a4f]" />
        <span className="font-medium text-[#1b4332]">{current.native}</span>
        {!compact ? (
          <span className="hidden text-[10px] text-[#1b4332]/60 sm:inline">
            ({current.englishName || current.label})
          </span>
        ) : null}
        <ChevronDown
          className={`h-3.5 w-3.5 text-[#1b4332]/60 transition-transform ${open ? 'rotate-180' : ''}`}
        />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 z-50 max-h-80 w-64 overflow-y-auto rounded-2xl border border-earth bg-white p-1.5 shadow-xl ring-1 ring-black/5">
          <div className="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-[#1b4332]/50 border-b border-earth/50">
            22 Indian Languages (22 भारतीय भाषाएं)
          </div>
          <div className="mt-1 space-y-0.5">
            {languages.map((l) => {
              const active = l.code === lang
              return (
                <button
                  key={l.code}
                  type="button"
                  onClick={() => {
                    setLang(normalizeLocaleCode(l.code))
                    setOpen(false)
                  }}
                  className={`flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs transition ${
                    active
                      ? 'bg-[#1b4332] text-white font-semibold'
                      : 'text-[#1b4332] hover:bg-cream'
                  }`}
                >
                  <div className="flex flex-col">
                    <span className="text-sm font-medium">{l.native}</span>
                    <span className={`text-[10px] ${active ? 'text-white/80' : 'text-[#1b4332]/60'}`}>
                      {l.englishName || l.label}
                    </span>
                  </div>
                  {active && <Check className="h-4 w-4 shrink-0 text-white" />}
                </button>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
