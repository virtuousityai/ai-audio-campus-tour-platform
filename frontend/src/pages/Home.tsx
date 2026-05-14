import { Headphones, Globe2 } from 'lucide-react'
import { useCities } from '@/queries/cities'
import { CityCard } from '@/components/Discovery/CityCard'
import { Skeleton } from '@/components/ui/Skeleton'
import { ErrorState } from '@/components/ui/ErrorState'

export function Home() {
  const { data: cities = [], isLoading, error, refetch } = useCities()

  return (
    <div className="min-h-screen" style={{ background: 'var(--ink)' }}>
      {/* Hero header */}
      <header
        className="relative px-6 pt-16 pb-12 text-center overflow-hidden"
        style={{ background: 'var(--navy)' }}
      >
        {/* Decorative gradient orb */}
        <div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-72 h-72 rounded-full blur-3xl opacity-20 pointer-events-none"
          style={{ background: 'radial-gradient(circle, var(--gold) 0%, transparent 70%)' }}
        />

        <div className="relative z-10 flex flex-col items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gold/10 border border-gold/30 flex items-center justify-center">
            <Headphones className="w-7 h-7 text-gold" />
          </div>

          <div>
            <p className="text-xs font-sans font-medium text-gold tracking-[0.25em] uppercase mb-2">
              Powered by AI
            </p>
            <h1 className="font-serif text-4xl font-bold text-cream leading-tight">
              Audio Campus Tours
            </h1>
            <p className="mt-3 font-sans text-base text-stone-light max-w-xs mx-auto leading-relaxed">
              Walk the stories. Hear the history.
            </p>
          </div>

          <div className="flex items-center gap-1.5 text-xs font-sans text-stone">
            <Globe2 className="w-3.5 h-3.5" />
            GPS-triggered narration · Works offline
          </div>
        </div>
      </header>

      {/* City selection */}
      <main className="px-4 py-8 max-w-lg mx-auto">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-serif text-2xl text-cream">Choose a Campus</h2>
          {!isLoading && !error && (
            <span className="text-xs font-sans text-stone">
              {cities.length} {cities.length === 1 ? 'campus' : 'campuses'}
            </span>
          )}
        </div>

        {isLoading && (
          <div className="flex flex-col gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="rounded-2xl overflow-hidden">
                <Skeleton className="h-32 rounded-none" />
                <div className="p-4 bg-white/5 flex justify-between">
                  <Skeleton className="h-4 w-24" />
                  <Skeleton className="h-4 w-16" />
                </div>
              </div>
            ))}
          </div>
        )}

        {error && !isLoading && (
          <ErrorState
            message={`Could not load campuses: ${error.message}`}
            onRetry={() => void refetch()}
          />
        )}

        {!isLoading && !error && cities.length === 0 && (
          <ErrorState message="No campuses available yet. Check back soon!" />
        )}

        {!isLoading && !error && cities.length > 0 && (
          <div className="flex flex-col gap-4">
            {cities.map((city) => (
              <CityCard key={city.id} city={city} />
            ))}
          </div>
        )}
      </main>

      {/* Bottom safe area */}
      <div className="h-8" />
    </div>
  )
}
