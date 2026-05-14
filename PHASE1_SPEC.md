# Phase 1 Build Spec — AI Audio Tour Platform
*Status: LOCKED  |  Updated: 2026-05-14*

---

## ✅ Decisions Locked

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Creator model** | Curated only (admin adds content) | Quality control; UGC in Phase 3 |
| **Launch cities** | Princeton NJ · Ann Arbor MI · College Station TX | Large college campuses; Princeton content already seeded from template |
| **TTS** | Puter.js (xai/leo voice, free) → Web Speech API fallback | Zero cost, already proven in template, falls back gracefully |
| **Audio storage** | Runtime TTS + IndexedDB cache | No S3 needed in Phase 1; cache on first play |
| **Group pricing** | "Coming Soon" placeholder only | Phase 3 |
| **Revenue share** | "Coming Soon" placeholder only | Phase 3 |
| **Depth tiers** | Snapshot (60s) / Guide (3–4min) / Deep Dive (8–12min) | Core differentiator; Snapshot+Guide free, Deep Dive premium |
| **Monetization** | Freemium (3 tours/month free, unlimited Explorer $4.99/mo) | Single upgrade trigger keeps conversion simple |

---

## 🏗 Project Structure

```
ai-audio-tour-platform/
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env.example
│
├── backend/                         FastAPI · Python 3.11
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── api/
│   │   ├── cities.py               GET /cities, GET /cities/{slug}
│   │   ├── tours.py                GET /tours, GET /tours/{id}
│   │   ├── pois.py                 GET /pois/{tour_id}
│   │   └── users.py                POST /users (register), GET /users/me
│   ├── models/
│   │   ├── city.py
│   │   ├── tour.py
│   │   ├── poi.py
│   │   ├── narration.py
│   │   └── user.py
│   ├── db/
│   │   ├── session.py              SQLAlchemy async engine
│   │   ├── init.sql                schema creation
│   │   └── seeds/
│   │       ├── princeton.json      ← from template
│   │       ├── umich.json
│   │       └── texas_am.json
│   └── services/
│       └── narration_gen.py        Claude API → 3-tier narration text
│
├── frontend/                        React 18 · TypeScript · Vite · Tailwind
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── public/
│   │   ├── manifest.json           PWA manifest
│   │   ├── sw.js                   Service worker (Workbox)
│   │   └── icons/                  PWA icons (all sizes)
│   └── src/
│       ├── main.tsx
│       ├── App.tsx                  Router + ErrorBoundary root
│       │
│       ├── components/
│       │   ├── ui/                  Atoms (never fail)
│       │   │   ├── Button.tsx
│       │   │   ├── Badge.tsx        Category + depth badges
│       │   │   ├── Card.tsx
│       │   │   ├── Skeleton.tsx     Loading states
│       │   │   └── ErrorState.tsx   Fallback UI
│       │   │
│       │   ├── Player/              Tour player (own error boundary)
│       │   │   ├── Player.tsx
│       │   │   ├── DepthSelector.tsx  [SNAPSHOT] [GUIDE] [DEEP DIVE]
│       │   │   ├── Waveform.tsx
│       │   │   ├── ProgressBar.tsx
│       │   │   └── Controls.tsx
│       │   │
│       │   ├── Map/                 Leaflet map (own error boundary)
│       │   │   ├── TourMap.tsx
│       │   │   ├── POIMarker.tsx
│       │   │   └── RoutePolyline.tsx
│       │   │
│       │   ├── Discovery/
│       │   │   ├── CityCard.tsx
│       │   │   ├── TourCard.tsx
│       │   │   └── CategoryFilter.tsx
│       │   │
│       │   └── Onboarding/
│       │       └── PreTourQuiz.tsx  3-question: interests · time · depth
│       │
│       ├── hooks/
│       │   ├── useGPS.ts            Geolocation API + configurable radius trigger
│       │   ├── useTTS.ts            Puter.js → Web Speech API fallback
│       │   ├── useOffline.ts        Online/offline detection + cache status
│       │   ├── useTour.ts           Tour session state (current stop, completed stops)
│       │   └── useDepthTier.ts      User depth preference + per-stop override
│       │
│       ├── store/
│       │   ├── tourStore.ts         Zustand: session, progress, depth tier
│       │   └── userStore.ts         Zustand: profile, preferences, XP, streak
│       │
│       ├── queries/
│       │   ├── cities.ts            TanStack Query: city list + detail
│       │   ├── tours.ts             TanStack Query: tour list + detail
│       │   └── pois.ts              TanStack Query: POIs for a tour
│       │
│       └── pages/
│           ├── Home.tsx             Discover: featured cities + tours
│           ├── CityPage.tsx         All tours in a city
│           ├── TourDetail.tsx       Tour info + start tour CTA
│           ├── TourPlayer.tsx       Active tour: map + player + depth selector
│           └── Profile.tsx          XP, streak, completed tours
│
└── nginx/
    └── nginx.conf                   Reverse proxy: / → frontend, /api → backend
```

