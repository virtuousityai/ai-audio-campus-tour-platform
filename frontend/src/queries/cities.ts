import { useQuery } from '@tanstack/react-query'
import { fetchCities, fetchCity } from '@/lib/api'
import type { City, Tour } from '@/types'

export function useCities() {
  return useQuery<City[], Error>({
    queryKey: ['cities'],
    queryFn: fetchCities,
    staleTime: 10 * 60 * 1000,
  })
}

export function useCity(slug: string | undefined) {
  return useQuery<City & { tours: Tour[] }, Error>({
    queryKey: ['city', slug],
    queryFn: () => fetchCity(slug!),
    enabled: Boolean(slug),
    staleTime: 10 * 60 * 1000,
  })
}
