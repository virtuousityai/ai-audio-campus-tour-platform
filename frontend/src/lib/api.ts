import type { City, Tour, POI } from '@/types'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText} — ${path}`)
  }
  return res.json() as Promise<T>
}

export function fetchCities(): Promise<City[]> {
  return apiFetch<City[]>('/api/cities')
}

export function fetchCity(slug: string): Promise<City & { tours: Tour[] }> {
  return apiFetch<City & { tours: Tour[] }>(`/api/cities/${slug}`)
}

export function fetchTours(cityId: string): Promise<Tour[]> {
  return apiFetch<Tour[]>(`/api/cities/${cityId}/tours`)
}

export function fetchTour(tourId: string): Promise<Tour> {
  return apiFetch<Tour>(`/api/tours/${tourId}`)
}

export function fetchPOIs(tourId: string): Promise<POI[]> {
  return apiFetch<POI[]>(`/api/tours/${tourId}/pois`)
}