---

## 🗄 Database Schema

```sql
-- ────────────────────────────────────────────────
-- CITIES
-- ────────────────────────────────────────────────
CREATE TABLE cities (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name         VARCHAR NOT NULL,
  slug         VARCHAR UNIQUE NOT NULL,   -- 'princeton', 'ann-arbor', 'college-station'
  university   VARCHAR NOT NULL,          -- 'Princeton University', 'University of Michigan', 'Texas A&M'
  country      VARCHAR NOT NULL DEFAULT 'US',
  state        VARCHAR,
  lat          DECIMAL(9,6) NOT NULL,
  lng          DECIMAL(9,6) NOT NULL,
  description  TEXT,
  hero_image   TEXT,
  published    BOOLEAN DEFAULT FALSE,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────
-- TOURS
-- ────────────────────────────────────────────────
CREATE TABLE tours (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  city_id          UUID REFERENCES cities(id) ON DELETE CASCADE,
  name             VARCHAR NOT NULL,
  slug             VARCHAR NOT NULL,
  tagline          TEXT,
  duration_minutes INT,
  distance_meters  INT,
  stop_count       INT DEFAULT 0,
  categories       TEXT[],            -- ['History','Architecture','Student Life']
  cover_image      TEXT,
  published        BOOLEAN DEFAULT FALSE,
  created_at       TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(city_id, slug)
);

-- ────────────────────────────────────────────────
-- POINTS OF INTEREST
-- ────────────────────────────────────────────────
CREATE TABLE pois (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tour_id         UUID REFERENCES tours(id) ON DELETE CASCADE,
  position        INT NOT NULL,           -- order within tour (1-based)
  name            VARCHAR NOT NULL,
  tagline         TEXT,
  lat             DECIMAL(9,6) NOT NULL,
  lng             DECIMAL(9,6) NOT NULL,
  gps_radius_m    INT DEFAULT 30,         -- meters to trigger auto-play
  walk_note       TEXT,                   -- "3 min from previous stop"
  categories      TEXT[],                 -- per-POI category tags
  photo_url       TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tour_id, position)
);

-- ────────────────────────────────────────────────
-- NARRATIONS (3 per POI — one per depth tier)
-- ────────────────────────────────────────────────
CREATE TABLE narrations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  poi_id          UUID REFERENCES pois(id) ON DELETE CASCADE,
  depth_tier      VARCHAR NOT NULL CHECK (depth_tier IN ('snapshot','guide','deepdive')),
  script          TEXT NOT NULL,
  duration_sec    INT,                    -- approximate seconds (word count / 130 WPM)
  audio_url       TEXT,                   -- NULL = runtime TTS; future: CDN URL
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(poi_id, depth_tier)
);

-- ────────────────────────────────────────────────
-- USERS
-- ────────────────────────────────────────────────
CREATE TABLE users (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email               VARCHAR UNIQUE,
  name                VARCHAR,
  tier                VARCHAR DEFAULT 'free' CHECK (tier IN ('free','explorer','local')),
  preferred_depth     VARCHAR DEFAULT 'guide' CHECK (preferred_depth IN ('snapshot','guide','deepdive')),
  preferred_categories TEXT[] DEFAULT '{}',
  preferred_duration  INT DEFAULT 60,     -- minutes
  xp                  INT DEFAULT 0,
  streak_current      INT DEFAULT 0,
  streak_longest      INT DEFAULT 0,
  last_active_date    DATE,
  created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────
-- TOUR SESSIONS (user progress per tour visit)
-- ────────────────────────────────────────────────
CREATE TABLE tour_sessions (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
  tour_id          UUID REFERENCES tours(id),
  depth_tier       VARCHAR DEFAULT 'guide',
  current_poi_id   UUID REFERENCES pois(id),
  pois_completed   UUID[] DEFAULT '{}',
  started_at       TIMESTAMPTZ DEFAULT NOW(),
  last_active_at   TIMESTAMPTZ DEFAULT NOW(),
  completed_at     TIMESTAMPTZ,
  resume_position_sec INT DEFAULT 0       -- seconds into current narration
);

-- ────────────────────────────────────────────────
-- INDEXES
-- ────────────────────────────────────────────────
CREATE INDEX idx_tours_city_id ON tours(city_id);
CREATE INDEX idx_pois_tour_id ON pois(tour_id);
CREATE INDEX idx_narrations_poi_id ON narrations(poi_id);
CREATE INDEX idx_sessions_user_id ON tour_sessions(user_id);
CREATE INDEX idx_sessions_tour_id ON tour_sessions(tour_id);
```

