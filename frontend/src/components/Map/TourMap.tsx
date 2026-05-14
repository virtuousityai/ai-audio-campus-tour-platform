import { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Polyline, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { POI } from '@/types'
import { ErrorBoundary } from '../ErrorBoundary'

// Fix default marker icon issue with Vite
delete (L.Icon.Default.prototype as { _getIconUrl?: unknown })._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function makeNumberedIcon(
  num: number,
  variant: 'active' | 'completed' | 'upcoming'
) {
  const colors = {
    active: { bg: '#B8860B', text: '#fff', border: '#D4A843' },
    completed: { bg: '#7A6E5F', text: '#F7F2E8', border: '#B5ADA0' },
    upcoming: { bg: '#1B2A4A', text: '#F7F2E8', border: '#B8860B' },
  }
  const c = colors[variant]
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="40" viewBox="0 0 32 40">
      <ellipse cx="16" cy="36" rx="6" ry="3" fill="rgba(0,0,0,0.25)"/>
      <path d="M16 0 C7.16 0 0 7.16 0 16 C0 26 16 40 16 40 C16 40 32 26 32 16 C32 7.16 24.84 0 16 0Z" fill="${c.bg}" stroke="${c.border}" stroke-width="1.5"/>
      <text x="16" y="20" text-anchor="middle" dominant-baseline="central" font-family="DM Sans, sans-serif" font-size="12" font-weight="600" fill="${c.text}">${num}</text>
    </svg>
  `
  return L.divIcon({
    html: svg,
    iconSize: [32, 40],
    iconAnchor: [16, 40],
    popupAnchor: [0, -40],
    className: '',
  })
}

function MapRecenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap()
  useEffect(() => {
    map.panTo([lat, lng], { animate: true, duration: 0.5 })
  }, [lat, lng, map])
  return null
}

interface TourMapProps {
  pois: POI[]
  currentIndex: number
  completedIndices: Set<number>
  onPoiSelect: (index: number) => void
}

function TourMapInner({ pois, currentIndex, completedIndices, onPoiSelect }: TourMapProps) {
  if (pois.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-navy/50 rounded-xl text-stone-light text-sm font-sans">
        No stops to display
      </div>
    )
  }

  const currentPoi = pois[currentIndex]
  const center: [number, number] = currentPoi
    ? [currentPoi.lat, currentPoi.lng]
    : [pois[0].lat, pois[0].lng]

  const polylinePositions: [number, number][] = pois.map((p) => [p.lat, p.lng])

  return (
    <div className="rounded-xl overflow-hidden" style={{ height: '340px' }}>
      <MapContainer
        center={center}
        zoom={16}
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
      >
        {/* CartoDB Voyager tiles */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
          subdomains="abcd"
          maxZoom={20}
        />

        {/* Dashed gold polyline */}
        <Polyline
          positions={polylinePositions}
          pathOptions={{
            color: '#B8860B',
            weight: 2,
            opacity: 0.7,
            dashArray: '8 6',
          }}
        />

        {/* Markers */}
        {pois.map((poi, idx) => {
          const variant =
            idx === currentIndex
              ? 'active'
              : completedIndices.has(idx)
                ? 'completed'
                : 'upcoming'

          return (
            <Marker
              key={poi.id}
              position={[poi.lat, poi.lng]}
              icon={makeNumberedIcon(poi.position, variant)}
            >
              <Popup>
                <div className="font-sans text-ink min-w-[140px]">
                  <p className="font-semibold text-sm mb-1">{poi.name}</p>
                  {poi.tagline && (
                    <p className="text-xs text-stone mb-2">{poi.tagline}</p>
                  )}
                  <button
                    onClick={() => onPoiSelect(idx)}
                    className="text-xs text-white bg-gold rounded px-2 py-1 hover:bg-gold-light transition-colors"
                  >
                    Go to this stop
                  </button>
                </div>
              </Popup>
            </Marker>
          )
        })}

        {/* Auto-center on current POI */}
        {currentPoi && (
          <MapRecenter lat={currentPoi.lat} lng={currentPoi.lng} />
        )}
      </MapContainer>
    </div>
  )
}

const MapFallback = ({ pois }: { pois: POI[] }) => (
  <div className="rounded-xl border border-white/10 p-4">
    <p className="text-stone-light text-sm font-sans mb-3">Map unavailable — use stop list below</p>
    <ol className="space-y-2">
      {pois.map((poi) => (
        <li key={poi.id} className="flex items-start gap-2 text-sm font-sans text-cream">
          <span className="w-5 h-5 rounded-full bg-gold/20 border border-gold/40 flex items-center justify-center text-xs text-gold flex-shrink-0 mt-0.5">
            {poi.position}
          </span>
          <span>{poi.name}</span>
        </li>
      ))}
    </ol>
  </div>
)

export function TourMap(props: TourMapProps) {
  return (
    <ErrorBoundary fallback={<MapFallback pois={props.pois} />}>
      <TourMapInner {...props} />
    </ErrorBoundary>
  )
}
