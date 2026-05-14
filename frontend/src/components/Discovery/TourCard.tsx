import { useNavigate } from 'react-router-dom'
import { Clock, MapPin, ChevronRight } from 'lucide-react'
import type { Tour } from '@/types'
import { Badge } from '../ui/Badge'

interface TourCardProps {
  tour: Tour
}

function formatDistance(meters: number): string {
  if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)} km`
  }
  return `${meters} m`
}

export function TourCard({ tour }: TourCardProps) {
  const navigate = useNavigate()

  return (
    <button
      onClick={() => navigate(`/tour/${tour.id}`)}
      className="group w-full text-left rounded-2xl border border-white/10 hover:border-gold/40 overflow-hidden transition-all duration-200 active:scale-[0.98] focus:outline-none focus-visible:ring-2 focus-visible:ring-gold"
      style={{ background: 'rgba(255,255,255,0.03)' }}
      aria-label={`${tour.name} tour`}
    >
      {/* Cover image strip */}
      {tour.cover_image && (
        <div
          className="h-24 w-full"
          style={{
            background: `linear-gradient(180deg, rgba(27,42,74,0.3) 0%, rgba(28,24,18,0.85) 100%), url(${tour.cover_image}) center/cover no-repeat`,
          }}
        />
      )}

      <div className="p-4">
        {/* Name + arrow */}
        <div className="flex items-start justify-between gap-2 mb-1">
          <h3 className="font-serif text-xl text-cream group-hover:text-gold-light transition-colors duration-150 leading-tight">
            {tour.name}
          </h3>
          <ChevronRight className="w-4 h-4 text-stone flex-shrink-0 mt-1 group-hover:text-gold transition-colors" />
        </div>

        {/* Tagline */}
        {tour.tagline && (
          <p className="text-sm font-sans text-stone-light mb-3 leading-snug">{tour.tagline}</p>
        )}

        {/* Meta row */}
        <div className="flex items-center gap-3 mb-3">
          <span className="flex items-center gap-1 text-xs font-sans text-stone">
            <Clock className="w-3.5 h-3.5" />
            {tour.duration_minutes} min
          </span>
          <span className="flex items-center gap-1 text-xs font-sans text-stone">
            <MapPin className="w-3.5 h-3.5" />
            {tour.stop_count} stops
          </span>
          <span className="text-xs font-sans text-stone">
            {formatDistance(tour.distance_meters)}
          </span>
        </div>

        {/* Category badges */}
        {tour.categories.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {tour.categories.slice(0, 3).map((cat) => (
              <Badge key={cat} label={cat} />
            ))}
            {tour.categories.length > 3 && (
              <span className="text-xs text-stone font-sans self-center">
                +{tour.categories.length - 3}
              </span>
            )}
          </div>
        )}
      </div>
    </button>
  )
}
