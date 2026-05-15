import { useState, useEffect, useRef, useCallback } from 'react'

export interface GPSPosition {
  lat: number
  lng: number
  accuracy: number
}

export type GPSStatus = 'idle' | 'watching' | 'denied' | 'unavailable' | 'error'

export interface UseGPSReturn {
  position: GPSPosition | null
  status: GPSStatus
  nearestPoiIndex: number | null
  startWatching: () => void
  stopWatching: () => void
}

export function haversineDistance(
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number
): number {
  const R = 6371000 // Earth radius in meters
  const φ1 = (lat1 * Math.PI) / 180
  const φ2 = (lat2 * Math.PI) / 180
  const Δφ = ((lat2 - lat1) * Math.PI) / 180
  const Δλ = ((lng2 - lng1) * Math.PI) / 180
  const a =
    Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

export function useGPS(
  pois: Array<{ lat: number; lng: number; gps_radius_m: number }>
): UseGPSReturn {
  const [position, setPosition] = useState<GPSPosition | null>(null)
  const [status, setStatus] = useState<GPSStatus>('idle')
  const [nearestPoiIndex, setNearestPoiIndex] = useState<number | null>(null)
  const watchIdRef = useRef<number | null>(null)
  const poisRef = useRef(pois)

  // Keep pois ref up to date without re-triggering effects
  useEffect(() => {
    poisRef.current = pois
  }, [pois])

  // Recompute nearest POI whenever position or pois change
  useEffect(() => {
    if (!position) {
      setNearestPoiIndex(null)
      return
    }

    const nearest = poisRef.current.findIndex(
      (poi) =>
        haversineDistance(position.lat, position.lng, poi.lat, poi.lng) <=
        poi.gps_radius_m
    )

    setNearestPoiIndex(nearest === -1 ? null : nearest)
  }, [position])

  const startWatching = useCallback(() => {
    if (!navigator.geolocation) {
      setStatus('unavailable')
      return
    }

    if (watchIdRef.current !== null) return // already watching

    setStatus('watching')

    watchIdRef.current = navigator.geolocation.watchPosition(
      (geoPos) => {
        setPosition({
          lat: geoPos.coords.latitude,
          lng: geoPos.coords.longitude,
          accuracy: geoPos.coords.accuracy,
        })
        setStatus('watching')
      },
      (err) => {
        switch (err.code) {
          case 1: // PERMISSION_DENIED
            setStatus('denied')
            break
          case 2: // POSITION_UNAVAILABLE
            setStatus('unavailable')
            break
          case 3: // TIMEOUT
            setStatus('error')
            break
          default:
            setStatus('error')
        }
      },
      {
        enableHighAccuracy: true,
        maximumAge: 3000,
        timeout: 10000,
      }
    )
  }, [])

  const stopWatching = useCallback(() => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current)
      watchIdRef.current = null
    }
    setStatus('idle')
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (watchIdRef.current !== null && navigator.geolocation) {
        navigator.geolocation.clearWatch(watchIdRef.current)
        watchIdRef.current = null
      }
    }
  }, [])

  // Handle case where geolocation is not available at all
  useEffect(() => {
    if (!navigator.geolocation) {
      setStatus('unavailable')
    }
  }, [])

  return { position, status, nearestPoiIndex, startWatching, stopWatching }
}
