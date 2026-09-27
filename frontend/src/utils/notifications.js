/**
 * Notification i18n helpers and optional browser notifications.
 */

export function resolveTranslationKey(t, key) {
  if (!key || !t) return key || ''
  const parts = key.split('.')
  let cur = t
  for (const part of parts) {
    if (cur == null || typeof cur !== 'object') return key
    cur = cur[part]
  }
  return typeof cur === 'string' ? cur : key
}

export function interpolateTemplate(template, payload = {}) {
  if (!template) return ''
  return String(template).replace(/\{\{(\w+)\}\}/g, (_, name) => {
    const val = payload[name]
    return val === undefined || val === null ? '' : String(val)
  })
}

export function formatNotificationText(t, notification) {
  const titleTpl = resolveTranslationKey(t, notification.title_key)
  const messageTpl = resolveTranslationKey(t, notification.message_key)
  const payload = notification.payload || {}
  return {
    title: interpolateTemplate(titleTpl, payload),
    message: interpolateTemplate(messageTpl, payload),
  }
}

export function isBrowserNotificationSupported() {
  return typeof window !== 'undefined' && 'Notification' in window
}

export function getBrowserNotificationPermission() {
  if (!isBrowserNotificationSupported()) return 'unsupported'
  return Notification.permission
}

export async function requestBrowserNotificationPermission() {
  if (!isBrowserNotificationSupported()) return 'unsupported'
  if (Notification.permission === 'granted') return 'granted'
  if (Notification.permission === 'denied') return 'denied'
  try {
    return await Notification.requestPermission()
  } catch {
    return 'denied'
  }
}

export function showBrowserNotification({ title, body, tag, onClick }) {
  if (!isBrowserNotificationSupported() || Notification.permission !== 'granted') return null
  try {
    const n = new Notification(title, { body, tag, icon: '/favicon.svg' })
    if (onClick) {
      n.onclick = () => {
        window.focus()
        onClick()
        n.close()
      }
    }
    return n
  } catch {
    return null
  }
}
