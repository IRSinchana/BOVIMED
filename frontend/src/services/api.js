/**
 * BOVIMED API client — FastAPI at VITE_API_BASE_URL.
 *
 * Local dev (`npm run dev`): same-origin /api and /media are proxied to :8000 (vite.config.js).
 * Production (Vercel): set VITE_API_BASE_URL=https://bovimed.onrender.com at build time.
 */

const DEFAULT_PROD_API_BASE = 'https://bovimed.onrender.com'
const CONFIGURED_API_BASE = (import.meta.env.VITE_API_BASE_URL || '').trim().replace(/\/+$/, '')

function resolveApiBase() {
  if (import.meta.env.PROD) {
    if (CONFIGURED_API_BASE && !/localhost|127\.0\.0\.1/i.test(CONFIGURED_API_BASE)) {
      return CONFIGURED_API_BASE
    }
    return DEFAULT_PROD_API_BASE
  }

  // Dev against deployed Render API (optional).
  if (CONFIGURED_API_BASE && /onrender\.com/i.test(CONFIGURED_API_BASE)) {
    return CONFIGURED_API_BASE
  }

  // Local dev: use VITE_API_BASE_URL when set, otherwise a local backend default.
  return CONFIGURED_API_BASE || 'http://127.0.0.1:8000'
}

const API_BASE = resolveApiBase()

const TOKEN_KEY = 'bovimed:token'

/** True when the frontend calls a deployed API (e.g. Render), not the local Vite proxy. */
export function isRemoteApiBase() {
  return Boolean(API_BASE) && /onrender\.com/i.test(API_BASE)
}

export function getApiBase() {
  return API_BASE
}

/** Normalize backend image paths to /media/uploads|results/<filename>. */
export function resolveMediaRelativePath(path) {
  if (!path) return null
  if (path.startsWith('blob:')) return path
  if (path.startsWith('http://') || path.startsWith('https://')) {
    try {
      const { pathname } = new URL(path)
      if (pathname.startsWith('/media/')) return pathname
    } catch {
      return path
    }
    return path
  }

  const normalized = String(path).replace(/\\/g, '/')
  if (normalized.startsWith('/media/')) return normalized

  const uploadsMatch = normalized.match(/\/uploads\/([^/]+)$/)
  if (uploadsMatch) return `/media/uploads/${uploadsMatch[1]}`

  const resultsMatch = normalized.match(/\/results\/([^/]+)$/)
  if (resultsMatch) return `/media/results/${resultsMatch[1]}`

  const name = normalized.split('/').pop()
  if (!name) return null
  return normalized.startsWith('/') ? normalized : `/${normalized}`
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
  if (path.startsWith('blob:')) return path
  if (path.startsWith('http://') || path.startsWith('https://')) return path

  const relative = resolveMediaRelativePath(path)
  if (!relative || relative.startsWith('http')) return relative

  // Local Vite dev: same-origin /media/* is proxied to the backend (vite.config.js).
  // Remote API base (Render): always use absolute URLs even in dev.
  const url =
    import.meta.env.DEV && !isRemoteApiBase() ? relative : `${API_BASE}${relative}`

  if (import.meta.env.DEV) {
    console.debug('[BOVIMED mediaUrl]', { input: path, relative, resolved: url, apiBase: API_BASE })
  }

  return url
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
  err.isAuthError = response.status === 401
  err.isValidationError = response.status === 400
  err.isNotFoundError = response.status === 404
  err.isServerError = response.status >= 500
  return err
}

function authHeaders(extra = {}) {
  const token = getToken()
  return {
    ...extra,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function isNetworkFailure(err) {
  if (!err) return false
  if (err instanceof TypeError) return true
  const msg = String(err.message || '').toLowerCase()
  return msg.includes('failed to fetch') || msg.includes('networkerror') || msg.includes('load failed') || msg.includes('timeout')
}

function isTransientBackendFailure(err) {
  if (!err) return false
  if (err?.name === 'AbortError') return true
  const status = Number(err?.status)
  if ([502, 503, 504].includes(status)) return true
  const msg = String(err?.message || '').toLowerCase()
  return (
    msg.includes('failed to fetch') ||
    msg.includes('networkerror') ||
    msg.includes('load failed') ||
    msg.includes('temporarily unavailable') ||
    msg.includes('service unavailable') ||
    msg.includes('gateway timeout') ||
    msg.includes('bad gateway')
  )
}

async function apiFetch(path, options = {}) {
  let res
  try {
    res = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: authHeaders(options.headers || {}),
    })
  } catch (err) {
    if (isNetworkFailure(err)) {
      const networkErr = new Error('Unable to connect to BOVIMED server.')
      networkErr.isNetworkError = true
      networkErr.cause = err
      throw networkErr
    }
    throw err
  }
  if (!res.ok) throw await parseError(res)
  if (res.status === 204) return null
  return res.json()
}

export async function getHealth() {
  return apiFetch('/api/health')
}

export async function getModelInfo() {
  return apiFetch('/api/model-info')
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

async function ensureBackendReachable() {
  const healthUrl = `${API_BASE}/api/health`
  const maxAttempts = 3
  let lastError = null

  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 15000)

    try {
      console.log('BOVIMED health probe:', healthUrl, 'attempt', attempt + 1)
      const res = await fetch(healthUrl, {
        method: 'GET',
        signal: controller.signal,
        headers: authHeaders(),
      })

      if (res.ok) {
        console.log('Backend health check passed:', res.status)
        return true
      }

      if ([502, 503, 504].includes(res.status)) {
        throw Object.assign(new Error(`Backend warm-up response (${res.status})`), {
          status: res.status,
          isTransientBackendFailure: true,
        })
      }

      // Not a transient wake-up issue; the endpoint is reachable but some other server issue may exist.
      console.log('Backend health check responded with status:', res.status)
      return true
    } catch (err) {
      lastError = err
      if (attempt < maxAttempts - 1) {
        const delayMs = 1500 * (attempt + 1)
        console.log('Backend not ready yet, retrying health check in', delayMs, 'ms')
        await sleep(delayMs)
      }
    } finally {
      clearTimeout(timeoutId)
    }
  }

  throw lastError || new Error('Unable to reach the BOVIMED server.')
}

