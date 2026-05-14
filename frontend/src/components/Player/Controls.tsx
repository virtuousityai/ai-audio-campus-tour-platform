import { Play, Pause, ChevronLeft, ChevronRight, Loader2 } from 'lucide-react'

interface ControlsProps {
  isPlaying: boolean
  isLoading: boolean
  onPlay: () => void
  onPause: () => void
  onPrev: () => void
  onNext: () => void
  hasPrev: boolean
  hasNext: boolean
}

export function Controls({
  isPlaying,
  isLoading,
  onPlay,
  onPause,
  onPrev,
  onNext,
  hasPrev,
  hasNext,
}: ControlsProps) {
  return (
    <div className="flex items-center justify-center gap-6">
      {/* Previous */}
      <button
        onClick={onPrev}
        disabled={!hasPrev}
        aria-label="Previous stop"
        className="w-10 h-10 flex items-center justify-center rounded-full text-stone-light hover:text-cream hover:bg-white/10 transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed active:scale-90"
      >
        <ChevronLeft className="w-6 h-6" />
      </button>

      {/* Play / Pause — large gold circle */}
      <button
        onClick={isPlaying ? onPause : onPlay}
        disabled={isLoading}
        aria-label={isLoading ? 'Loading audio' : isPlaying ? 'Pause narration' : 'Play narration'}
        className={`
          w-16 h-16 rounded-full flex items-center justify-center
          shadow-lg shadow-gold/20
          transition-all duration-150 active:scale-95
          ${isLoading
            ? 'bg-gold/50 cursor-wait'
            : 'bg-gold hover:bg-gold-light cursor-pointer'
          }
        `}
      >
        {isLoading ? (
          <Loader2 className="w-6 h-6 text-white animate-spin" />
        ) : isPlaying ? (
          <Pause className="w-6 h-6 text-white" />
        ) : (
          <Play className="w-6 h-6 text-white ml-0.5" />
        )}
      </button>

      {/* Next */}
      <button
        onClick={onNext}
        disabled={!hasNext}
        aria-label="Next stop"
        className="w-10 h-10 flex items-center justify-center rounded-full text-stone-light hover:text-cream hover:bg-white/10 transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed active:scale-90"
      >
        <ChevronRight className="w-6 h-6" />
      </button>
    </div>
  )
}
