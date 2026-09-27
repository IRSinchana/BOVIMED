import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  AlertCircle,
  AlertOctagon,
  AlertTriangle,
  Bell,
  CheckCircle,
  Clock,
  Inbox,
  ScanLine,
  ShieldAlert,
} from 'lucide-react'
import { ErrorMessage, RiskBadge } from '../components/Status'
import { useI18n } from '../i18n/I18nContext'
import {
  getNotifications,
  markAllNotificationsRead,
  markNotificationRead,
} from '../services/api'
import { formatConfidence, normalizeRiskLevel } from '../utils/analysis'
import { formatNotificationText } from '../utils/notifications'

function riskLabel(t, risk) {
  const level = normalizeRiskLevel(risk)
  return t.risk?.[level] || level
}

function isHighRiskNotification(notification) {
  const payload = notification?.payload || {}
  const level = normalizeRiskLevel(payload.risk)
  if (level === 'High' || level === 'Critical' || level === 'Severe') return true
  const severity = String(notification?.severity || '').toLowerCase()
  return severity === 'high' || severity === 'critical'
}

function isRecentNotification(notification) {
  if (!notification?.created_at) return false
  const created = new Date(notification.created_at)
  if (Number.isNaN(created.getTime())) return false
  const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000
  return created.getTime() >= weekAgo
}

function getSeverityVisuals(severity, riskLevel) {
  const level = normalizeRiskLevel(riskLevel)
  if (level === 'Critical' || severity === 'critical') {
    return {
      icon: ShieldAlert,
      color: '#b91c1c',
      border: 'border-red-300',
      badge: 'bg-red-100 text-red-800 border-red-300',
    }
  }
  if (level === 'High' || level === 'Severe' || severity === 'high') {
    return {
      icon: AlertOctagon,
      color: '#c2410c',
      border: 'border-orange-300',
      badge: 'bg-orange-100 text-orange-900 border-orange-300',
    }
  }
  if (level === 'Moderate' || severity === 'warning') {
    return {
      icon: AlertTriangle,
      color: '#d97706',
      border: 'border-amber-300',
      badge: 'bg-amber-100 text-amber-900 border-amber-300',
    }
  }
  if (level === 'Mild') {
    return {
      icon: AlertCircle,
      color: '#0369a1',
      border: 'border-sky-300',
      badge: 'bg-sky-100 text-sky-900 border-sky-300',
    }
  }
  return {
    icon: CheckCircle,
    color: '#2d6a4f',
    border: 'border-emerald-200',
    badge: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  }
}

function getResultPath(notification) {
  const payload = notification?.payload || {}
  if (notification?.action_url) return notification.action_url
  if (payload.analysisId) return `/result/${payload.analysisId}`
  return null
}

function getScreeningNote(t, riskLevel) {
  const level = normalizeRiskLevel(riskLevel)
  if (level === 'High' || level === 'Critical' || level === 'Severe') {
    return t.notifications?.screeningNoteHigh || t.notifications?.screeningNote
  }
  if (level === 'Moderate') {
    return t.notifications?.screeningNoteModerate || t.notifications?.screeningNote
  }
  return t.notifications?.screeningNote || ''
}

function safeText(value, fallback = '—') {
  if (value === undefined || value === null || value === '') return fallback
  return String(value)
}

