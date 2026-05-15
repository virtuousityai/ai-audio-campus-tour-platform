# 🎧 AI Audio Campus Tour Platform

> **GPS-triggered audio walking tours for college campuses — with depth tiers no competitor has.**

A freemium Progressive Web App (PWA) where visitors walk a campus and their phone automatically narrates each landmark as they approach it. Every stop offers three depths of learning: a 60-second Snapshot, a 4-minute Guide, and a 12-minute Deep Dive. No competitor in the $174M audio tour market offers this.

**Live cities:** Princeton University · University of Michigan · Texas A&M University

---

## Why This Exists

Every audio tour app — VoiceMap, Rick Steves, izi.TRAVEL, GPSmyCity — delivers one fixed narration per stop. The Blinkist pattern (quick summary vs. full story vs. expert layer) has been standard in audiobooks and education for a decade. It has never been applied to walking tours.

This platform fills that gap. A rushed parent gets the 60-second Snapshot. A prospective student gets the 4-minute Guide. A history enthusiast gets the full 12-minute Deep Dive with primary sources and hidden stories. Same stop, same GPS trigger, three completely different experiences — chosen with a single tap.

---

## Screenshots

> _Coming soon — v0.3.0 will include a live demo URL_

---

## Feature Overview

### ✅ Shipped (v0.2.0)

| Feature | Description |
|---------|-------------|
| **GPS Auto-Advance** | `watchPosition` + Haversine proximity detection. Walk into a stop's radius → narration auto-starts |
| **3-Tier Depth System** | Snapshot (60s) · Guide (3–4min) · Deep Dive (8–12min) per stop |
| **Freemium Gate** | Snapshot + Guide free; Deep Dive requires Explorer subscription |
| **AI Text-to-Speech** | Puter.js (`xai/leo` voice, free) → Web Speech API fallback |
| **Audio Cache** | First-play audio cached as blob URL; replays instantly |
| **Offline-First PWA** | Two-cache service worker: app shell (cache-first) + API (network-first) |
| **Offline Banner** | Detects connection loss; slides in from bottom with iOS safe-area support |
| **GPS Status Badge** | Pulsing green dot when GPS is active; orange on permission error |
| **XP System** | +10 per stop completed, +50 per full tour; persisted in localStorage |
| **Error Boundaries** | Isolated at Map, Player, Discovery, GPS seams — no cascade failures |

### 🔜 Coming Next (v0.3.0)

| Feature | Description |
|---------|-------------|
| **AI Guide Chat** | Ask questions about any stop; Claude answers in the persona of a campus guide |
| **Daily Discovery** | Featured tour/POI of the day; visit streak with XP bonus |
| **Playback Speed** | 0.8×, 1.0×, 1.2×, 1.5× controls on the audio player |
| **Chapter Markers** | Skip to named chapters within Deep Dive narrations |

### 📋 Planned (Phase 3+)

| Feature | Description |
|---------|-------------|
| **Badges & Collections** | "Big Ten Explorer", "Ivy League Walk", "Deep Diver" achievement system |
| **Creator CMS** | Admin dashboard for adding cities, tours, and POI content without code |
| **Claude Narration Gen** | Input POI bullet points → Claude generates all 3 tiers automatically |
| **Group Mode** | Synchronized playback for campus tour groups _(Coming Soon)_ |
| **Revenue Share** | Creator marketplace with revenue sharing _(Coming Soon)_ |

---

## Content

### Seeded Universities (v0.2.0)

| City | University | Stops | Narrations |
|------|-----------|-------|-----------|
| Princeton, NJ | Princeton University | 7 | 21 |
| Ann Arbor, MI | University of Michigan | 8 | 24 |
| College Station, TX | Texas A&M University | 8 | 24 |

**Total: 23 stops · 69 narrations** — all hand-written at three depth levels.

### Sample Tour Stops

**Princeton:** Nassau Hall · Firestone Library · Princeton Chapel · McCosh Hall · Blair Arch · Whitman College · Princeton Stadium

**University of Michigan:** Michigan Stadium (The Big House) · UMMA · Burton Tower · Angell Hall · Law Quad · The Diag · Michigan Union · Nichols Arboretum

**Texas A&M:** Kyle Field · Academic Building · Century Tree · Rudder Tower · Memorial Student Center · Simpson Drill Field · Bonfire Memorial · Albritton Bell Tower

