# AI Audio Campus Tour Platform — Build Plan & Version Log

## Product Vision

Multi-city freemium PWA for GPS-triggered audio walking tours at college campuses.
Core differentiator: **3-tier depth system** (Snapshot 60s / Guide 3–4min / Deep Dive 8–12min).
No competitor has this. Market: $174M audio tour sector.

**Revenue model:** Freemium — Snapshot + Guide free; Deep Dive premium ($4.99/mo Explorer).

---

## Version Log

### v0.3.0 — Stock Photos (City Cards + POI Player)
*2026-05-16 · commit 36e43a1*

**Shipped:**
- CityCard: hero_image renders as 160px photo strip with gradient overlay; navy fallback when null
- Player: poi.photo_url shown as 176px image above stop header; hidden when null
- TourCard: cover_image already wired (no change needed)
- 29 image URLs backfilled via SQL:
  - 3 city heroes + 3 tour covers: Unsplash (atmospheric campus shots, free license)
  - 23 POI photos: Wikimedia Commons (real landmark photos, CC licensed)
- Image sources: Princeton/UMICH/TAMU landmarks — Nassau Hall, Michigan Stadium aerial, Kyle Field panorama, Blair Arch, Law Quad, Century Tree, etc.

---

### v0.1.0 — Phase 1A: Foundation Scaffold
*2026-05-14 · commit e390021*

**Shipped:**
- Docker Compose: 5 containers (postgres, redis, backend, frontend, nginx)
- FastAPI backend with async SQLAlchemy + asyncpg
- PostgreSQL schema: City → Tour → POI → Narration
- React 18 + Vite + TypeScript + Tailwind frontend
- TourPlayer page with DepthSelector (Snapshot / Guide / Deep Dive)
- Puter.js TTS → Web Speech API fallback chain with audio blob cache
- Princeton University seed: 7 POIs × 3 tiers = 21 narrations
- Zustand stores: userStore (persisted) + tourStore (session)
- TanStack Query v5 for server state
- Error boundaries at map, player, discovery, GPS seams

---

### v0.2.0 — Phase 1B: GPS Auto-Advance + Multi-City + Offline PWA
*2026-05-14 · commit c6879ee · tag v0.2.0*

**Shipped:**
- `useGPS` hook: `watchPosition` + Haversine proximity detection
- GPS auto-advance: TourPlayer switches POI + tab when you enter a stop's radius
- `prevNearestRef` dedup guard — prevents re-firing same POI transition on every update
- `GPSBadge` component: pulsing green when watching, orange on error
- `useOffline` hook + `OfflineBanner` component (fixed bottom, iOS safe-area)
- Two-cache service worker: shell (cache-first) + API (network-first with fallback)
- University of Michigan seed: 8 POIs × 3 tiers = 24 narrations
- Texas A&M University seed: 8 POIs × 3 tiers = 24 narrations
- Fixed seed early-return bug (Princeton check blocked UMICH/TAMU insert)
- TypeScript: 0 errors

**Total content:** 3 cities · 3 tours · 23 POIs · 69 narrations

---

## Upcoming Phases

### v0.3.0 — Phase 2A: AI Guide Chat
*Target: next sprint*

**Goal:** Visitor can ask questions about the current POI and get AI-powered answers
in the voice/persona of a campus guide.

**Scope:**
- `/api/chat` endpoint — FastAPI + Claude API (streaming)
- `AiChat` component — bottom sheet, message history, persona prompt per tour
- Free tier: 5 questions/tour; Explorer: unlimited
- Freemium gate: upgrade CTA on 6th question
- Abort on tab switch (don't leave streaming requests dangling)

**Files:**
| File | Change |
|------|--------|
| `backend/api/chat.py` | New — streaming Claude endpoint |
| `backend/main.py` | Add `/chat` route |
| `frontend/src/components/Player/AiChat.tsx` | New — chat bottom sheet |
| `frontend/src/pages/TourPlayer.tsx` | Wire AiChat into player |
| `frontend/src/stores/chatStore.ts` | New — message history per POI |

---

### v0.3.1 — Phase 2B: Daily Discovery + Streak
*Target: sprint +1*

**Goal:** Home screen engagement loop — daily featured tour/POI, visit streak counter.

**Scope:**
- `/api/discovery` endpoint — returns featured city/POI of the day
- `DiscoveryCard` home screen component
- Streak tracking in `userStore` (last visit date, streak count)
- Streak badge on home screen; +25 XP on streak continuation

---

### v0.4.0 — Phase 2C: Playback Speed + Chapter Markers
*Target: sprint +2*

**Goal:** Power-user controls that make Deep Dive tier more useful.

**Scope:**
- Playback speed selector: 0.8×, 1.0×, 1.2×, 1.5× (TTS doesn't support this directly — applies to `<audio>` element)
- Chapter markers within Deep Dive narrations (stored as `chapter_markers: [{label, offset_ms}]` in narration metadata)
- Skip-to-chapter UI in player

---

### v0.5.0 — Phase 3: Creator CMS (Curated Admin)
*Target: Phase 3*

**Goal:** Admin dashboard for adding new cities, tours, and POI content without code.

**Scope:**
- Auth: admin-only JWT (no public signup yet)
- City/Tour/POI CRUD API
- Admin UI: simple form-based CMS
- Claude-assisted narration generation: input POI name + bullet facts → generate all 3 tiers

---

### v0.6.0 — Phase 3: Badges + Collections
*Target: Phase 3*

**Goal:** Gamification layer to drive retention and cross-city exploration.

**Scope:**
- Badge system: First Stop, Tour Complete, 3-City Explorer, Deep Diver
- Cross-city collections: "Big Ten Campuses", "Ivy League Walk"
- Badge display on profile screen

---

## Deferred / Coming Soon

| Feature | Status | Notes |
|---------|--------|-------|
| Group pricing | Coming Soon | Phase 4 |
| Revenue share (creator marketplace) | Coming Soon | Phase 4 |
| Open UGC tours | Coming Soon | Phase 4 — curated only through Phase 3 |
| Native iOS/Android wrapper | Coming Soon | Capacitor.js wrapper after PWA is stable |
| Offline audio download | Coming Soon | IndexedDB + blob storage, Phase 2+ |
| S3 audio storage | Coming Soon | Replace runtime TTS with pre-generated audio in Phase 3 |

---

## Architecture Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-13 | Puter.js TTS (free) over Claude TTS | Zero cost, xai/leo voice is natural, falls back to Web Speech API |
| 2026-05-13 | Runtime TTS (no S3) | Eliminates storage cost and audio upload workflow for Phase 1 |
| 2026-05-13 | Curated content only (no UGC) | Quality control; creator marketplace is Phase 4 |
| 2026-05-13 | 3-tier depth as core UX | Only differentiator vs. all major competitors |
| 2026-05-14 | asyncpg requires Python lists for TEXT[] | PostgreSQL array literals ("{}") fail; always use `["a","b"]` |
| 2026-05-14 | Per-city idempotency in seed | Single early-return on Princeton blocked UMICH/TAMU seed |