---

## 🎚 TTS Architecture

### Layered TTS (no single point of failure)

```typescript
// hooks/useTTS.ts
export function useTTS() {
  const playScript = async (script: string, opts?: TTSOpts) => {
    // Layer 1: Puter.js (free, high-quality xai/leo voice)
    if (isPuterReady()) {
      try {
        return await puter.ai.txt2speech(script, { provider: 'xai', voice: 'leo' })
      } catch (e) {
        console.warn('Puter TTS failed, falling back to Web Speech API')
      }
    }
    // Layer 2: Web Speech API (browser built-in, always available)
    return webSpeechFallback(script)
  }

  // Cache audio object in IndexedDB keyed by (poi_id + depth_tier)
  // On next visit to same POI: serves from cache, no TTS call needed
}
```

### Audio Caching Strategy

```
First play:   Puter.js generates audio → cache in IndexedDB (poi_id + depth_tier key)
Second play:  Served from IndexedDB — instant, offline-capable
Offline:      All previously-played audio available; unplayed shows "Not cached yet"
Download:     "Download tour" pre-plays all stops silently → populates cache
```

---

## 🗺 Seed Data — 3 Launch Cities

### Princeton (already have from template)
8 stops: Nassau Hall · Maclean House · Art Museum · University Chapel · Blair Arch ·
Prospect House · Cannon Green · Firestone Library

### Ann Arbor / UMICH (to generate)
8 stops: Michigan Stadium · University of Michigan Museum of Art · Burton Memorial Tower ·
Angell Hall · Law Quad · Diag (central mall) · Michigan Union · Nichols Arboretum

### College Station / Texas A&M (to generate)
8 stops: Kyle Field · Academic Building · Rudder Tower · Century Tree · Memorial Student Center ·
Simpson Drill Field · Hullabaloo U (student union) · Bonfire Memorial

---

## ⚡ Resilience Rules (No Component Fails Silently)

### Error Boundaries — one per logical seam

```tsx
// App.tsx
<RootErrorBoundary>
  <Router>
    <MapErrorBoundary fallback={<MapFallback />}>
      <TourMap />
    </MapErrorBoundary>
    <PlayerErrorBoundary fallback={<PlayerFallback />}>
      <TourPlayer />
    </PlayerErrorBoundary>
  </Router>
</RootErrorBoundary>
```

### Network failures → always show something

```tsx
// Every data fetch follows this pattern
const { data: tours = [], isError, isFetching } = useQuery({...})

if (isFetching) return <TourCardSkeleton count={4} />
if (isError)   return <ErrorState message="Couldn't load tours" onRetry={refetch} />
return <TourList tours={tours} />  // never null, always has fallback default []
```

### GPS failure → graceful manual mode

```
GPS granted + working  →  Autoplay when entering POI radius
GPS denied             →  Manual tap to play (no GPS badge shown)
GPS timeout (>10s)     →  Toast "GPS unavailable — tap any stop to play"
```

### TTS failure → transcript always visible

