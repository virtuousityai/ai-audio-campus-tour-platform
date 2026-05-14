import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { X, Map as MapIcon, BookOpen, Star, Trophy } from 'lucide-react'
import { useTour } from '@/hooks/useTour'
import { useTourStore } from '@/store/tourStore'
import { useUserStore } from '@/store/userStore'
import { Player } from '@/components/Player/Player'
import { TourMap } from '@/components/Map/TourMap'
import { Skeleton } from '@/components/ui/Skeleton'
import { ErrorState } from '@/components/ui/ErrorState'

type Tab = 'guide' | 'map'

const XP_PER_STOP = 10
const XP_TOUR_COMPLETE = 50

export function TourPlayer() {
  const { tourId } = useParams<{ tourId: string }>()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('guide')
  const [showCompletion, setShowCompletion] = useState(false)
  const [earnedXP, setEarnedXP] = useState(0)

  const { setActiveTour, resetSession } = useTourStore()
  const { addCompletedPoi, addCompletedTour, addXP } = useUserStore()

  const {
    pois,
    currentPoi,
    currentPoiIndex,
    depthTier,
    completedPoiIndices,
    isLoading,
    error,
    setCurrentPoi,
    setDepthTier,
    markPoiComplete,
  } = useTour(tourId ?? null)

  // Activate tour in store on mount
  useEffect(() => {
    if (tourId) setActiveTour(tourId)
    return () => {
      // Don't reset on unmount — keep state if user navigates back
    }
  }, [tourId, setActiveTour])

  const handlePrev = () => {
    if (currentPoiIndex > 0) {
      setCurrentPoi(currentPoiIndex - 1)
    }
  }

  const handleNext = () => {
    const nextIdx = currentPoiIndex + 1

    // Mark current as complete
    if (currentPoi && !completedPoiIndices.has(currentPoiIndex)) {
      markPoiComplete(currentPoiIndex)
      addCompletedPoi(currentPoi.id)
      addXP(XP_PER_STOP)
      setEarnedXP((x) => x + XP_PER_STOP)
    }

    if (nextIdx >= pois.length) {
      // Tour complete
      if (tourId) {
        addCompletedTour(tourId)
        addXP(XP_TOUR_COMPLETE)
        setEarnedXP((x) => x + XP_TOUR_COMPLETE)
      }
      setShowCompletion(true)
    } else {
      setCurrentPoi(nextIdx)
    }
  }

  const handlePoiSelect = (index: number) => {
    setCurrentPoi(index)
    setActiveTab('guide')
  }

  const handleExit = () => {
    resetSession()
    navigate(-1)
  }

  // Completion screen
  if (showCompletion) {
    return (
      <div
        className="min-h-screen flex flex-col items-center justify-center px-6 text-center gap-6"
        style={{ background: 'var(--ink)' }}
      >
        <div className="w-20 h-20 rounded-full bg-gold/20 border-2 border-gold flex items-center justify-center">
          <Trophy className="w-10 h-10 text-gold" />
        </div>
        <div>
          <h2 className="font-serif text-4xl text-cream mb-2">Tour Complete!</h2>
          <p className="font-sans text-stone-light text-base">
            You explored all {pois.length} stops.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-gold/10 border border-gold/30 rounded-full px-6 py-3">
          <Star className="w-5 h-5 text-gold" />
          <span className="font-sans font-semibold text-gold text-lg">+{earnedXP} XP earned</span>
        </div>
        <button
          onClick={handleExit}
          className="mt-4 font-sans text-sm text-stone-light underline underline-offset-2 hover:text-cream transition-colors"
        >
          Back to tours
        </button>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen" style={{ background: 'var(--ink)' }}>
      {/* Fixed header */}
      <header
        className="sticky top-0 z-20 px-4 py-3 flex items-center justify-between border-b border-white/10"
        style={{ background: 'var(--navy)' }}
      >
        <div className="flex-1 min-w-0">
          {isLoading ? (
            <Skeleton className="h-4 w-32" />
          ) : (
            <p className="text-sm font-sans font-medium text-cream truncate">
              {pois[0]?.tour_id ? 'Campus Tour' : 'Audio Tour'}
            </p>
          )}
        </div>
        <button
          onClick={handleExit}
          className="w-8 h-8 rounded-full flex items-center justify-center text-stone-light hover:text-cream hover:bg-white/10 transition-all active:scale-90 flex-shrink-0"
          aria-label="Exit tour"
        >
          <X className="w-4 h-4" />
        </button>
      </header>

      {/* Progress dots */}
      {!isLoading && pois.length > 0 && (
        <div className="px-4 py-3 flex items-center justify-center gap-1.5 flex-wrap">
          {pois.map((_, idx) => (
            <button
              key={idx}
              onClick={() => handlePoiSelect(idx)}
              aria-label={`Go to stop ${idx + 1}`}
              className={`
                rounded-full transition-all duration-200
                ${idx === currentPoiIndex
                  ? 'w-4 h-2 bg-gold'
                  : completedPoiIndices.has(idx)
                    ? 'w-2 h-2 bg-gold/40'
                    : 'w-2 h-2 bg-white/20'
                }
              `}
            />
          ))}
        </div>
      )}

      {/* Tab bar */}
      <div className="flex border-b border-white/10 px-4" style={{ background: 'var(--navy)' }}>
        <button
          onClick={() => setActiveTab('guide')}
          className={`flex items-center gap-1.5 px-4 py-3 text-sm font-sans font-medium border-b-2 transition-colors ${
            activeTab === 'guide'
              ? 'border-gold text-gold'
              : 'border-transparent text-stone hover:text-cream'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          Guide
        </button>
        <button
          onClick={() => setActiveTab('map')}
          className={`flex items-center gap-1.5 px-4 py-3 text-sm font-sans font-medium border-b-2 transition-colors ${
            activeTab === 'map'
              ? 'border-gold text-gold'
              : 'border-transparent text-stone hover:text-cream'
          }`}
        >
          <MapIcon className="w-3.5 h-3.5" />
          Map
        </button>
      </div>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {isLoading && (
          <div className="px-4 py-6 flex flex-col gap-4 max-w-lg mx-auto">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-48 w-full" />
          </div>
        )}

        {error && !isLoading && (
          <div className="px-4 py-8">
            <ErrorState
              message={`Could not load tour stops: ${error.message}`}
            />
          </div>
        )}

        {!isLoading && !error && !currentPoi && (
          <div className="px-4 py-8">
            <ErrorState message="No stops found for this tour." />
          </div>
        )}

        {!isLoading && !error && currentPoi && (
          <>
            {/* Guide tab */}
            {activeTab === 'guide' && (
              <div className="px-4 py-6 max-w-lg mx-auto flex flex-col gap-6">
                <Player
                  poi={currentPoi}
                  totalStops={pois.length}
                  depthTier={depthTier}
                  onDepthChange={setDepthTier}
                  onPrev={handlePrev}
                  onNext={handleNext}
                />

                {/* Stop list */}
                <div>
                  <h3 className="text-xs font-sans font-semibold text-stone tracking-widest uppercase mb-3">
                    All Stops
                  </h3>
                  <div className="flex flex-col gap-2">
                    {pois.map((poi, idx) => {
                      const isActive = idx === currentPoiIndex
                      const isCompleted = completedPoiIndices.has(idx)

                      return (
                        <button
                          key={poi.id}
                          onClick={() => handlePoiSelect(idx)}
                          className={`
                            w-full text-left flex items-center gap-3 p-3 rounded-xl transition-all duration-150 active:scale-[0.98]
                            ${isActive
                              ? 'bg-gold/10 border border-gold/30'
                              : 'bg-white/5 border border-transparent hover:border-white/20'
                            }
                          `}
                        >
                          <span
                            className={`
                              w-6 h-6 rounded-full flex items-center justify-center text-xs font-sans font-semibold flex-shrink-0
                              ${isActive
                                ? 'bg-gold text-white'
                                : isCompleted
                                  ? 'bg-stone/30 text-stone'
                                  : 'bg-white/10 text-stone-light'
                              }
                            `}
                          >
                            {poi.position}
                          </span>
                          <div className="min-w-0">
                            <p
                              className={`font-sans text-sm font-medium truncate ${
                                isActive ? 'text-cream' : isCompleted ? 'text-stone' : 'text-stone-light'
                              }`}
                            >
                              {poi.name}
                            </p>
                            {poi.tagline && (
                              <p className="text-xs text-stone truncate">{poi.tagline}</p>
                            )}
                          </div>
                          {isCompleted && !isActive && (
                            <span className="ml-auto text-xs text-stone flex-shrink-0">Done</span>
                          )}
                        </button>
                      )
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* Map tab */}
            {activeTab === 'map' && (
              <div className="px-4 py-6 max-w-lg mx-auto flex flex-col gap-4">
                <TourMap
                  pois={pois}
                  currentIndex={currentPoiIndex}
                  completedIndices={completedPoiIndices}
                  onPoiSelect={handlePoiSelect}
                />

                {/* Legend */}
                <div>
                  <h3 className="text-xs font-sans font-semibold text-stone tracking-widest uppercase mb-3">
                    Stop Legend
                  </h3>
                  <div className="flex flex-col gap-2">
                    {pois.map((poi, idx) => {
                      const isActive = idx === currentPoiIndex
                      const isCompleted = completedPoiIndices.has(idx)

                      return (
                        <button
                          key={poi.id}
                          onClick={() => {
                            handlePoiSelect(idx)
                            setActiveTab('guide')
                          }}
                          className="w-full text-left flex items-center gap-3 py-2 border-b border-white/5 last:border-0 hover:text-cream transition-colors"
                        >
                          <span
                            className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-sans font-bold flex-shrink-0 ${
                              isActive
                                ? 'bg-gold text-white'
                                : isCompleted
                                  ? 'bg-stone/40 text-stone-light'
                                  : 'bg-navy border border-gold/50 text-gold'
                            }`}
                          >
                            {poi.position}
                          </span>
                          <span
                            className={`font-sans text-sm ${
                              isActive
                                ? 'text-cream font-medium'
                                : isCompleted
                                  ? 'text-stone line-through'
                                  : 'text-stone-light'
                            }`}
                          >
                            {poi.name}
                          </span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* Bottom safe area */}
        <div className="h-8" style={{ paddingBottom: 'env(safe-area-inset-bottom)' }} />
      </main>
    </div>
  )
}
