import { Lock } from 'lucide-react'
import type { DepthTier } from '@/types'

interface DepthSelectorProps {
  value: DepthTier
  onChange: (tier: DepthTier) => void
  userTier?: 'free' | 'explorer'
}

const TIERS: { id: DepthTier; label: string; duration: string }[] = [
  { id: 'snapshot', label: 'Snapshot', duration: '1 min' },
  { id: 'guide', label: 'Guide', duration: '4 min' },
  { id: 'deepdive', label: 'Deep Dive', duration: '10 min' },
]

export function DepthSelector({
  value,
  onChange,
  userTier = 'explorer',
}: DepthSelectorProps) {
  const isLocked = (tier: DepthTier) => tier === 'deepdive' && userTier === 'free'

  return (
    <div className="flex items-center gap-1.5" role="group" aria-label="Narration depth">
      {TIERS.map(({ id, label, duration }) => {
        const active = value === id
        const locked = isLocked(id)

        return (
          <div key={id} className="relative group">
            <button
              onClick={() => {
                if (!locked) onChange(id)
              }}
              disabled={locked}
              aria-pressed={active}
              aria-label={`${label}, ${duration}${locked ? ', locked for free users' : ''}`}
              className={`
                flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-sans font-medium
                transition-all duration-150 select-none whitespace-nowrap
                ${active
                  ? 'bg-gold text-white shadow-sm shadow-gold/30'
                  : locked
                    ? 'bg-white/5 text-stone border border-white/10 cursor-not-allowed'
                    : 'bg-white/10 text-stone-light border border-white/10 hover:bg-white/15 hover:text-cream cursor-pointer'
                }
              `}
            >
              {label}
              {!locked && (
                <span className={`${active ? 'text-gold-light' : 'text-stone'} text-[10px]`}>
                  · {duration}
                </span>
              )}
              {locked && <Lock className="w-2.5 h-2.5 ml-0.5 opacity-60" />}
            </button>

            {/* Upgrade tooltip */}
            {locked && (
              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-navy border border-gold/30 rounded text-[10px] text-gold-light font-sans whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 shadow-lg">
                Upgrade to Explorer
                <div className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gold/30" />
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
