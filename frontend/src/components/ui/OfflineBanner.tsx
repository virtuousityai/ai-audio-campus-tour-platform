import { WifiOff } from 'lucide-react'
import { useOffline } from '@/hooks/useOffline'

export function OfflineBanner() {
  const { isOnline } = useOffline()

  return (
    <div
      className={`
        fixed bottom-0 left-0 right-0 z-50
        flex items-center justify-center gap-2
        px-4 py-3
        bg-amber-900/90 text-amber-200
        border-t border-amber-700/60
        transition-transform duration-300 ease-in-out
        ${isOnline ? 'translate-y-full' : 'translate-y-0'}
      `}
      style={{ paddingBottom: 'calc(0.75rem + env(safe-area-inset-bottom))' }}
      role="status"
      aria-live="polite"
      aria-label={isOnline ? undefined : "You are offline"}
    >
      <WifiOff className="w-4 h-4 flex-shrink-0" />
      <span className="text-sm font-sans font-medium">
        You're offline — previously visited stops still play
      </span>
    </div>
  )
}