export async function analyzeImage(image, options = {}) {
  if (!image) {
    throw new Error('Please select a cow image before starting the AI scan.')
  }

  const form = new FormData()
  const filename = options.filename || image.name || 'capture.jpg'
  const endpoint = `${API_BASE}/api/analyze`
  const maxAttempts = options.maxAttempts ?? 3

  console.log('BOVIMED API URL:', API_BASE)
  console.log('Analyze endpoint:', endpoint)
  console.log('Selected file:', image?.name)
  console.log('File type:', image?.type)
  console.log('File size:', image?.size)

  try {
    await ensureBackendReachable()
  } catch (healthErr) {
    console.warn('Backend health probe failed before analyze:', healthErr)
  }

  form.append('image', image, filename)
  if (options.cowId && String(options.cowId).trim()) {
    form.append('cow_id', String(options.cowId).trim())
  }

  let lastError = null

  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const controller = new AbortController()
    const timeoutMs = options.timeout ?? 60000
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs)

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        signal: controller.signal,
        headers: authHeaders(),
        body: form,
      })

      console.log('Analyze response status:', res.status)

      if (!res.ok) {
        const parsedError = await parseError(res)
        if (isTransientBackendFailure(parsedError) && attempt < maxAttempts - 1) {
          const delayMs = 1500 * (attempt + 1)
          console.warn('Transient backend failure during analyze, retrying in', delayMs, 'ms', parsedError)
          await sleep(delayMs)
          continue
        }
        throw parsedError
      }

      return res.json()
    } catch (err) {
      lastError = err

      if (err?.name === 'AbortError') {
        const timeoutError = new Error('Starting BOVIMED AI service… This may take a few seconds. Please wait a moment and try again.')
        timeoutError.isTimeoutError = true
        timeoutError.cause = err
        if (attempt < maxAttempts - 1) {
          const delayMs = 1500 * (attempt + 1)
          console.warn('Analyze request timed out, retrying in', delayMs, 'ms')
          await sleep(delayMs)
          continue
        }
        throw timeoutError
      }

      if (isTransientBackendFailure(err) && attempt < maxAttempts - 1) {
        const delayMs = 1500 * (attempt + 1)
        console.warn('Transient backend failure, retrying analyze in', delayMs, 'ms', err)
        await sleep(delayMs)
        continue
      }

      if (err instanceof TypeError || /failed to fetch|networkerror|load failed/i.test(String(err?.message || ''))) {
        const networkError = new Error('Unable to reach the BOVIMED server. Please check your connection and try again.')
        networkError.isNetworkError = true
        networkError.cause = err
        console.error('Analyze network error:', err)
        throw networkError
      }

      console.error('Analyze request error:', err)
      throw err
    } finally {
      clearTimeout(timeoutId)
    }
  }

  throw lastError || new Error('Unable to reach the BOVIMED server.')
}

export async function getDashboard() {
  return apiFetch('/api/dashboard')
}

export async function listCows() {
  return apiFetch('/api/cows')
}

export async function getCow(cowId) {
  return apiFetch(`/api/cows/${encodeURIComponent(cowId)}`)
}

export async function getCowHistory(cowId) {
  return apiFetch(`/api/cows/${encodeURIComponent(cowId)}/history`)
}

export async function listAlerts({ unreadOnly = false, limit = 50 } = {}) {
  const params = new URLSearchParams()
  if (unreadOnly) params.set('unread_only', 'true')
  if (limit) params.set('limit', String(limit))
  const qs = params.toString()
  return apiFetch(`/api/alerts${qs ? `?${qs}` : ''}`)
}

export async function markAlertRead(alertId) {
  return apiFetch(`/api/alerts/${alertId}/read`, { method: 'POST' })
}

export async function sendChatMessage(payload) {
  return apiFetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function getChatStatus() {
  return apiFetch('/api/chat/status')
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

export async function listHistory({ limit = 50, cowId } = {}) {
  const params = new URLSearchParams()
  if (limit) params.set('limit', String(limit))
  if (cowId) params.set('cow_id', cowId)
  const qs = params.toString()
  return apiFetch(`/api/history${qs ? `?${qs}` : ''}`)
}

export async function getAnalysis(analysisId) {
  return apiFetch(`/api/history/${analysisId}`)
}

export async function getNotifications({ limit = 50 } = {}) {
  const params = new URLSearchParams()
  if (limit) params.set('limit', String(limit))
  const qs = params.toString()
  return apiFetch(`/api/notifications${qs ? `?${qs}` : ''}`)
}

export async function getNotificationUnreadCount() {
  return apiFetch('/api/notifications/unread-count')
}

export async function markNotificationRead(notificationId) {
  return apiFetch(`/api/notifications/${notificationId}/read`, { method: 'PATCH' })
}

export async function markAllNotificationsRead() {
  return apiFetch('/api/notifications/read-all', { method: 'PATCH' })
}

export async function getNotificationPreferences() {
  return apiFetch('/api/notifications/preferences')
}

export async function updateNotificationPreferences(payload) {
  return apiFetch('/api/notifications/preferences', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

