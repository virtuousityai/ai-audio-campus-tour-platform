import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { DepthTier } from '@/types'

interface UserStore {
  preferredDepth: DepthTier
  preferredCategories: string[]
  preferredDuration: number
  xp: number
  streakCurrent: number
  completedTourIds: string[]
  completedPoiIds: string[]
  setPreferredDepth: (d: DepthTier) => void
  setPreferredCategories: (cats: string[]) => void
  addCompletedPoi: (poiId: string) => void
  addCompletedTour: (tourId: string) => void
  addXP: (amount: number) => void
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      preferredDepth: 'guide',
      preferredCategories: [],
      preferredDuration: 60,
      xp: 0,
      streakCurrent: 0,
      completedTourIds: [],
      completedPoiIds: [],

      setPreferredDepth: (d) => set({ preferredDepth: d }),
      setPreferredCategories: (cats) => set({ preferredCategories: cats }),

      addCompletedPoi: (poiId) =>
        set((state) => ({
          completedPoiIds: state.completedPoiIds.includes(poiId)
            ? state.completedPoiIds
            : [...state.completedPoiIds, poiId],
        })),

      addCompletedTour: (tourId) =>
        set((state) => ({
          completedTourIds: state.completedTourIds.includes(tourId)
            ? state.completedTourIds
            : [...state.completedTourIds, tourId],
        })),

      addXP: (amount) => set((state) => ({ xp: state.xp + amount })),
    }),
    {
      name: 'audio-tour-user',
    }
  )
)
