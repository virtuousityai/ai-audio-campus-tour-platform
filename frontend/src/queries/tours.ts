import { useQuery } from '@tanstack/react-query'
import { fetchTours, fetchTour } from '@/lib/api'
import type { Tour } from '@/types'

export function useTours(cityId: string | undefined) {
  return useQuery<Tour[], Error>({
    queryKey: ['tours', cityId],
    queryFn: () => fetchTours(cityId!),
    enabled: Boolean(cityId),
    staleTime: 10 * 60 * 1000,
  })
}

export function useTourDetail(tourId: string | undefined) {
  return useQuery<Tour, Error>({
    queryKey: ['tour', tourId],
    queryFn: () => fetchTour(tourId!),
    enabled: Boolean(tourId),
    staleTime: 10 * 60 * 1000,
  })
}
