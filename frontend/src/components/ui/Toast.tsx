import React, { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react'

type ToastType = 'info' | 'error' | 'success'

interface ToastItem {
  id: string
  message: string
  type: ToastType
}

interface ToastContextValue {
  showToast: (message: string, type?: ToastType) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const showToast = useCallback((message: string, type: ToastType = 'info') => {
    const id = Math.random().toString(36).slice(2)
    setToasts((prev) => [...prev, { id, message, type }])
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 3000)
  }, [])

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <ToastContainer toasts={toasts} onDismiss={(id) => setToasts((p) => p.filter((t) => t.id !== id))} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used inside ToastProvider')
  return ctx
}

const icons: Record<ToastType, React.ReactNode> = {
  info: <Info className="w-4 h-4 text-gold-light" />,
  error: <AlertCircle className="w-4 h-4 text-rust" />,
  success: <CheckCircle className="w-4 h-4 text-green-400" />,
}

const bgColors: Record<ToastType, string> = {
  info: 'bg-navy border-gold/30',
  error: 'bg-navy border-rust/40',
  success: 'bg-navy border-green-500/30',
}

function ToastContainer({
  toasts,
  onDismiss,
}: {
  toasts: ToastItem[]
  onDismiss: (id: string) => void
}) {
  if (toasts.length === 0) return null

  return (
    <div
      className="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-2 pointer-events-none"
      role="status"
      aria-live="polite"
    >
      {toasts.map((t) => (
        <ToastItem key={t.id} toast={t} onDismiss={onDismiss} />
      ))}
    </div>
  )
}

function ToastItem({ toast, onDismiss }: { toast: ToastItem; onDismiss: (id: string) => void }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 10)
    return () => clearTimeout(t)
  }, [])

  return (
    <div
      className={`pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg font-sans text-sm text-white max-w-xs transition-all duration-300 ${bgColors[toast.type]} ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}
    >
      {icons[toast.type]}
      <span className="flex-1">{toast.message}</span>
      <button
        onClick={() => onDismiss(toast.id)}
        className="opacity-60 hover:opacity-100 transition-opacity"
        aria-label="Dismiss"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  )
}
