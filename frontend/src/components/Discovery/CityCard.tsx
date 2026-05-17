import { useNavigate } from 'react-router-dom'
import { MapPin, Map } from 'lucide-react'
import type { City } from '@/types'

interface CityCardProps {
  city: City
}

export function CityCard({ city }: CityCardProps) {
  const navigate = useNavigate()

  const location = [city.state, city.country].filter(Boolean).join(', ')

  return (
    <button
      onClick={() => navigate(`/city/${city.slug}`)}
      className="group w-full text-left rounded-2xl overflow-hidden border border-white/10 hover:border-gold/40 transition-all duration-200 active:scale-[0.98] focus:outline-none focus-visible:ring-2 focus-visible:ring-gold"
      aria-label={`${city.university} — ${city.name}`}
    >
      {/* Hero image section */}
      {city.hero_image ? (
        <div className="relative h-40 overflow-hidden">
          <img
            src={city.hero_image}
            alt={city.name}
            loading="lazy"
            className="w-full h-full object-cover"
          />
          {/* Dark gradient overlay at bottom for text readability */}
          <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-black/20 to-black/70" />
          {/* Gold accent line at top */}
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-gold/0 via-gold to-gold/0 group-hover:from-gold/30 group-hover:via-gold group-hover:to-gold/30 transition-all duration-300" />
          {/* Text overlaid on image */}
          <div className="absolute bottom-0 left-0 right-0 px-5 pb-4 pt-2">
            <p className="text-xs font-sans text-white/80 tracking-widest uppercase mb-0.5">
              {city.university}
            </p>
            <h3 className="font-serif text-2xl font-bold text-white leading-tight group-hover:text-gold-light transition-colors duration-200">
              {city.name}
            </h3>
          </div>
        </div>
      ) : (
        /* Fallback: color gradient hero area */
        <div
          className="relative px-5 pt-6 pb-8 overflow-hidden"
          style={{ background: 'linear-gradient(160deg, var(--navy) 0%, var(--ink) 100%)' }}
        >
          {/* Gold accent line */}
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-gold/0 via-gold to-gold/0 group-hover:from-gold/30 group-hover:via-gold group-hover:to-gold/30 transition-all duration-300" />

          <p className="text-xs font-sans text-stone tracking-widest uppercase mb-1">
            {city.university}
          </p>
          <h3 className="font-serif text-3xl font-bold text-cream leading-tight group-hover:text-gold-light transition-colors duration-200">
            {city.name}
          </h3>

          {city.description && (
            <p className="mt-2 text-sm font-sans text-stone-light leading-relaxed line-clamp-2">
              {city.description}
            </p>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="px-5 py-3 bg-white/5 border-t border-white/10 flex items-center justify-between">
        <span className="flex items-center gap-1.5 text-xs font-sans text-stone">
          <MapPin className="w-3.5 h-3.5" />
          {location}
        </span>
        <span className="flex items-center gap-1.5 text-xs font-sans font-medium text-gold-light bg-gold/10 rounded-full px-3 py-1">
          <Map className="w-3 h-3" />
          {city.tour_count} {city.tour_count === 1 ? 'tour' : 'tours'}
        </span>
      </div>
    </button>
  )
}