---

## Architecture

```
Browser / iOS / Android (PWA)
        │
        ▼
   nginx :3030
    ├── /          → frontend (React + Vite + TypeScript)  :5174
    └── /api/      → backend  (FastAPI + asyncpg)          :8001
                                    │
                            ┌───────┴───────┐
                        PostgreSQL        Redis
                          :5433            :6380
```

### Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | React 18 + Vite + TypeScript | Fast HMR, PWA-ready, type-safe components |
| **Styling** | Tailwind CSS | Mobile-first, design tokens, no cascade surprises |
| **Server state** | TanStack Query v5 | Stale-while-revalidate, offline cache, typed defaults |
| **Client state** | Zustand v4 | Persisted `userStore`, session-only `tourStore` |
| **Backend** | FastAPI + asyncpg | Async-native, fast, Python ecosystem |
| **Database** | PostgreSQL 16 | Relational schema: City → Tour → POI → Narration |
| **Cache / Sessions** | Redis 7 | Ready for rate limits, auth sessions, pub/sub |
| **TTS** | Puter.js (xai/leo) | Free, natural voice, falls back to Web Speech API |
| **GPS** | Geolocation API | `watchPosition` + Haversine distance formula |
| **Proxy** | Nginx (Alpine) | Single entry point; WebSocket-ready for future live features |
| **Containers** | Docker Compose | 5 services; one-command local setup |

### Data Model

```
City
 └── Tour (one per city in Phase 1)
      └── POI  (7–8 per tour, GPS coordinates + radius)
           └── Narration × 3  (snapshot · guide · deepdive)
```

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows/Linux)
- Git

### 1. Clone

```bash
git clone https://github.com/virtuousityai/ai-audio-campus-tour-platform.git
cd ai-audio-campus-tour-platform
```

### 2. Start

```bash
docker compose up -d
```

All 5 containers start automatically. First run builds images and seeds the database (~60s).

### 3. Open

```
http://localhost:3030
```

On iOS Safari or Android Chrome, tap **Add to Home Screen** for the full PWA experience.

### 4. Verify the API

```bash
# All 3 cities
curl http://localhost:8001/cities | python3 -m json.tool

# POIs for a tour (replace with actual tour ID from /cities response)
curl "http://localhost:8001/pois?tour_id=<id>" | python3 -m json.tool

# Health check
curl http://localhost:8001/health
```

### Ports

| Service | URL | Notes |
|---------|-----|-------|
| App (via Nginx) | http://localhost:3030 | Use this for the PWA |
| Frontend (direct) | http://localhost:5174 | Vite dev server with HMR |
| Backend API | http://localhost:8001 | FastAPI + auto-docs at `/docs` |
| PostgreSQL | localhost:5433 | user: `audio_tour`, db: `audio_tour` |
| Redis | localhost:6380 | No auth in dev |

### API Docs

FastAPI auto-generates interactive docs:
```
http://localhost:8001/docs        (Swagger UI)
http://localhost:8001/redoc       (ReDoc)
```

---

## Project Structure

```
ai-audio-campus-tour-platform/
│
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                    FastAPI app, CORS, startup seed
│   ├── api/
│   │   ├── cities.py              GET /cities
│   │   ├── tours.py               GET /tours?city_slug=
│   │   └── pois.py                GET /pois?tour_id=  (with inline narrations)
│   ├── models/
│   │   ├── city.py
│   │   ├── tour.py
│   │   ├── poi.py
│   │   └── narration.py
│   └── db/
│       ├── session.py             AsyncSessionLocal
│       ├── init.sql               Schema (run once at postgres init)
│       └── seed.py                Princeton + UMICH + TAMU seed data
│
└── frontend/
    ├── Dockerfile
    ├── vite.config.ts
    ├── public/
    │   ├── sw.js                  Two-cache service worker
    │   └── manifest.json          PWA manifest
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── hooks/
        │   ├── useTTS.ts          Puter.js TTS → Web Speech API
        │   ├── useGPS.ts          watchPosition + Haversine proximity
        │   └── useOffline.ts      navigator.onLine + events
        ├── stores/
        │   ├── userStore.ts       XP, completed tours, tier (persisted)
        │   └── tourStore.ts       Current POI, active depth tab (session)
        ├── pages/
        │   ├── Home.tsx           City discovery
        │   └── TourPlayer.tsx     Main player with GPS auto-advance
        └── components/
            ├── Player/
            │   ├── DepthSelector.tsx   Snapshot / Guide / Deep Dive pills
            │   ├── AudioPlayer.tsx     Play/pause/progress
            │   └── POIMap.tsx          Leaflet map with stop markers
            └── ui/
                ├── GPSBadge.tsx        GPS status indicator
                └── OfflineBanner.tsx   Offline notification bar
```

