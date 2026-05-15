const CACHE_NAME = 'audio-tour-v1'
const API_CACHE = 'audio-tour-api-v1'

// Install: cache the app shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(['/', '/manifest.json']))
      .then(() => self.skipWaiting())
  )
})

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k !== CACHE_NAME && k !== API_CACHE)
            .map((k) => caches.delete(k))
        )
      )
      .then(() => self.clients.claim())
  )
})

// Fetch strategy:
// - /api/* → network first, fall back to API cache (stale data ok)
// - Navigation (HTML) → network first, fall back to /
// - Static assets (JS/CSS/fonts) → cache first, then network
// - Audio files → cache first (important for offline playback)
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // API calls: network-first, cache fallback
  if (
    url.pathname.startsWith('/api/') ||
    url.pathname.startsWith('/cities') ||
    url.pathname.startsWith('/tours') ||
    url.pathname.startsWith('/pois')
  ) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const clone = res.clone()
          caches.open(API_CACHE).then((c) => c.put(request, clone))
          return res
        })
        .catch(() => caches.match(request))
    )
    return
  }

  // Navigation: network-first, fall back to /
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(
        () => caches.match('/') ?? new Response('Offline', { status: 503 })
      )
    )
    return
  }

  // Static assets: cache-first
  if (
    url.pathname.match(/\.(js|css|woff2?|png|svg|ico)$/) ||
    url.hostname.includes('fonts.googleapis.com') ||
    url.hostname.includes('fonts.gstatic.com')
  ) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached
        return fetch(request).then((res) => {
          const clone = res.clone()
          caches.open(CACHE_NAME).then((c) => c.put(request, clone))
          return res
        })
      })
    )
    return
  }

  // Default: network
  event.respondWith(
    fetch(request).catch(
      () => caches.match(request) ?? Promise.reject('offline')
    )
  )
})
