import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { ToastProvider } from '@/components/ui/Toast'
import { Home } from '@/pages/Home'
import { CityPage } from '@/pages/CityPage'
import { TourDetail } from '@/pages/TourDetail'
import { TourPlayer } from '@/pages/TourPlayer'

export default function App() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/city/:slug" element={<CityPage />} />
            <Route path="/tour/:tourId" element={<TourDetail />} />
            <Route path="/tour/:tourId/play" element={<TourPlayer />} />
            {/* Catch-all → home */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </ErrorBoundary>
  )
}
