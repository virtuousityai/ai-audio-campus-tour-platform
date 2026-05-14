import { useState, useEffect, useRef, useCallback } from 'react'

declare global {
  interface Window {
    puter?: {
      ai?: {
        txt2speech: (
          text: string,
          options?: { provider?: string; voice?: string }
        ) => Promise<HTMLAudioElement>
      }
    }
  }
}

interface TTSState {
  isLoading: boolean
  isPlaying: boolean
  error: string | null
}

interface UseTTSReturn extends TTSState {
  speak: (script: string) => void
  stop: () => void
}

// Simple hash for cache key
function hashString(str: string): string {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const chr = str.charCodeAt(i)
    hash = (hash << 5) - hash + chr
    hash |= 0
  }
  return String(hash)
}

let puterLoaded = false

function loadPuter(): Promise<void> {
  return new Promise((resolve) => {
    if (puterLoaded || window.puter) {
      puterLoaded = true
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = 'https://js.puter.com/v2/'
    script.async = true
    script.onload = () => {
      puterLoaded = true
      resolve()
    }
    script.onerror = () => resolve() // resolve anyway — will fall back to speechSynthesis
    document.head.appendChild(script)
  })
}

export function useTTS(): UseTTSReturn {
  const [state, setState] = useState<TTSState>({
    isLoading: false,
    isPlaying: false,
    error: null,
  })

  const currentAudioRef = useRef<HTMLAudioElement | null>(null)
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null)
  const audioCache = useRef<Map<string, string>>(new Map()) // hash → object URL

  // Load Puter.js on mount
  useEffect(() => {
    loadPuter().catch(() => {/* silent */})
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopPlayback()
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const stopPlayback = useCallback(() => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause()
      currentAudioRef.current.currentTime = 0
      currentAudioRef.current = null
    }
    if (utteranceRef.current && window.speechSynthesis) {
      window.speechSynthesis.cancel()
      utteranceRef.current = null
    }
    setState({ isLoading: false, isPlaying: false, error: null })
  }, [])

  const speakWithSpeechSynthesis = useCallback((script: string) => {
    if (!window.speechSynthesis) {
      setState({ isLoading: false, isPlaying: false, error: 'TTS not supported on this device' })
      return
    }
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(script)
    utterance.rate = 0.95
    utterance.pitch = 1.0
    utterance.volume = 1.0

    // Pick a natural-sounding voice if available
    const voices = window.speechSynthesis.getVoices()
    const preferred = voices.find(
      (v) =>
        v.lang.startsWith('en') &&
        (v.name.includes('Samantha') ||
          v.name.includes('Alex') ||
          v.name.includes('Daniel') ||
          v.name.includes('Google'))
    )
    if (preferred) utterance.voice = preferred

    utterance.onstart = () => setState((s) => ({ ...s, isLoading: false, isPlaying: true }))
    utterance.onend = () => setState({ isLoading: false, isPlaying: false, error: null })
    utterance.onerror = (e) => {
      if (e.error === 'interrupted') return
      setState({ isLoading: false, isPlaying: false, error: 'Speech synthesis error' })
    }

    utteranceRef.current = utterance
    setState((s) => ({ ...s, isLoading: false, isPlaying: true }))
    window.speechSynthesis.speak(utterance)
  }, [])

  const speak = useCallback(
    async (script: string) => {
      stopPlayback()
      setState({ isLoading: true, isPlaying: false, error: null })

      const cacheKey = hashString(script)
      const cachedUrl = audioCache.current.get(cacheKey)

      // Try cached audio first
      if (cachedUrl) {
        const audio = new Audio(cachedUrl)
        currentAudioRef.current = audio
        audio.onplay = () => setState({ isLoading: false, isPlaying: true, error: null })
        audio.onended = () => setState({ isLoading: false, isPlaying: false, error: null })
        audio.onerror = () => speakWithSpeechSynthesis(script)
        audio.play().catch(() => speakWithSpeechSynthesis(script))
        return
      }

      // Try Puter.js
      if (window.puter?.ai?.txt2speech) {
        try {
          const audio = await window.puter.ai.txt2speech(script, {
            provider: 'xai',
            voice: 'leo',
          })
          currentAudioRef.current = audio

          // Cache the audio source for replay
          if (audio.src) {
            audioCache.current.set(cacheKey, audio.src)
          }

          audio.onplay = () => setState({ isLoading: false, isPlaying: true, error: null })
          audio.onended = () => setState({ isLoading: false, isPlaying: false, error: null })
          audio.onerror = () => speakWithSpeechSynthesis(script)

          setState((s) => ({ ...s, isLoading: false }))
          await audio.play()
          return
        } catch {
          // Fall through to speechSynthesis
        }
      }

      // Fallback: Web Speech API
      speakWithSpeechSynthesis(script)
    },
    [stopPlayback, speakWithSpeechSynthesis]
  )

  return {
    speak,
    stop: stopPlayback,
    isLoading: state.isLoading,
    isPlaying: state.isPlaying,
    error: state.error,
  }
}