export default function AlertsPage() {
  const { t, lang } = useI18n()
  const [items, setItems] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeFilter, setActiveFilter] = useState('all')
  const [markingAll, setMarkingAll] = useState(false)

  const loadNotifications = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getNotifications({ limit: 100 })
      setItems(Array.isArray(data?.notifications) ? data.notifications : [])
      setUnreadCount(data?.unread_count ?? 0)
    } catch {
      setError(t.notifications?.loadError || 'Unable to load notifications. Please try again.')
      setItems([])
      setUnreadCount(0)
    } finally {
      setLoading(false)
    }
  }, [t.notifications?.loadError])

  useEffect(() => {
    loadNotifications()
  }, [loadNotifications])

  const stats = useMemo(() => {
    const all = items.length
    const unread = items.filter((n) => !n.is_read).length
    const highRisk = items.filter((n) => isHighRiskNotification(n)).length
    const recent = items.filter((n) => isRecentNotification(n)).length
    return { all, unread, highRisk, recent }
  }, [items])

  const filteredItems = useMemo(() => {
    switch (activeFilter) {
      case 'unread':
        return items.filter((n) => !n.is_read)
      case 'highRisk':
        return items.filter((n) => isHighRiskNotification(n))
      case 'recent':
        return items.filter((n) => isRecentNotification(n))
      default:
        return items
    }
  }, [items, activeFilter])

  async function onMarkRead(id) {
    try {
      await markNotificationRead(id)
      setItems((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n)),
      )
      setUnreadCount((count) => Math.max(0, count - 1))
    } catch {
      setError(t.notifications?.loadError || 'Unable to load notifications. Please try again.')
    }
  }

  async function onMarkAllRead() {
    setMarkingAll(true)
    try {
      await markAllNotificationsRead()
      setItems((prev) => prev.map((n) => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch {
      setError(t.notifications?.loadError || 'Unable to load notifications. Please try again.')
    } finally {
      setMarkingAll(false)
    }
  }

  function formatTime(iso) {
    try {
      return new Intl.DateTimeFormat(lang, {
        dateStyle: 'medium',
        timeStyle: 'short',
      }).format(new Date(iso))
    } catch {
      return safeText(iso)
    }
  }

  const summaryCards = [
    { id: 'all', label: t.notifications?.summaryAll || 'All', value: stats.all, icon: Inbox },
    { id: 'unread', label: t.notifications?.summaryUnread || 'Unread', value: stats.unread, icon: Bell },
    { id: 'highRisk', label: t.notifications?.summaryHighRisk || 'High Risk', value: stats.highRisk, icon: AlertTriangle },
    { id: 'recent', label: t.notifications?.summaryRecent || 'Recent', value: stats.recent, icon: Clock },
  ]

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold text-[#1b4332]">
            {t.notifications?.title || 'Notifications'}
          </h1>
          <p className="mt-1 max-w-2xl text-sm text-[#1b4332]/70">
            {t.notifications?.pageSubtitle || 'Stay updated about important cow health events.'}
          </p>
        </div>
        {unreadCount > 0 ? (
          <button
            type="button"
            disabled={markingAll}
            onClick={onMarkAllRead}
            className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-[#2d6a4f] disabled:opacity-60"
          >
            {t.notifications?.markAllRead || 'Mark all as read'}
          </button>
        ) : null}
      </header>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map(({ id, label, value, icon: Icon }) => {
          const active = activeFilter === id
          return (
            <button
              key={id}
              type="button"
              onClick={() => setActiveFilter(id)}
              className={`rounded-3xl border bg-white p-4 text-left shadow-sm transition hover:shadow-md ${
                active ? 'border-[#2d6a4f] ring-2 ring-[#2d6a4f]/20' : 'border-earth'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-[#1b4332]/55">
                    {label}
                  </p>
                  <p className="mt-1 font-display text-2xl font-bold text-[#1b4332]">{value}</p>
                </div>
                <span className="rounded-2xl bg-cream/70 p-2">
                  <Icon className="h-5 w-5" color="#2d6a4f" aria-hidden />
                </span>
              </div>
            </button>
          )
        })}
      </div>

      <ErrorMessage message={error} />

      {loading ? (
        <div className="rounded-3xl border border-earth bg-white p-8 text-center shadow-sm">
          <p className="text-sm text-[#1b4332]/70">
            {t.notifications?.loading || 'Loading notifications...'}
          </p>
        </div>
      ) : null}

      {!loading && filteredItems.length === 0 && !error ? (
        <div className="rounded-3xl border border-earth bg-white p-10 text-center shadow-sm">
          <Bell className="mx-auto mb-3 h-12 w-12 text-[#2d6a4f]/70" aria-hidden />
          <p className="text-lg font-semibold text-[#1b4332]">
            {t.notifications?.emptyTitle || 'No new notifications'}
          </p>
          <p className="mt-2 text-sm text-[#1b4332]/70">
            {t.notifications?.emptyHint ||
              'Notifications about cow health and AI screening results will appear here.'}
          </p>
        </div>
      ) : null}

      {!loading && filteredItems.length > 0 ? (
        <div className="space-y-4">
          {filteredItems.map((notification) => {
            const payload = notification.payload || {}
            const riskLevel = normalizeRiskLevel(payload.risk || notification.type)
            const visuals = getSeverityVisuals(notification.severity, riskLevel)
            const RiskIcon = visuals.icon
            const resultPath = getResultPath(notification)
            const { title, message } = formatNotificationText(t, notification)
            const condition = safeText(payload.detection, title)
            const cowId = safeText(payload.cowId || notification.cow_id)
            const screeningNote = getScreeningNote(t, riskLevel)

            return (
              <article
                key={notification.id}
                className={`rounded-3xl border bg-white p-5 shadow-sm transition hover:shadow-md ${visuals.border} ${
                  notification.is_read ? 'opacity-85' : ''
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-earth/60 pb-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <RiskIcon className="h-5 w-5 shrink-0" color={visuals.color} aria-hidden />
                    <RiskBadge risk={riskLevel} label={riskLabel(t, riskLevel)} />
                    <span
                      className={`rounded-xl border px-2.5 py-0.5 text-xs font-bold uppercase ${visuals.badge}`}
                    >
                      {notification.is_read
                        ? t.notifications?.read || 'Read'
                        : t.notifications?.unread || 'Unread'}
                    </span>
                  </div>
                  <time className="text-xs text-[#1b4332]/60">{formatTime(notification.created_at)}</time>
                </div>

                <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                  <div className="rounded-2xl bg-cream/40 p-3">
                    <p className="text-xs font-semibold uppercase text-[#1b4332]/55">
                      {t.notifications?.cow || 'Cow'}
                    </p>
                    <p className="mt-1 font-semibold text-[#1b4332]">{cowId}</p>
                  </div>
                  <div className="rounded-2xl bg-cream/40 p-3 sm:col-span-2">
                    <p className="text-xs font-semibold uppercase text-[#1b4332]/55">
                      {t.notifications?.condition || 'Condition'}
                    </p>
                    <p className="mt-1 font-semibold text-[#1b4332]">{condition}</p>
                  </div>
                  <div className="rounded-2xl bg-cream/40 p-3">
                    <p className="text-xs font-semibold uppercase text-[#1b4332]/55">
                      {t.notifications?.confidence || 'Confidence'}
                    </p>
                    <p className="mt-1 font-semibold text-[#2d6a4f]">
                      {formatConfidence(payload.confidence)}
                    </p>
                  </div>
                </div>

                <p className="mt-4 text-sm leading-relaxed text-[#1b4332]/85">
                  {message || screeningNote}
                </p>
                {screeningNote ? (
                  <p className="mt-2 text-sm italic text-[#1b4332]/70">{screeningNote}</p>
                ) : null}

                <div className="mt-4 flex flex-wrap gap-2">
                  {resultPath ? (
                    <Link
                      to={resultPath}
                      onClick={() => {
                        if (!notification.is_read) onMarkRead(notification.id)
                      }}
                      className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-4 py-2 text-xs font-semibold text-white"
                    >
                      <ScanLine className="h-4 w-4" aria-hidden />
                      {t.notifications?.viewResult || t.notifications?.viewAnalysis || 'View Result'}
                    </Link>
                  ) : null}
                  {!notification.is_read ? (
                    <button
                      type="button"
                      onClick={() => onMarkRead(notification.id)}
                      className="rounded-xl border border-earth bg-white px-4 py-2 text-xs font-semibold text-[#2d6a4f]"
                    >
                      {t.notifications?.markRead || 'Mark as Read'}
                    </button>
                  ) : null}
                </div>
              </article>
            )
          })}
        </div>
      ) : null}
    </div>
  )
}
