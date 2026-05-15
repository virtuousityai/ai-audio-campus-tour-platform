import type { GPSStatus } from '@/hooks/useGPS'

interface GPSBadgeProps {
  status: GPSStatus
}

export function GPSBadge({ status }: GPSBadgeProps) {
  if (status === 'idle' || status === 'unavailable') return null

  const isActive = status === 'watching'
  const dotColor = isActive ? 'bg-green-400' : 'bg-orange-400'
  const label =
    status === 'watching'
      ? 'GPS Active'
      : status === 'denied'
        ? 'GPS Off'
        : 'GPS Error'

  return (
    <div
      className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-white/10 border border-white/15"
      aria-label={label}
      title={label}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${dotColor} ${isActive ? 'animate-pulse' : ''}`}
      />
      <span className="text-[10px] font-sans font-medium text-stone-light leading-none">
        {label}
      </span>
    </div>
  )
}
