import { create } from 'zustand'
import type { DepthTier } from '@/types'

interface TourStore {
  activeTourId: string | null
  currentPoiIndex: number
  depthTier: DepthTier
  isPlaying: boolean
  completedPoiIndices: Set<number>
  setActiveTour: (tourId: string) => void
  setCurrentPoi: (index: number) => void
  setDepthTier: (tier: DepthTier) => void
  setIsPlaying: (playing: boolean) => void
  markPoiComplete: (index: number) => void
  resetSession: () => void
}

const defaultState = {
  activeTourId: null,
  currentPoiIndex: 0,
  depthTier: 'guide' as DepthTier,
  isPlaying: false,
  completedPoiIndices: new Set<number>(),
}

export const useTourStore = create<TourStore>()((set) => ({
  ...defaultState,

  setActiveTour: (tourId) =>
    set({
      activeTourId: tourId,
      currentPoiIndex: 0,
      isPlaying: false,
      completedPoiIndices: new Set(),
    }),

  setCurrentPoi: (index) =>
    set((state) => ({
      currentPoiIndex: index,
      isPlaying: state.isPlaying ? false : state.isPlaying,
    })),

  setDepthTier: (tier) => set({ depthTier: tier, isPlaying: false }),

  setIsPlaying: (playing) => set({ isPlaying: playing }),

  markPoiComplete: (index) =>
    set((state) => {
      const next = new Set(state.completedPoiIndices)
      next.add(index)
      return { completedPoiIndices: next }
    }),

  resetSession: () =>
    set({
      ...defaultState,
      completedPoiIndices: new Set<number>(),
    }),
}))
