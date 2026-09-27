/** Web Speech API helpers — BCP-47 codes for all BOVIMED languages. */

export const SPEECH_LOCALE_MAP = {
  en: 'en-IN',
  hi: 'hi-IN',
  kn: 'kn-IN',
  te: 'te-IN',
  ta: 'ta-IN',
  ml: 'ml-IN',
  mr: 'mr-IN',
  bn: 'bn-IN',
  gu: 'gu-IN',
  pa: 'pa-IN',
  or: 'or-IN',
  as: 'as-IN',
  ur: 'ur-IN',
  ks: 'ks-IN',
  kok: 'kok-IN',
  ne: 'ne-NP',
  sd: 'sd-IN',
  sa: 'sa-IN',
  sat: 'sat-IN',
  brx: 'brx-IN',
  doi: 'doi-IN',
  mai: 'mai-IN',
  mni: 'mni-IN',
}

export function speechLocaleForLang(lang) {
  const code = (lang || 'en').split('-')[0].toLowerCase()
  return SPEECH_LOCALE_MAP[code] || 'en-IN'
}

export function isSpeechRecognitionSupported() {
  return typeof window !== 'undefined' && !!(window.SpeechRecognition || window.webkitSpeechRecognition)
}

export function isSpeechSynthesisSupported() {
  return typeof window !== 'undefined' && !!window.speechSynthesis
}

function pickVoice(locale) {
  const voices = window.speechSynthesis?.getVoices?.() || []
  if (!voices.length) return null
  const lang = locale.toLowerCase()
  const base = lang.split('-')[0]
  return (
    voices.find((v) => v.lang?.toLowerCase() === lang) ||
    voices.find((v) => v.lang?.toLowerCase().startsWith(`${base}-`)) ||
    voices.find((v) => v.lang?.toLowerCase().startsWith(base)) ||
    voices.find((v) => v.default) ||
    voices[0]
  )
}

export function createRecognition(lang, { onResult, onError, onEnd, onStart }) {
  const Ctor = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!Ctor) return null
  const recognition = new Ctor()
  recognition.lang = speechLocaleForLang(lang)
  recognition.interimResults = false
  recognition.continuous = false
  recognition.maxAlternatives = 1
  if (onStart) recognition.onstart = onStart
  if (onResult) recognition.onresult = onResult
  if (onError) recognition.onerror = onError
  if (onEnd) recognition.onend = onEnd
  return recognition
}

export function speakText(text, lang, { onStart, onEnd, onError } = {}) {
  if (!isSpeechSynthesisSupported() || !text?.trim()) return false
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  const locale = speechLocaleForLang(lang)
  utterance.lang = locale
  const voice = pickVoice(locale)
  if (voice) utterance.voice = voice
  utterance.rate = 0.95
  utterance.onstart = () => onStart?.()
  utterance.onend = () => onEnd?.()
  utterance.onerror = (e) => onError?.(e)
  window.speechSynthesis.speak(utterance)
  return true
}

export function stopSpeaking() {
  if (!isSpeechSynthesisSupported()) return
  window.speechSynthesis.cancel()
}

export function isSpeaking() {
  return isSpeechSynthesisSupported() && window.speechSynthesis.speaking
}

/** Preload voices (Chrome loads them asynchronously). */
export function preloadVoices() {
  if (!isSpeechSynthesisSupported()) return
  window.speechSynthesis.getVoices()
  window.speechSynthesis.onvoiceschanged = () => {
    window.speechSynthesis.getVoices()
  }
}
