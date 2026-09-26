/** @deprecated Prefer useI18n().t.risk — kept for older imports */
export function translateRisk(t, risk) {
  const map = { Healthy: 'Low', Severe: 'High' }
  const level = map[risk] || risk
  return t?.risk?.[level] || t?.risk?.[risk] || level
}

export { LANGUAGE_OPTIONS as LANG_META } from './index'
