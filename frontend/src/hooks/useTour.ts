import { useTourStore } from '@/store/tourStore'
import { usePOIs } from '@/queries/pois'
import type { POI, Narration, DepthTier } from '@/types'

interface UseTourReturn {
  pois: POI[]
  currentPoi: POI | null
  currentNarration: Narration | null
  currentPoiIndex: number
  depthTier: DepthTier
  isPlaying: boolean
  completedPoiIndices: Set<number>
  isLoading: boolean
  error: Error | null
  setCurrentPoi: (index: number) => void
  setDepthTier: (tier: DepthTier) => void
  setIsPlaying: (playing: boolean) => void
  markPoiComplete: (index: number) => void
}

export function useTour(tourId: string | null): UseTourReturn {
  const {
    currentPoiIndex,
    depthTier,
    isPlaying,
    completedPoiIndices,
    setCurrentPoi,
    setDepthTier,
    setIsPlaying,
    markPoiComplete,
  } = useTourStore()

  const { data: pois = [], isLoading, error } = usePOIs(tourId)

  const currentPoi: POI | null = pois[currentPoiIndex] ?? null

  const currentNarration: Narration | null =
    currentPoi?.narrations.find((n) => n.depth_tier === depthTier) ??
    currentPoi?.narrations[0] ??
    null

  return {
    pois,
    currentPoi,
    currentNarration,
    currentPoiIndex,
    depthTier,
    isPlaying,
    completedPoiIndices,
    isLoading,
    error: error as Error | null,
    setCurrentPoi,
    setDepthTier,
    setIsPlaying,
    markPoiComplete,
  }
}