```
TTS succeeds    →  Audio plays + transcript visible below player
TTS fails       →  Toast "Audio unavailable" + transcript auto-expands
Offline + no cache →  Transcript-only mode (no audio attempt)
```

---

## 📱 PWA Requirements

### manifest.json
```json
{
  "name": "Campus Audio Tours",
  "short_name": "AudioTour",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#1B2A4A",
  "background_color": "#1C1812",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### Service Worker (Workbox)
- Cache app shell (HTML/JS/CSS) → instant load
- Cache Leaflet tiles → offline maps work
- Cache API responses → city/tour/POI data survives offline
- Background sync → user progress syncs when reconnected

### iOS Specifics
- `<meta name="apple-mobile-web-app-capable" content="yes">`
- `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">`
- Audio must be triggered by user gesture (iOS restriction) → first tap on Play unlocks audio context

---

## 🐳 Docker Compose

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: audio_tours
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: devpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/db/init.sql:/docker-entrypoint-initdb.d/01_init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:devpassword@postgres:5432/audio_tours
      REDIS_URL: redis://redis:6379
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    volumes:
      - ./backend:/app                # hot reload in dev
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    depends_on:
      - backend
    environment:
      VITE_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app               # hot reload in dev
      - /app/node_modules
    command: npm run dev -- --host

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - frontend
      - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf

volumes:
  postgres_data:
```

**One-command dev start:**
```bash
cp .env.example .env      # add ANTHROPIC_API_KEY
docker compose up         # http://localhost:80
```

---

## 📋 Phase 1 Build Checklist

### Week 1 — Foundation
- [ ] Project scaffold (React+Vite, FastAPI, Docker compose)
- [ ] Database schema + seed data (Princeton from template)
- [ ] API endpoints: /cities, /tours, /pois, /narrations
- [ ] Home page: city discovery cards (Princeton, UMICH, Texas A&M)
- [ ] City page: tour listing with category filter

### Week 2 — Player Core
- [ ] Tour player: map + stop list tabs (from template pattern)
- [ ] Depth tier selector: [SNAPSHOT] [GUIDE] [DEEP DIVE] pills
- [ ] TTS hook: Puter.js primary → Web Speech API fallback
- [ ] Audio cache: IndexedDB keyed by poi_id + depth_tier
- [ ] Completion tracking: stops visited, tour completion

### Week 3 — GPS + Offline
- [ ] GPS hook: Geolocation API with configurable radius
- [ ] Autoplay trigger when entering POI radius
- [ ] Offline detection + transcript-only fallback
- [ ] Service worker: app shell + API response cache
- [ ] PWA manifest + iOS meta tags

### Week 4 — Personalization + Polish
- [ ] Pre-tour quiz: 3 questions (interests · time · depth)
- [ ] Category badges per POI
- [ ] User profile: XP, streak counter, completed tours
- [ ] Resume from position (last stop + audio position saved)
- [ ] Error boundaries on every logical seam
- [ ] Skeleton loaders + empty states everywhere

### Week 5–6 — Content + Freemium
- [ ] UMICH seed data (8 stops, 3 narration tiers each)
- [ ] Texas A&M seed data (8 stops, 3 narration tiers each)
- [ ] Freemium gate: Deep Dive tier → "Upgrade to Explorer"
- [ ] Freemium gate: tour #4 in a month → upgrade modal
- [ ] "Coming Soon" placeholders: Group Tours, Creator Revenue
- [ ] End-to-end test on iPhone Safari + Android Chrome

---

## 🎨 Design Tokens (from Princeton template)

```css
:root {
  --ink:          #1C1812;    /* primary text / background */
  --parchment:    #F7F2E8;    /* card background */
  --cream:        #FDF9F3;    /* page background */
  --gold:         #B8860B;    /* primary accent */
  --gold-light:   #D4A843;    /* hover / active */
  --stone:        #7A6E5F;    /* secondary text */
  --stone-light:  #B5ADA0;    /* muted text */
  --navy:         #1B2A4A;    /* header / player background */
  --rust:         #8B4513;    /* walk time pill */
}

/* Typography */
--font-serif: 'Cormorant Garamond', serif;    /* titles, stop names */
--font-sans:  'DM Sans', sans-serif;          /* body, UI */
```

---

*Ready to build. Run `/start phase1` to scaffold the project.*
