import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Send, Trash2 } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from '../components/Status'
import { sendChatMessage } from '../services/api'

const STORAGE_KEY = 'bovimed:chat'

export default function ChatPage() {
  const { t, lang } = useI18n()
  const [params] = useSearchParams()
  const cowId = params.get('cowId') || params.get('cow_id') || ''
  const risk = params.get('risk') || ''
  const detection = params.get('detection') || ''
  const confidence = params.get('confidence')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [typing, setTyping] = useState(false)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('fallback')
  const bottomRef = useRef(null)

  const context = useMemo(() => {
    if (!cowId && !risk && !detection) return null
    return {
      risk_level: risk || undefined,
      detection: detection || undefined,
      confidence: confidence != null ? Number(confidence) : undefined,
    }
  }, [cowId, risk, detection, confidence])

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) setMessages(JSON.parse(raw))
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.slice(-80)))
    } catch {
      // ignore
    }
  }, [messages])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typing])

  const chips = [
    { key: 'explainScan', text: t.chat.chips.explainScan },
    { key: 'whatToDo', text: t.chat.chips.whatToDo },
    { key: 'medicineSafety', text: t.chat.chips.medicineSafety },
    { key: 'prevention', text: t.chat.chips.prevention },
    { key: 'findVet', text: t.chat.chips.findVet },
    { key: 'nearbyCare', text: t.chat.chips.nearbyCare },
    { key: 'emergency', text: t.chat.chips.emergency },
    { key: 'history', text: t.chat.chips.history },
  ]

  const suggestions = [t.chat.q1, t.chat.q2, t.chat.q3, t.chat.q4, t.chat.q5, t.chat.q6, t.chat.q7, t.chat.q8]

  async function ask(text) {
    const message = String(text || '').trim()
    if (!message) return
    setError(null)
    const userMsg = { role: 'user', text: message, at: new Date().toISOString() }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setTyping(true)
    try {
      const res = await sendChatMessage({
        message,
        language: lang,
        cow_id: cowId || null,
        context,
      })
      setMode(res.mode || 'fallback')
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.answer,
          at: new Date().toISOString(),
          safety: res.safety_notice,
        },
      ])
    } catch (e) {
      setError(e.message || t.common.error)
    } finally {
      setTyping(false)
    }
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.chat.title}</h1>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.chat.subtitle}</p>
        <p className="mt-2 text-xs font-medium text-[#2d6a4f]">
          {t.langIndicator}: {lang.toUpperCase()}
        </p>
      </div>

      {context ? (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-[#1b4332]">
          <p className="font-semibold">{t.chat.contextBanner}</p>
          <p className="mt-1">
            {cowId ? `${t.dashboard.cowId}: ${cowId}` : ''}
            {risk ? ` · ${t.dashboard.risk}: ${risk}` : ''}
            {detection ? ` · ${detection}` : ''}
          </p>
        </div>
      ) : null}

      <p className="text-xs text-[#1b4332]/60">
        {mode === 'external' ? t.chat.externalNotice : t.chat.fallbackNotice}
      </p>

      <div className="flex flex-wrap gap-2">
        {chips.map((c) => (
          <button
            key={c.key}
            type="button"
            onClick={() => ask(c.text)}
            className="rounded-full border border-earth bg-white px-3 py-1.5 text-xs font-semibold text-[#1b4332]"
          >
            {c.text}
          </button>
        ))}
      </div>

      <div className="min-h-[360px] rounded-3xl border border-earth bg-white p-4 shadow-sm">
        <div className="mb-3 flex flex-wrap gap-2">
          {suggestions.slice(0, 4).map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => ask(q)}
              className="rounded-xl bg-cream px-3 py-2 text-left text-xs text-[#1b4332]"
            >
              {q}
            </button>
          ))}
        </div>

        <div className="max-h-[420px] space-y-3 overflow-y-auto pr-1">
          {messages.length === 0 ? (
            <p className="text-sm text-[#1b4332]/55">{t.chat.suggested}</p>
          ) : null}
          {messages.map((m, i) => (
            <div
              key={`${m.at}-${i}`}
              className={`max-w-[90%] rounded-2xl px-3 py-2 text-sm ${
                m.role === 'user'
                  ? 'ml-auto bg-[#1b4332] text-white'
                  : 'bg-cream text-[#1b4332]'
              }`}
            >
              <p className="whitespace-pre-wrap">{m.text}</p>
              <p className={`mt-1 text-[10px] ${m.role === 'user' ? 'text-white/70' : 'text-[#1b4332]/50'}`}>
                {new Date(m.at).toLocaleTimeString()}
              </p>
            </div>
          ))}
          {typing ? <p className="text-sm text-[#1b4332]/60">{t.chat.typing}</p> : null}
          <div ref={bottomRef} />
        </div>
      </div>

      <ErrorMessage message={error} />

      <form
        className="flex gap-2"
        onSubmit={(e) => {
          e.preventDefault()
          ask(input)
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t.chat.placeholder}
          className="flex-1 rounded-2xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
        />
        <button
          type="submit"
          className="inline-flex items-center gap-2 rounded-2xl bg-[#1b4332] px-4 py-3 font-semibold text-white"
        >
          <Send className="h-4 w-4" />
          {t.chat.send}
        </button>
        <button
          type="button"
          onClick={() => setMessages([])}
          className="rounded-2xl border border-earth bg-white px-3 py-3 text-[#1b4332]"
          aria-label={t.chat.clear}
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </form>

      <p className="text-xs text-[#1b4332]/55">{t.chat.safety}</p>
      <Link to="/veterinarians" className="text-sm font-semibold text-[#2d6a4f] underline">
        {t.nav.vets}
      </Link>
    </div>
  )
}
