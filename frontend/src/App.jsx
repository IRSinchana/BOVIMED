import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import { AuthProvider } from './context/AuthContext'
import { I18nProvider } from './i18n/I18nContext'
import AppLayout from './layouts/AppLayout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import AnalyzePage from './pages/AnalyzePage'
import CameraScanPage from './pages/CameraScanPage'
import ResultPage from './pages/ResultPage'
import SettingsPage from './pages/SettingsPage'
import ChatPage from './pages/ChatPage'
import VeterinariansPage from './pages/VeterinariansPage'
import AlertsPage from './pages/AlertsPage'
import { CowsPage, HistoryPage } from './pages/SimplePages'
import CowProfilePage from './pages/CowProfilePage'
import CompareScansPage from './pages/CompareScansPage'
import { useAuth } from './context/AuthContext'

function RootRedirect() {
  const { isAuthenticated, loading } = useAuth()
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-cream text-[#1b4332]">
        Loading…
      </div>
    )
  }
  return <Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />
}

export default function App() {
  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RootRedirect />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/analyze" element={<AnalyzePage />} />
              <Route path="/camera" element={<CameraScanPage />} />
              <Route path="/result" element={<ResultPage />} />
              <Route path="/result/:analysisId" element={<ResultPage />} />
              <Route path="/cows" element={<CowsPage />} />
              <Route path="/cows/:cowId" element={<CowProfilePage />} />
              <Route path="/compare" element={<CompareScansPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/veterinarians" element={<VeterinariansPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>

            <Route path="*" element={<RootRedirect />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </I18nProvider>
  )
}
