import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import {
  Bell,
  Camera,
  History,
  LayoutDashboard,
  LogOut,
  Menu,
  MessageCircle,
  ScanLine,
  Settings,
  Stethoscope,
  Users,
  X,
} from 'lucide-react'
import AiModeBadge, { BrandMark } from '../components/AiModeBadge'
import LanguageSelector from '../components/LanguageSelector'
import { useAuth } from '../context/AuthContext'
import { useI18n } from '../i18n/I18nContext'
import { getHealth } from '../services/api'

function navClassName({ isActive }) {
  return `bovimed-nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold transition-colors ${
    isActive ? 'is-active' : ''
  }`
}

function mobileNavClassName({ isActive }) {
  return `bovimed-nav-link flex flex-1 flex-col items-center gap-0.5 rounded-lg px-1 py-2 text-[10px] font-semibold ${
    isActive ? 'is-active' : ''
  }`
}

export default function AppLayout() {
  const { t } = useI18n()
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const [health, setHealth] = useState(null)

  const NAV = [
    { to: '/dashboard', end: true, label: t.nav.dashboard, icon: LayoutDashboard },
    { to: '/analyze', label: t.nav.analyze, icon: ScanLine },
    { to: '/camera', label: t.nav.camera, icon: Camera },
    { to: '/cows', label: t.nav.cows, icon: Users },
    { to: '/history', label: t.nav.history, icon: History },
    { to: '/alerts', label: t.nav.alerts, icon: Bell },
    { to: '/chat', label: t.nav.chat, icon: MessageCircle },
    { to: '/veterinarians', label: t.nav.vets, icon: Stethoscope },
    { to: '/settings', label: t.nav.settings, icon: Settings },
  ]

  useEffect(() => {
    let cancelled = false
    getHealth()
      .then((h) => {
        if (!cancelled) setHealth(h)
      })
      .catch(() => {
        if (!cancelled)
          setHealth({ demo_mode: true, message: t.common.backendDown, status: 'error' })
      })
    return () => {
      cancelled = true
    }
  }, [t.common.backendDown])

  async function onLogout() {
    await logout()
    navigate('/login', { replace: true })
  }

  const navItems = (
    <>
      {NAV.map(({ to, end, label, icon: Icon }) => (
        <NavLink key={to} to={to} end={end} onClick={() => setOpen(false)} className={navClassName}>
          {({ isActive }) => (
            <>
              <Icon
                className="h-4 w-4 shrink-0"
                strokeWidth={2.25}
                aria-hidden
                color={isActive ? '#ffffff' : '#1b4332'}
              />
              <span style={{ color: isActive ? '#ffffff' : '#1b4332' }}>{label}</span>
            </>
          )}
        </NavLink>
      ))}
    </>
  )

  return (
    <div className="min-h-screen bg-cream text-[#1b4332]">
      <header className="sticky top-0 z-30 border-b border-earth/80 bg-cream/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <button
              type="button"
              className="rounded-lg border border-earth p-2 text-[#1b4332] lg:hidden"
              aria-label="Open menu"
              onClick={() => setOpen(true)}
            >
              <Menu className="h-5 w-5" color="#1b4332" />
            </button>
            <BrandMark to="/dashboard" />
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            <LanguageSelector />
            <AiModeBadge health={health} />
            <span className="hidden text-sm font-medium text-[#1b4332]/80 md:inline">
              {user?.full_name}
            </span>
            <button
              type="button"
              onClick={onLogout}
              className="inline-flex items-center gap-1.5 rounded-xl border border-earth bg-white px-3 py-2 text-sm font-semibold text-[#1b4332]"
            >
              <LogOut className="h-4 w-4" color="#1b4332" />
              <span className="hidden sm:inline">{t.nav.logout}</span>
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl">
        <aside className="sticky top-[65px] hidden h-[calc(100vh-65px)] w-60 shrink-0 border-r rtl:border-r-0 rtl:border-l border-earth bg-white/80 p-4 lg:block">
          <nav className="flex flex-col gap-1" aria-label="Main">
            {navItems}
          </nav>
          <p className="mt-8 px-2 text-xs leading-relaxed text-[#1b4332]/55">{t.disclaimer}</p>
        </aside>

        {open ? (
          <div className="fixed inset-0 z-40 lg:hidden">
            <button
              type="button"
              className="absolute inset-0 bg-[#1b4332]/40"
              aria-label="Close menu"
              onClick={() => setOpen(false)}
            />
            <div className="absolute left-0 rtl:left-auto rtl:right-0 top-0 flex h-full w-72 flex-col bg-white p-4 shadow-xl">
              <div className="mb-4 flex items-center justify-between">
                <BrandMark to="/dashboard" />
                <button type="button" className="rounded-lg p-2" onClick={() => setOpen(false)}>
                  <X className="h-5 w-5" color="#1b4332" />
                </button>
              </div>
              <nav className="flex flex-col gap-1">{navItems}</nav>
            </div>
          </div>
        ) : null}

        <main className="min-w-0 flex-1 px-4 py-6 pb-24 sm:px-6 lg:pb-6">
          <Outlet context={{ health, setHealth }} />
        </main>
      </div>

      <nav className="fixed inset-x-0 bottom-0 z-30 flex border-t border-earth bg-white/95 px-1 py-1 lg:hidden">
        {NAV.slice(0, 5).map(({ to, end, label, icon: Icon }) => (
          <NavLink key={to} to={to} end={end} className={mobileNavClassName}>
            {({ isActive }) => (
              <>
                <Icon
                  className="h-4 w-4"
                  strokeWidth={2.25}
                  color={isActive ? '#ffffff' : '#1b4332'}
                />
                <span style={{ color: isActive ? '#ffffff' : '#1b4332' }} className="truncate">
                  {label}
                </span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
    </div>
  )
}
