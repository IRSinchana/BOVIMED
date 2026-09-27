import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Mic, MicOff, Send, Trash2, Volume2, VolumeX } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from '../components/Status'
import { getChatStatus, sendChatMessage } from '../services/api'
import {
  createRecognition,
  isSpeechRecognitionSupported,
  isSpeechSynthesisSupported,
  isSpeaking,
  preloadVoices,
  speakText,
  stopSpeaking,
} from '../utils/speech'

const STORAGE_KEY = 'bovimed:chat'

function modeNotice(t, mode) {
  if (mode === 'external') return t.chat.externalNotice
  if (mode === 'unconfigured') return t.chat.unconfiguredNotice
  if (mode === 'error') return t.chat.errorNotice
  if (mode === 'local') return t.chat.localNotice
  return t.chat.fallbackNotice
}

function modeStatusLabel(t, mode) {
  if (mode === 'external') return t.chat.aiStatusLive
  if (mode === 'unconfigured') return t.chat.aiStatusUnconfigured
  if (mode === 'error') return t.chat.aiStatusError
  return t.chat.aiStatusLocal
}

export default function ChatPage() {
  const { t, lang, textDir } = useI18n()
  const [params] = useSearchParams()
  const cowId = params.get('cowId') || params.get('cow_id') || ''
  const risk = params.get('risk') || ''
  const detection = params.get('detection') || ''
  const confidence = params.get('confidence')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [typing, setTyping] = useState(false)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('local')
  const [listening, setListening] = useState(false)
  const [speakingId, setSpeakingId] = useState(null)
  const [speechError, setSpeechError] = useState(null)
  const recognitionRef = useRef(null)
  const listenTimeoutRef = useRef(null)
  const bottomRef = useRef(null)

  const context = useMemo(() => {
    if (!cowId && !risk && !detection && confidence == null) return null
    return {
      risk_level: risk || undefined,
      detection: detection || undefined,
      confidence: confidence != null ? Number(confidence) : undefined,
    }
  }, [cowId, risk, detection, confidence])

  useEffect(() => {
    preloadVoices()
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) setMessages(JSON.parse(raw))
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    getChatStatus()
      .then((s) => {
        if (s.configured && s.enabled) setMode('external')
        else if (s.enabled && !s.configured) setMode('unconfigured')
        else setMode('local')
      })
      .catch(() => {
        // status is optional; chat response still reports mode
      })
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

  useEffect(() => {
    return () => {
      stopSpeaking()
      recognitionRef.current?.abort?.()
      if (listenTimeoutRef.current) clearTimeout(listenTimeoutRef.current)
    }
  }, [])

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

  const ask = useCallback(
    async (text) => {
      const message = String(text || '').trim()
      if (!message) return
      setError(null)
      setSpeechError(null)
      const userMsg = { role: 'user', text: message, at: new Date().toISOString() }
      setMessages((prev) => [...prev, userMsg])
      setInput('')
      setTyping(true)
      try {
        const history = messages.slice(-12).map((m) => ({
          role: m.role,
          content: m.text,
        }))
        const res = await sendChatMessage({
          message,
          language: lang,
          cow_id: cowId || null,
          risk: risk || null,
          detection: detection || null,
          confidence: confidence != null ? Number(confidence) : null,
          context,
          history,
        })
        setMode(res.mode || 'local')
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            text: res.answer,
            at: new Date().toISOString(),
            safety: res.safety_notice,
            id: `a-${Date.now()}`,
          },
        ])
      } catch (e) {
        setError(e.message || t.common.error)
      } finally {
        setTyping(false)
      }
    },
    [messages, lang, cowId, risk, detection, confidence, context, t.common.error],
  )

  function stopListening() {
    if (listenTimeoutRef.current) {
      clearTimeout(listenTimeoutRef.current)
      listenTimeoutRef.current = null
    }
    recognitionRef.current?.stop?.()
    recognitionRef.current = null
    setListening(false)
  }

  function startListening() {
    setSpeechError(null)
    if (!isSpeechRecognitionSupported()) {
      setSpeechError(t.chat.micUnsupported)
      return
    }
    stopListening()
    const recognition = createRecognition(lang, {
      onStart: () => setListening(true),
      onResult: (event) => {
        const transcript = event.results?.[0]?.[0]?.transcript?.trim()
        stopListening()
        if (transcript) {
          setInput(transcript)
          void ask(transcript)
        } else {
          setSpeechError(t.chat.speechNoInput)
        }
      },
      onError: (event) => {
        stopListening()
        const code = event?.error
        if (code === 'not-allowed' || code === 'service-not-allowed') {
          setSpeechError(t.chat.micDenied)
        } else if (code === 'no-speech') {
          setSpeechError(t.chat.speechNoInput)
        } else if (code === 'language-not-supported') {
          setSpeechError(t.chat.speechLangUnavailable)
        } else {
          setSpeechError(t.chat.speechError)
        }
      },
      onEnd: () => setListening(false),
    })
    if (!recognition) {
      setSpeechError(t.chat.micUnsupported)
      return
    }
    recognitionRef.current = recognition
    listenTimeoutRef.current = setTimeout(() => {
      stopListening()
      setSpeechError(t.chat.speechTimeout)
    }, 15000)
    try {
      recognition.start()
    } catch {
      stopListening()
      setSpeechError(t.chat.speechError)
    }
  }

  function toggleMic() {
    if (listening) {
      stopListening()
      return
    }
    startListening()
  }

  function handleSpeak(messageId, text) {
    if (!isSpeechSynthesisSupported()) {
      setSpeechError(t.chat.ttsUnsupported)
      return
    }
    if (speakingId === messageId && isSpeaking()) {
      stopSpeaking()
      setSpeakingId(null)
      return
    }
    stopSpeaking()
    const ok = speakText(text, lang, {
      onStart: () => setSpeakingId(messageId),
      onEnd: () => setSpeakingId(null),
      onError: () => {
        setSpeakingId(null)
        setSpeechError(t.chat.ttsUnsupported)
      },
    })
    if (!ok) setSpeechError(t.chat.ttsUnsupported)
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4">
      <div dir={textDir}>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.chat.title}</h1>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.chat.subtitle}</p>
        <div className="mt-2 flex flex-wrap items-center gap-2 text-xs font-medium text-[#2d6a4f]">
          <span>{t.langIndicator}: {lang.toUpperCase()}</span>
          <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[#1b4332]">
            {modeStatusLabel(t, mode)}
          </span>
        </div>
      </div>

      {context ? (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-[#1b4332]" dir={textDir}>
          <p className="font-semibold">{t.chat.contextBanner}</p>
          <p className="mt-1">
            {cowId ? `${t.dashboard.cowId}: ${cowId}` : ''}
            {risk ? ` · ${t.dashboard.risk}: ${risk}` : ''}
            {detection ? ` · ${detection}` : ''}
          </p>
        </div>
      ) : null}

      <p className="text-xs text-[#1b4332]/60" dir={textDir}>{modeNotice(t, mode)}</p>

      <div className="flex flex-wrap gap-2" dir={textDir}>
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
        <div className="mb-3 flex flex-wrap gap-2" dir={textDir}>
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
            <p className="text-sm text-[#1b4332]/55" dir={textDir}>{t.chat.suggested}</p>
          ) : null}
          {messages.map((m, i) => (
            <div
              key={`${m.at}-${i}`}
              className={`max-w-[90%] rounded-2xl px-3 py-2 text-sm ${
                m.role === 'user'
                  ? 'ml-auto bg-[#1b4332] text-white'
                  : 'bg-cream text-[#1b4332]'
              }`}
              dir={textDir}
            >
              <p className="whitespace-pre-wrap">{m.text}</p>
              <div
                className={`mt-1 flex items-center justify-between gap-2 text-[10px] ${
                  m.role === 'user' ? 'text-white/70' : 'text-[#1b4332]/50'
                }`}
              >
                <span>{new Date(m.at).toLocaleTimeString()}</span>
                {m.role === 'assistant' ? (
                  <button
                    type="button"
                    onClick={() => handleSpeak(m.id || `msg-${i}`, m.text)}
                    className="inline-flex items-center gap-1 rounded-full bg-white/80 px-2 py-0.5 text-[10px] font-semibold text-[#1b4332]"
                  >
                    {speakingId === (m.id || `msg-${i}`) && isSpeaking() ? (
                      <>
                        <VolumeX className="h-3 w-3" />
                        {t.chat.stopSpeaking}
                      </>
                    ) : (
                      <>
                        <Volume2 className="h-3 w-3" />
                        {t.chat.speak}
                      </>
                    )}
                  </button>
                ) : null}
              </div>
            </div>
          ))}
          {typing ? <p className="text-sm text-[#1b4332]/60" dir={textDir}>{t.chat.typing}</p> : null}
          {listening ? (
            <p className="text-sm font-medium text-[#2d6a4f]" dir={textDir}>
              {t.chat.listening}
            </p>
          ) : null}
          <div ref={bottomRef} />
        </div>
      </div>

      <ErrorMessage message={error} />
      {speechError ? <ErrorMessage message={speechError} /> : null}

      <form
        className="flex gap-2"
        onSubmit={(e) => {
          e.preventDefault()
          ask(input)
        }}
      >
        <button
          type="button"
          onClick={toggleMic}
          aria-label={listening ? t.chat.stopSpeaking : t.chat.listening}
          className={`inline-flex items-center justify-center rounded-2xl border px-3 py-3 ${
            listening
              ? 'border-red-300 bg-red-50 text-red-700'
              : 'border-earth bg-white text-[#1b4332]'
          }`}
        >
          {listening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
        </button>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={listening ? t.chat.listening : t.chat.placeholder}
          className="flex-1 rounded-2xl border border-earth px-4 py-3 outline-none focus:border-[#2d6a4f]"
          dir={textDir}
        />
        <button
          type="submit"
          disabled={typing || !input.trim()}
          className="inline-flex items-center gap-2 rounded-2xl bg-[#1b4332] px-4 py-3 font-semibold text-white disabled:opacity-60"
        >
          <Send className="h-4 w-4" />
          {t.chat.send}
        </button>
        <button
          type="button"
          onClick={() => {
            stopSpeaking()
            setMessages([])
          }}
          className="rounded-2xl border border-earth bg-white px-3 py-3 text-[#1b4332]"
          aria-label={t.chat.clear}
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </form>

      <p className="text-xs text-[#1b4332]/55" dir={textDir}>{t.chat.safety}</p>
      <Link to="/veterinarians" className="text-sm font-semibold text-[#2d6a4f] underline" dir={textDir}>
        {t.nav.vets}
      </Link>
    </div>
  )
}
