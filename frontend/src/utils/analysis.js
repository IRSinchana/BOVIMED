import { mediaUrl } from '../services/api'

export function riskBadgeClass(risk) {
  const key = String(risk || '').toLowerCase()
  if (key === 'healthy' || key === 'low') return 'bg-emerald-100 text-emerald-800 border-emerald-200'
  if (key === 'mild') return 'bg-amber-100 text-amber-900 border-amber-200'
  if (key === 'moderate') return 'bg-orange-100 text-orange-900 border-orange-200'
  if (key === 'high' || key === 'severe') return 'bg-red-100 text-red-800 border-red-200'
  if (key === 'critical') return 'bg-red-200 text-red-950 border-red-400'
  return 'bg-stone-100 text-stone-700 border-stone-200'
}

export function normalizeRiskLevel(risk) {
  const map = { Healthy: 'Low', Severe: 'High' }
  return map[risk] || risk || 'Low'
}

export function formatConfidence(value) {
  if (value == null || Number.isNaN(Number(value))) return '—'
  const n = Number(value)
  const pct = n <= 1 ? n * 100 : n
  return `${pct.toFixed(1)}%`
}

export function formatBBox(bbox) {
  if (!Array.isArray(bbox) || bbox.length !== 4) return null
  return bbox.map((v) => Number(v).toFixed(1)).join(', ')
}

const NO_FINDING_PREDICTIONS = new Set([
  'No Detection',
  'No Relevant Health Detection',
  'AI screening complete',
  'No clear health finding detected',
])

/** Primary detection from backend response (single source of truth). */
export function getPrimaryDetection(result) {
  if (!result) return null
  if (result.primary_finding?.class_name) return result.primary_finding
  const detections = Array.isArray(result.detections) ? result.detections : []
  if (!detections.length) return null
  return detections.reduce((best, det) => {
    if (!best) return det
    return Number(det.confidence) > Number(best.confidence) ? det : best
  }, null)
}

export function hasHealthFinding(result) {
  const primary = getPrimaryDetection(result)
  if (primary?.class_name) return true
  const prediction = String(result?.prediction || '').trim()
  return Boolean(prediction && !NO_FINDING_PREDICTIONS.has(prediction))
}

function classFindingLabel(className, t) {
  if (!className || !t?.result?.classFindings) return null
  return t.result.classFindings[className] || null
}

/** Human-readable finding label derived from backend analysis fields. */
export function getFindingDisplayLabel(result, t) {
  const primary = getPrimaryDetection(result)
  const fromClass = classFindingLabel(primary?.class_name, t)
  if (fromClass) return fromClass

  const prediction = String(result?.prediction || '').trim()
  if (prediction && !NO_FINDING_PREDICTIONS.has(prediction)) {
    return prediction
  }

  return t?.result?.noPrimaryDetected || 'No clear health finding detected.'
}

export function resolveOriginalImageSrc(result) {
  return mediaUrl(result?.image_url)
}

export function resolveAnnotatedImageSrc(result) {
  return mediaUrl(result?.annotated_image_url)
}

export const DISCLAIMER =
  'BOVIMED provides AI-assisted screening and is not a substitute for professional veterinary diagnosis. Consult a qualified veterinarian for confirmation and treatment decisions.'
