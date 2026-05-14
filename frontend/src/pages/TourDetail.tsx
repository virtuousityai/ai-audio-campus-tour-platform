import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Clock, MapPin, Footprints } from 'lucide-react'
import { useTourDetail } from '@/queries/tours'
import { useTourStore } from '@/store/tourStore'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Skeleton } from '@/components/ui/Skeleton'
import { ErrorState } from '@/components/ui/ErrorState'

function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)} km`
  return `${meters} m`
}

export function TourDetail() {
  const { tourId } = useParams<{ tourId: string }>()
  const navigate = useNavigate()
  const { data: tour, isLoading, error, refetch } = useTourDetail(tourId)
  const { setActiveTour } = useTourStore()

  const handleStartTour = () => {
    if (!tourId) return
    setActiveTour(tourId)
    navigate(`/tour/${tourId}/play`)
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--ink)' }}>
      {/* Header */}
      <header className="px-4 pt-10 pb-8" style={{ background: 'var(--navy)' }}>
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-1.5 text-sm font-sans text-stone-light hover:text-cream transition-colors mb-6 active:scale-95"
          aria-label="Go back"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>

        {isLoading ? (
          <div className="flex flex-col gap-3">
            <Skeleton className="h-10 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <div className="flex gap-3 mt-2">
              <Skeleton className="h-6 w-20" />
              <Skeleton className="h-6 w-20" />
              <Skeleton className="h-6 w-20" />
            </div>
          </div>
        ) : tour ? (
          <>
            <h1 className="font-serif text-3xl font-bold text-cream leading-tight mb-2">
              {tour.name}
            </h1>
            {tour.tagline && (
              <p className="font-serif italic text-stone-light text-lg mb-4">{tour.tagline}</p>
            )}

            {/* Meta row */}
            <div className="flex flex-wrap items-center gap-3 text-sm font-sans text-stone">
              <span className="flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-gold" />
                {tour.duration_minutes} min
              </span>
              <span className="w-px h-4 bg-white/20" />
              <span className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-gold" />
                {tour.stop_count} stops
              </span>
              <span className="w-px h-4 bg-white/20" />
              <span className="flex items-center gap-1.5">
                <Footprints className="w-4 h-4 text-gold" />
                {formatDistance(tour.distance_meters)}
              </span>
            </div>
          </>
        ) : null}
      </header>

      <main className="px-4 py-6 max-w-lg mx-auto">
        {error && !isLoading && (
          <ErrorState
            message={`Could not load tour: ${error.message}`}
            onRetry={() => void refetch()}
          />
        )}

        {!isLoading && tour && (
          <>
            {/* Categories */}
            {tour.categories.length > 0 && (
              <div className="mb-6">
                <h2 className="text-xs font-sans font-semibold text-stone tracking-widest uppercase mb-3">
                  Topics
                </h2>
                <div className="flex flex-wrap gap-2">
                  {tour.categories.map((cat) => (
                    <Badge key={cat} label={cat} />
                  ))}
                </div>
              </div>
            )}

            {/* What to expect */}
            <div className="mb-8">
              <h2 className="text-xs font-sans font-semibold text-stone tracking-widest uppercase mb-3">
                What to Expect
              </h2>
              <div className="rounded-xl border border-white/10 p-4 space-y-3" style={{ background: 'rgba(255,255,255,0.02)' }}>
                <p className="font-sans text-sm text-stone-light leading-relaxed">
                  This self-guided audio tour features AI-narrated stories at {tour.stop_count} key
                  locations across campus. Walk at your own pace and hear {tour.duration_minutes}{' '}
                  minutes of history, culture, and campus life.
                </p>
                <p className="font-sans text-sm text-stone-light leading-relaxed">
                  Choose your narration depth — Snapshot for a quick overview, Guide for the full
                  story, or Deep Dive for academic depth.
                </p>
              </div>
            </div>

            {/* CTA */}
            <Button
              variant="primary"
              className="w-full py-4 text-base"
              onClick={handleStartTour}
            >
              Start Tour →
            </Button>

            <p className="text-center text-xs font-sans text-stone mt-3">
              Works offline · No account required
            </p>
          </>
        )}
      </main>

      <div className="h-8" />
    </div>
  )
}
