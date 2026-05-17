import { useState, useEffect, useRef } from 'react'
import { MapPin, ChevronDown, ChevronUp, FileText } from 'lucide-react'
import type { POI, DepthTier, Narration } from '@/types'
import { useTTS } from '@/hooks/useTTS'
import { ErrorBoundary } from '../ErrorBoundary'
import { Badge } from '../ui/Badge'
import { DepthSelector } from './DepthSelector'
import { Waveform } from './Waveform'
import { Controls } from './Controls'

interface PlayerProps {
  poi: POI
  totalStops: number
  depthTier: DepthTier
  onDepthChange: (tier: DepthTier) => void
  onPrev: () => void
  onNext: () => void
}

function getNarration(poi: POI, tier: DepthTier): Narration | null {
  return poi.narrations.find((n) => n.depth_tier === tier) ?? poi.narrations[0] ?? null
}

function PlayerInner({ poi, totalStops, depthTier, onDepthChange, onPrev, onNext }: PlayerProps) {
  const { speak, stop, isLoading, isPlaying, error } = useTTS()
  const [progress, setProgress] = useState(0)
  const [scriptExpanded, setScriptExpanded] = useState(false)
  const [ttsError, setTtsError] = useState(false)
  const progressRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const narration = getNarration(poi, depthTier)

  // Reset on POI or depth change
  useEffect(() => {
    stop()
    setProgress(0)
    if (progressRef.current) clearInterval(progressRef.current)
  }, [poi.id, depthTier, stop])

  // Fake progress bar while playing
  useEffect(() => {
    if (isPlaying && narration) {
      const duration = narration.duration_sec * 1000
      const interval = 250
      progressRef.current = setInterval(() => {
        setProgress((p) => {
          const next = p + (interval / duration) * 100
          return next >= 100 ? 100 : next
        })
      }, interval)
    } else {
      if (progressRef.current) clearInterval(progressRef.current)
    }
    return () => {
      if (progressRef.current) clearInterval(progressRef.current)
    }
  }, [isPlaying, narration])

  // Auto-expand script on TTS error
  useEffect(() => {
    if (error) {
      setTtsError(true)
      setScriptExpanded(true)
    }
  }, [error])

  const handlePlay = () => {
    if (!narration) return
    setTtsError(false)
    setProgress(0)
    speak(narration.script, narration.audio_url ?? undefined)
  }

  const handlePause = () => stop()

  const statusText = () => {
    if (isLoading) return 'Generating audio...'
    if (isPlaying) return narration?.audio_url ? 'Playing' : 'Playing (live TTS)'
    if (ttsError) return 'Audio unavailable — transcript shown below'
    return 'Tap ▶ to hear narration'
  }

  return (
    <div className="flex flex-col gap-4">
      {/* POI photo */}
      {poi.photo_url && (
        <div className="relative h-44 rounded-xl overflow-hidden">
          <img
            src={poi.photo_url}
            alt={poi.name}
            loading="lazy"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-ink/90" />
        </div>
      )}

      {/* Stop header */}
      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <span className="text-xs font-sans font-medium text-stone tracking-widest uppercase">
            Stop {poi.position} of {totalStops}
          </span>
          {poi.walk_note && (
            <span className="flex items-center gap-1 text-[11px] text-stone bg-white/5 border border-white/10 rounded-full px-2 py-0.5">
              <MapPin className="w-2.5 h-2.5" />
              {poi.walk_note}
            </span>
          )}
        </div>

        <h2 className="font-serif text-3xl text-cream leading-tight">{poi.name}</h2>
        {poi.tagline && (
          <p className="font-serif italic text-stone-light text-base">{poi.tagline}</p>
        )}
      </div>

      {/* Categories */}
      {poi.categories.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {poi.categories.map((cat) => (
            <Badge key={cat} label={cat} />
          ))}
        </div>
      )}

      {/* Depth selector */}
      <DepthSelector value={depthTier} onChange={onDepthChange} />

      {/* Player card */}
      <div className="rounded-2xl overflow-hidden" style={{ background: 'var(--navy)' }}>
        <div className="p-5 flex flex-col gap-4">
          {/* Waveform */}
          <Waveform isPlaying={isPlaying} isLoading={isLoading} />

          {/* Progress bar */}
          <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gold rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>

          {/* Controls */}
          <Controls
            isPlaying={isPlaying}
            isLoading={isLoading}
            onPlay={handlePlay}
            onPause={handlePause}
            onPrev={onPrev}
            onNext={onNext}
            hasPrev={poi.position > 1}
            hasNext={poi.position < totalStops}
          />

          {/* Status text */}
          <p className="text-center text-xs text-stone font-sans">{statusText()}</p>
        </div>
      </div>

      {/* Script panel */}
      {narration && (
        <div
          className="rounded-xl overflow-hidden border-l-4"
          style={{
            background: 'var(--parchment)',
            borderLeftColor: 'var(--gold)',
          }}
        >
          <button
            onClick={() => setScriptExpanded((v) => !v)}
            className="w-full flex items-center justify-between px-4 py-3 hover:bg-black/5 transition-colors"
            aria-expanded={scriptExpanded}
          >
            <span className="flex items-center gap-2 text-xs font-sans font-semibold tracking-widest uppercase text-stone">
              <FileText className="w-3.5 h-3.5" />
              Narration Script
            </span>
            {scriptExpanded ? (
              <ChevronUp className="w-4 h-4 text-stone" />
            ) : (
              <ChevronDown className="w-4 h-4 text-stone" />
            )}
          </button>

          {(scriptExpanded || ttsError) && (
            <div className="px-4 pb-4 max-h-64 overflow-y-auto">
              <p className="font-sans text-sm leading-relaxed text-ink">{narration.script}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export function Player(props: PlayerProps) {
  return (
    <ErrorBoundary
      fallback={
        <div className="rounded-xl p-4" style={{ background: 'var(--parchment)', borderLeft: '4px solid var(--gold)' }}>
          <p className="text-xs font-sans font-semibold tracking-widest uppercase text-stone mb-2">
            Transcript
          </p>
          <p className="font-sans text-sm leading-relaxed text-ink">
            {getNarration(props.poi, props.depthTier)?.script ?? 'No narration available for this stop.'}
          </p>
        </div>
      }
    >
      <PlayerInner {...props} />
    </ErrorBoundary>
  )
}
