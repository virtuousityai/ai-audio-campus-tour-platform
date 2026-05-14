const CACHE_VERSION = 'v1'
const APP_SHELL_CACHE = `audio-tour-shell-${CACHE_VERSION}`
const STATIC_CACHE = `audio-tour-static-${CACHE_VERSION}`

const APP_SHELL_URLS = ['/', '/manifest.json']

// Install: cache app shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(APP_SHELL_CACHE)
      .then((cache) => cache.addAll(APP_SHELL_URLS))
      .then(() => self.skipWaiting())
  )
})

// Activate: clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k !== APP_SHELL_CACHE && k !== STATIC_CACHE)
            .map((k) => caches.delete(k))
        )
      )
      .then(() => self.clients.claim())
  )
})

// Fetch strategy
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Network-first for API calls
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request))
    return
  }

  // Cache-first for static assets (JS, CSS, fonts, images)
  if (
    request.destination === 'script' ||
    request.destination === 'style' ||
    request.destination === 'font' ||
    request.destination === 'image' ||
    url.pathname.match(/\.(js|css|woff2?|ttf|png|jpg|svg|ico)$/)
  ) {
    event.respondWith(cacheFirst(request, STATIC_CACHE))
    return
  }

  // Stale-while-revalidate for navigation
  if (request.mode === 'navigate') {
    event.respondWith(staleWhileRevalidate(request, APP_SHELL_CACHE))
    return
  }

  // Default: network with cache fallback
  event.respondWith(networkFirst(request))
})

async function networkFirst(request) {
  try {
    const response = await fetch(request)
    return response
  } catch {
    const cached = await caches.match(request)
    return cached || new Response('Offline', { status: 503 })
  }
}

async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request)
  if (cached) return cached

  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(cacheName)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    return new Response('Asset unavailable offline', { status: 503 })
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cached = await cache.match(request)

  const fetchPromise = fetch(request)
    .then((response) => {
      if (response.ok) cache.put(request, response.clone())
      return response
    })
    .catch(() => null)

  // For navigations, fall back to root if specific page not cached
  if (cached) {
    fetchPromise // update in background
    return cached
  }

  const fetched = await fetchPromise
  if (fetched) return fetched

  const root = await cache.match('/')
  return root || new Response('Offline', { status: 503 })
}
