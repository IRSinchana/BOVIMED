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

export const DISCLAIMER =
  'BOVIMED provides AI-assisted screening and is not a substitute for professional veterinary diagnosis. Consult a qualified veterinarian for confirmation and treatment decisions.'
