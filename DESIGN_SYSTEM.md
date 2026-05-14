# AI Audio Tour Platform — Architecture & Design System

**Status:** Phase 1 Planning  
**Updated:** 2026-05-13

---

## 🎯 Product Vision

**From:** Enterprise-only audio tours (AACP MVP)  
**To:** Multi-city freemium PWA (consumer + creator economy)  
**Model:** Spotify-like discovery + Airbnb-like creator marketplace

---

## 📐 System Architecture

### Core Layers

```
┌─────────────────────────────────────────────────┐
│  Browser/Mobile (PWA + iOS/Android Wrapper)    │
├─────────────────────────────────────────────────┤
│  React + TypeScript (Vite)                      │
│  State: TanStack Query + Zustand                │
│  Styling: Tailwind + CSS Modules (resilient)    │
├─────────────────────────────────────────────────┤
│  NextJS API Routes (BFF Pattern)                │
├─────────────────────────────────────────────────┤
│  FastAPI Backend (Python)                       │
│  - Multi-tenant Tour Management                 │
│  - User/Creator Auth & Profiles                 │
│  - Subscription & Freemium Tiers                │
│  - Claude API Integration (narration gen)       │
│  - Audio Processing & Streaming                 │
├─────────────────────────────────────────────────┤
│  Data Layer                                      │
│  - PostgreSQL (multi-tenant, normalized)        │
│  - Redis (cache, session, rate limits)          │
│  - S3-compatible (audio files, images)          │
├─────────────────────────────────────────────────┤
│  Docker Container (production-ready)            │
└─────────────────────────────────────────────────┘
```

### Why This Stack?

| Component | Choice | Why |
|-----------|--------|-----|
| **Frontend** | React + Vite | Fast HMR, PWA-ready, iOS/Android bridging |
| **State** | TanStack Query + Zustand | Offline-first queries, minimal boilerplate |
| **Backend** | NextJS API + FastAPI | BFF for client logic, FastAPI for heavy lifting (Claude, audio) |
| **Database** | PostgreSQL | Multi-tenant row-level security, JSONB for tours, relational auth |
| **Cache** | Redis | Session cache, rate limits, streaming buffer |
| **Storage** | S3 | Audio CDN, image optimization, multipart uploads |
| **Container** | Docker | Dev parity, one-command deploy, Kubernetes-ready |

---

## 🛠️ Component Philosophy: Maximum Resilience

### Principle 1: No Silent Failures
Every component must **fail loud and visible**:
- Network errors → Toast notification with retry button
- Missing data → Skeleton loader → graceful empty state
- Audio playback failures → User can still see transcript + map

### Principle 2: Boundary Isolation
Components are wrapped in **Error Boundaries** at logical seams:
- Tour player (audio playback)
- Discovery feed (tour listing)
- Creator CMS (form handling)
- Map view (geolocation)

Each boundary has a fallback UI.

### Principle 3: Defensive Data Fetching
```typescript
// ✅ Pattern: Query with fallback
const { data = [], isError, error } = useQuery({
  queryKey: ['tours', cityId],
  queryFn: fetchTours,
  staleTime: 5 * 60 * 1000,
  retry: 2,
  retryDelay: exponentialBackoff,
})

// ✅ Pattern: Optimistic updates with rollback
const { mutate } = useMutation({
  mutationFn: saveRating,
  onMutate: (data) => {
    // Optimistic update
    queryClient.setQueryData(..., oldData => ({...}))
    return oldData // for rollback
  },
  onError: (err, _, rollback) => rollback?.(), 
})
```

### Principle 4: Offline-First Architecture
```typescript
// TanStack Query + Workbox
// - All tour data cached on first visit
// - Audio cached (configurable per tier)
// - Syncs on reconnect
// - User sees "offline mode" badge
```

### Principle 5: Progressive Enhancement
1. Load text + map → playable immediately
2. Stream audio metadata → can play without full file
3. Load images → cached, low priority
4. Load analytics → deferred, doesn't block UX

---

## 🏗️ Recommended Build Phases

### Phase 1: MVP Core (4-6 weeks)
**Goal:** Single city, fully playable tours, freemium trial

- [ ] Database schema (multi-tenant, tours, users, audio_files)
- [ ] Auth (email/social, freemium tier system)
- [ ] Tour player (map + audio + transcript, offline capable)
- [ ] Discovery page (featured tours, search by location)
- [ ] Audio generation pipeline (Claude → MP3 → S3)
- [ ] Creator onboarding (minimal CMS: create tour, add POIs, generate narration)
- [ ] Docker dev environment + compose file
- [ ] Stripe trial setup (30-day free)

**Outputs:**
- `/clients/tours/{id}` → play any published tour
- `/create` → minimal tour builder
- `/discover` → browse tours by city
- `docker compose up` → full stack locally

---

### Phase 2: Multi-City + Creator Tools (4-6 weeks)
**Goal:** Multi-city discovery, creator marketplace, analytics

- [ ] City management (tour admins can add routes, POIs)
- [ ] Creator profiles (bio, tour list, ratings)
- [ ] Advanced CMS (bulk POI upload, CSV import, batch narration)
- [ ] Tour ratings + reviews (user feedback)
- [ ] Creator analytics (plays, completion rate, ratings, revenue)
- [ ] Revenue share system (Stripe Connect for creators)
- [ ] i18n foundation (English + 3 major languages)