---

## Depth Tier Design

The depth selector is the product's core differentiator. Every stop has three completely independent narrations — not one narration with sections, but three different scripts written for three different visitor mindsets.

```
┌──────────────────────────────────────────────┐
│  Nassau Hall · Princeton University          │
│                                              │
│  [ Snapshot · 1 min ]  [ Guide · 4 min ]    │
│  [ 🔒 Deep Dive · 10 min ]  ← Explorer only │
│                                              │
│  ▶  ━━━━━━━━━━━━━━━━━━━━━━━  2:14 / 4:00   │
│                                              │
│  "Still curious? Ask your guide..."  →       │
└──────────────────────────────────────────────┘
```

| Tier | Length | Audience | Price |
|------|--------|----------|-------|
| **Snapshot** | 60–90s | Visitors passing by | Free |
| **Guide** | 3–4 min | Most tour-goers | Free |
| **Deep Dive** | 8–12 min | Enthusiasts, students, researchers | Explorer ($4.99/mo) |

---

## GPS Behavior

```
Phone GPS → watchPosition (3s update, high accuracy)
         → Haversine distance to all POIs
         → nearestPoiIndex: first POI within gps_radius_m (default 50m)
         → TourPlayer detects change → switches active stop + starts Guide narration
         → prevNearestRef guard → prevents re-trigger on every position update
```

Error handling:
- **Permission denied** → orange GPS badge, manual tap-to-select stays functional
- **Unavailable** → silent fallback, user can tap any stop manually
- **Timeout** → retries automatically via watchPosition

---

## Resilience Principles

This app was designed to survive aggressive vibe-coding sessions without cascade failures.

1. **Error Boundaries at every seam** — Map, Player, Discovery, GPS each have isolated error boundaries. One crash doesn't take down the others.
2. **TanStack Query typed defaults** — all `useQuery` calls return `data = []` not `undefined`. No "cannot read property of undefined" crashes.
3. **TTS fallback chain** — Puter.js fails → Web Speech API. Both fail → silent, user sees transcript.
4. **Service worker two-cache** — app shell and API cached separately. A bad API response doesn't break the shell.
5. **Seed idempotency** — each city has its own check. Restarting the backend never double-inserts or partially seeds.
6. **TypeScript strict mode** — `noUnusedLocals`, `noUnusedParameters`, `strict: true`. Errors caught at build time.

---

## Development Notes

### TypeScript check

```bash
docker exec audio-tour-frontend npx tsc --noEmit
```

### After frontend changes — bump SW cache

In `frontend/public/sw.js`:
```js
const SHELL_CACHE = 'audio-tour-v2'   // increment version
const API_CACHE   = 'audio-tour-api-v2'
```
Then hard-reload (Cmd+Shift+R) and clear site data on iOS Safari.

### Rebuild after Dockerfile changes

```bash
docker compose down && docker compose up --build -d
```

### Database access

```bash
docker exec -it audio-tour-postgres psql -U audio_tour -d audio_tour
```

---

## Roadmap

```
v0.1.0  ✅  Foundation — React/FastAPI scaffold, Princeton seed, TTS, DepthSelector
v0.2.0  ✅  GPS + Multi-city — auto-advance, UMICH/TAMU, offline PWA
v0.3.0  🔜  AI Chat — ask-your-guide Claude integration, streaming responses
v0.3.1  🔜  Engagement — Daily Discovery, visit streak, playback speed
v0.4.0  📋  Creator CMS — admin dashboard, Claude narration generation
v0.5.0  📋  Social — badges, cross-city collections, sharing
v1.0.0  📋  Public launch — auth, Stripe, native app wrapper (Capacitor)
```

---

## Contributing

This is a private product in active development. Content contributions (new cities, corrected narrations) welcome — open an issue with the city name and a list of 6–8 landmark stops.

---

## License

Private — All Rights Reserved · © 2026 Virtuousity AI
