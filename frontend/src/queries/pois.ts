import { useQuery } from '@tanstack/react-query'
import { fetchPOIs } from '@/lib/api'
import type { POI } from '@/types'

export function usePOIs(tourId: string | null) {
  return useQuery<POI[], Error>({
    queryKey: ['pois', tourId],
    queryFn: () => fetchPOIs(tourId!),
    enabled: Boolean(tourId),
    staleTime: 30 * 60 * 1000,
  })
}