**Outputs:**
- `/city/{slug}` → all tours in a city
- `/creators/{id}` → creator portfolio
- `/dashboard/analytics` → creator insights
- Revenue reports for creators

---

### Phase 3: Growth & Monetization (4-6 weeks)
**Goal:** Premium features, viral discovery, scaling

- [ ] Freemium tiers (free tour 5/month, premium unlimited)
- [ ] AI recommendations (what to play next)
- [ ] Saved tours (playlists, favorites)
- [ ] Social sharing (pre-built links, referral code)
- [ ] Premium narration voices (vs Claude default)
- [ ] Map routing (turn-by-turn to next POI)
- [ ] Audio downloads (offline entire tours)

**Outputs:**
- `/upgrade` → tier upsell
- Sharing preview cards
- Download progress UI
- Referral tracking

---

### Phase 4: Platform Depth (Ongoing)
**Goal:** Creator economy, content moderation, data insights

- [ ] User-generated tours (anyone can create)
- [ ] Content moderation (AI flagging, human review)
- [ ] Advanced analytics (heatmaps, drop-off points)
- [ ] Audio post-processing (music, sound effects)
- [ ] Seasonal tours (time-limited, event-based)
- [ ] Collections (curated tour bundles by category)
- [ ] API for partners (venues can embed tours on their site)

**Outputs:**
- Moderation dashboard
- Heatmap visualization
- Partner integration docs

---

## ❓ Strategic Questions (World-Class Polish)

### 1. **Monetization & Economics**
- Are creators split-revenue based? (e.g., Spotify 70/30 model for premium plays)
- Or is it a marketplace (creators pay to publish, get % of subscription tier)?
- For free tours: how do you prevent spam/low-quality content?
- Subscription tiers: what's the feature diff between Free/Premium/Pro?

### 2. **Content Strategy**
- Who curates the "Featured Tours" on discovery?
- Should tours have categories (historical, food, nature, nightlife)?
- Minimum quality bar for user-generated content? (verification, review process?)
- Rights/licensing: how do you handle copyrighted location descriptions?

### 3. **User Acquisition**
- Is this targeting **travelers** (tourists) or **locals** (repeat users)?
- Day-trippers vs multi-day visitors? (affects offline audio strategy)
- Which cities first? (NYC, Paris, Tokyo? Or smaller high-engagement cities?)
- Partnerships with tourism boards, hotels, airports?

### 4. **Localization & Accessibility**
- Multiple languages per tour (English narration + translations)?
- Or multiple tour versions (same POI, diff language creators)?
- Closed captions for all narration?
- Accessibility: voice controls for hands-free playback while walking?

### 5. **Audio Strategy**
- Default: Claude text-to-speech vs hiring voice actors?
- Premium narration tiers? (celebrity voices, professional actors?)
- Music/ambient sound: royalty-free library vs dynamic generation?
- Audio quality (bitrate, format)? Mobile bandwidth vs quality trade-off?

### 6. **Creator Onboarding**
- Minimum friction: can someone create a tour in 10 minutes?
- Require verification (email, phone, credit card)?
- First tour approval before publishing, or auto-publish with moderation?
- Revenue unlock (payout threshold)? (e.g., need 100 plays before earning)

### 7. **Engagement Loops**
- Notifications: "Tour near you", "Creator you follow uploaded new tour"?
- Gamification: badges for completing X tours, collecting cities?
- Social: follow other users, see their tour history?
- Challenges: "Complete 3 tours in Rome this week"?

### 8. **Data & Privacy**
- Location tracking: do you track user GPS paths (for heatmaps)?
- Consent model: per-city, per-tour, global?
- Data retention: how long to keep tour history?
- GDPR/CCPA compliance: easy data export, deletion?

### 9. **Resilience & Scale**
- Expected concurrent users per city? (affects CDN, streaming architecture)
- Audio streaming: progressive (start playing before full download) vs full download?
- Degradation mode: what happens if Claude API goes down? (canned narration, transcript-only mode?)
- Offline strategy: cache entire tour or just partial audio?

### 10. **Metrics & Success**
- North star: creators publishing, users completing tours, playtime?
- Creator success rate: what % of tours get >10 plays?
- Retention: weekly active users, re-play rate?
- Revenue per user (ARPU)?
- Creator revenue target (to make content creation worth their time)?

---

## 🐳 Docker & Dev Setup

```dockerfile
# Dockerfile (multi-stage)
FROM node:20-alpine as build-frontend
WORKDIR /app/frontend
COPY . .
RUN npm ci && npm run build

FROM python:3.11-slim as backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.9'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: audio_tours_dev
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:dev_password@postgres:5432/audio_tours_dev
      REDIS_URL: redis://redis:6379
      CLAUDE_API_KEY: ${CLAUDE_API_KEY}

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
    environment:
      VITE_API_URL: http://localhost:8000
```

**Local dev:**
```bash
docker compose up
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Postgres: localhost:5432
# Redis: localhost:6379
```

---

## 📊 Next Steps

1. **Clarify vision** → Answer 5-10 questions above
2. **Lock schema** → Database design for multi-tenant, tours, creators, subscriptions
3. **Auth foundation** → Email/social login, tier system, refresh tokens
4. **Player MVP** → Playable tour with offline cache
5. **Creator CMS** → Minimal tour builder
6. **Iterate** → Phases 2-4 based on learnings
