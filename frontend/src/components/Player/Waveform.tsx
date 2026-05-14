interface WaveformProps {
  isPlaying: boolean
  isLoading: boolean
}

const BAR_COUNT = 24

// Stagger delays and base heights for visual variety
const barConfig = Array.from({ length: BAR_COUNT }, (_, i) => ({
  delay: (i * 0.05) % 0.6,
  baseHeight: 20 + ((i * 7 + 13) % 40), // deterministic pseudo-random heights
}))

export function Waveform({ isPlaying, isLoading }: WaveformProps) {
  return (
    <div
      className="flex items-center justify-center gap-[3px] h-12"
      role="img"
      aria-label={isLoading ? 'Loading audio' : isPlaying ? 'Audio playing' : 'Audio paused'}
    >
      {barConfig.map((bar, i) => (
        <WaveBar
          key={i}
          index={i}
          delay={bar.delay}
          baseHeight={bar.baseHeight}
          isPlaying={isPlaying}
          isLoading={isLoading}
        />
      ))}
    </div>
  )
}

interface WaveBarProps {
  index: number
  delay: number
  baseHeight: number
  isPlaying: boolean
  isLoading: boolean
}

function WaveBar({ delay, baseHeight, isPlaying, isLoading }: WaveBarProps) {
  if (isLoading) {
    return (
      <div
        className="w-1 rounded-full bg-gold/40 animate-pulse"
        style={{
          height: `${baseHeight * 0.5}%`,
          animationDelay: `${delay}s`,
          animationDuration: '1.5s',
        }}
      />
    )
  }

  if (isPlaying) {
    return (
      <div
        className="w-1 rounded-full bg-gold origin-bottom"
        style={{
          height: `${baseHeight}%`,
          animation: `waveBar 0.8s ease-in-out ${delay}s infinite alternate`,
        }}
      />
    )
  }

  // Paused: minimal flat bars
  return (
    <div
      className="w-1 rounded-full bg-gold/30 transition-all duration-500"
      style={{ height: '4px' }}
    />
  )
}
