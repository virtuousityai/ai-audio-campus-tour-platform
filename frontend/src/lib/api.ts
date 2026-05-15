import type { City, Tour, POI } from '@/types'

// Empty string → relative URLs → requests go through nginx (/api/ prefix is stripped there)
// Set VITE_API_URL explicitly only when running outside Docker (e.g. local Vite dev server)
const API_BASE = import.meta.env.VITE_API_URL ?? ''

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

// Returns city detail with tours[] nested — no separate fetchTours call needed
export function fetchCity(slug: string): Promise<City & { tours: Tour[] }> {
  return apiFetch<City & { tours: Tour[] }>(`/api/cities/${slug}`)
}

export function fetchTours(cityId: string): Promise<Tour[]> {
  return apiFetch<Tour[]>(`/api/tours?city_id=${cityId}`)
}

export function fetchTour(tourId: string): Promise<Tour> {
  return apiFetch<Tour>(`/api/tours/${tourId}`)
}

export function fetchPOIs(tourId: string): Promise<POI[]> {
  return apiFetch<POI[]>(`/api/pois?tour_id=${tourId}`)
}
