export interface City {
  id: string
  name: string
  slug: string
  university: string
  country: string
  state: string | null
  lat: number
  lng: number
  description: string | null
  hero_image: string | null
  tour_count: number
}

export interface Tour {
  id: string
  city_id: string
  name: string
  slug: string
  tagline: string | null
  duration_minutes: number
  distance_meters: number
  stop_count: number
  categories: string[]
  cover_image: string | null
}

export interface Narration {
  id: string
  poi_id: string
  depth_tier: 'snapshot' | 'guide' | 'deepdive'
  script: string
  duration_sec: number
  audio_url: string | null
}

export interface POI {
  id: string
  tour_id: string
  position: number
  name: string
  tagline: string | null
  lat: number
  lng: number
  gps_radius_m: number
  walk_note: string | null
  categories: string[]
  photo_url: string | null
  narrations: Narration[]
}

export type DepthTier = 'snapshot' | 'guide' | 'deepdive'

export interface UserPrefs {
  preferredDepth: DepthTier
  preferredCategories: string[]
  preferredDuration: number
  xp: number
  streakCurrent: number
  completedTourIds: string[]
  completedPoiIds: string[]
}
