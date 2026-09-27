import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Bell } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { getNotificationUnreadCount } from '../services/api'

export default function NotificationBell() {
  const navigate = useNavigate()
  const { t } = useI18n()
  const [unread, setUnread] = useState(0)

  const refreshCount = useCallback(async () => {
    try {
      const data = await getNotificationUnreadCount()
      setUnread(data?.unread_count ?? 0)
    } catch {
      setUnread(0)
    }
  }, [])

  useEffect(() => {
    refreshCount()
    const id = setInterval(refreshCount, 30000)
    return () => clearInterval(id)
  }, [refreshCount])

  return (
    <button
      type="button"
      onClick={() => navigate('/alerts')}
      className="relative inline-flex items-center justify-center rounded-xl border border-earth bg-white p-2 text-[#1b4332]"
      aria-label={t.notifications?.title || 'Notifications'}
    >
      <Bell className="h-5 w-5" color="#1b4332" />
      {unread > 0 ? (
        <span
          className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1 text-[10px] font-bold text-white"
          aria-live="polite"
        >
          {unread > 99 ? '99+' : unread}
        </span>
      ) : null}
    </button>
  )
}
