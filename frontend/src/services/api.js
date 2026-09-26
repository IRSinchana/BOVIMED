/**
 * BOVIMED API client — FastAPI at VITE_API_BASE_URL.
 */

const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(
  /\/$/,
  '',
)

const TOKEN_KEY = 'bovimed:token'

export function getApiBase() {
  return API_BASE
}

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    // ignore
  }
}

export function mediaUrl(path) {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return `${API_BASE}${path.startsWith('/') ? path : `/${path}`}`
}

async function parseError(response) {
  let detail = `Request failed (${response.status})`
  try {
    const data = await response.json()
    if (typeof data.detail === 'string') detail = data.detail
    else if (Array.isArray(data.detail))
      detail = data.detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
    else if (data.message) detail = data.message
  } catch {
    // keep default
  }
  const err = new Error(detail)
  err.status = response.status
  return err
}

function authHeaders(extra = {}) {
  const token = getToken()
  return {
    ...extra,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: authHeaders(options.headers || {}),
  })
  if (!res.ok) throw await parseError(res)
  if (res.status === 204) return null
  return res.json()
}

export async function getHealth() {
  return apiFetch('/api/health')
}

export async function registerFarmer(payload) {
  return apiFetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function loginFarmer(payload) {
  return apiFetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function fetchMe() {
  return apiFetch('/api/auth/me')
}

export async function logoutFarmer() {
  try {
    await apiFetch('/api/auth/logout', { method: 'POST' })
  } catch {
    // still clear local token
  } finally {
    setToken(null)
  }
}

export async function updateProfile(payload) {
  return apiFetch('/api/auth/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function analyzeImage(image, options = {}) {
  const form = new FormData()
  const filename = options.filename || image.name || 'capture.jpg'
  form.append('image', image, filename)
  if (options.cowId && String(options.cowId).trim()) {
    form.append('cow_id', String(options.cowId).trim())
  }
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
  if (!res.ok) throw await parseError(res)
  return res.json()
}

export async function getDashboard() {
  return apiFetch('/api/dashboard')
}

export async function listCows() {
  return apiFetch('/api/cows')
}

export async function listAlerts() {
  return apiFetch('/api/alerts')
}

export async function sendChatMessage(payload) {
  return apiFetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function searchVeterinarians(payload) {
  return apiFetch('/api/veterinarians/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function getChatHistory({ cowId, limit = 50 } = {}) {
  const params = new URLSearchParams()
  if (cowId) params.set('cow_id', cowId)
  if (limit) params.set('limit', limit)
  const qs = params.toString()
  return apiFetch(`/api/chat/history${qs ? `?${qs}` : ''}`)
}

export async function clearChatHistory({ cowId } = {}) {
  const params = new URLSearchParams()
  if (cowId) params.set('cow_id', cowId)
  const qs = params.toString()
  return apiFetch(`/api/chat/history${qs ? `?${qs}` : ''}`, { method: 'DELETE' })
}

export async function listHistory() {
  return apiFetch('/api/history')
}

export async function listCowAlerts(cowId) {
  return apiFetch(`/api/cows/${cowId}/alerts`)
}

export async function dismissAlert(alertId) {
  return apiFetch(`/api/alerts/${alertId}/dismiss`, { method: 'POST' })
}

