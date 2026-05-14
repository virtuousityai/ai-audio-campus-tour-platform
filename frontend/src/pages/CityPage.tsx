import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, MapPin } from 'lucide-react'
import { useCity } from '@/queries/cities'
import { TourCard } from '@/components/Discovery/TourCard'
import { Skeleton } from '@/components/ui/Skeleton'
import { ErrorState } from '@/components/ui/ErrorState'

export function CityPage() {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const { data, isLoading, error, refetch } = useCity(slug)

  const location = data ? [data.state, data.country].filter(Boolean).join(', ') : ''

  return (
    <div className="min-h-screen" style={{ background: 'var(--ink)' }}>
      {/* Hero */}
      <header
        className="relative px-4 pt-10 pb-8"
        style={{
          background: data?.hero_image
            ? `linear-gradient(160deg, rgba(27,42,74,0.95) 0%, rgba(28,24,18,0.98) 100%), url(${data.hero_image}) center/cover no-repeat`
            : 'var(--navy)',
        }}
      >
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-sm font-sans text-stone-light hover:text-cream transition-colors mb-6 active:scale-95"
          aria-label="Back to home"
        >
          <ArrowLeft className="w-4 h-4" />
          All Campuses
        </button>

        {isLoading ? (
          <div className="flex flex-col gap-2">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-10 w-56" />
          </div>
        ) : data ? (
          <>
            <p className="text-xs font-sans text-stone tracking-widest uppercase mb-1">
              {data.university}
            </p>
            <h1 className="font-serif text-4xl font-bold text-cream leading-tight mb-2">
              {data.name}
            </h1>
            {location && (
              <span className="flex items-center gap-1 text-sm font-sans text-stone-light">
                <MapPin className="w-3.5 h-3.5" />
                {location}
              </span>
            )}
            {data.description && (
              <p className="mt-3 text-sm font-sans text-stone-light leading-relaxed max-w-sm">
                {data.description}
              </p>
            )}
          </>
        ) : null}
      </header>

      {/* Tours section */}
      <main className="px-4 py-6 max-w-lg mx-auto">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-serif text-2xl text-cream">Available Tours</h2>
          {data?.tours && (
            <span className="text-xs font-sans text-stone">
              {data.tours.length} {data.tours.length === 1 ? 'tour' : 'tours'}
            </span>
          )}
        </div>

        {isLoading && (
          <div className="flex flex-col gap-4">
            {[1, 2].map((i) => (
              <div key={i} className="rounded-2xl p-4 bg-white/5">
                <Skeleton className="h-6 w-48 mb-2" />
                <Skeleton className="h-4 w-64 mb-3" />
                <div className="flex gap-2">
                  <Skeleton className="h-4 w-16" />
                  <Skeleton className="h-4 w-16" />
                </div>
              </div>
            ))}
          </div>
        )}

        {error && !isLoading && (
          <ErrorState
            message={`Could not load tours: ${error.message}`}
            onRetry={() => void refetch()}
          />
        )}

        {!isLoading && !error && data?.tours?.length === 0 && (
          <ErrorState message="No tours available for this campus yet." />
        )}

        {!isLoading && !error && data?.tours && data.tours.length > 0 && (
          <div className="flex flex-col gap-4">
            {data.tours.map((tour) => (
              <TourCard key={tour.id} tour={tour} />
            ))}
          </div>
        )}
      </main>

      <div className="h-8" />
    </div>
  )
}
