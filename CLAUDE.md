# AI Audio Campus Tour Platform — Claude Code Context

## What This Is

A multi-city freemium PWA for GPS-triggered audio walking tours at college campuses.
Visitors walk a campus; GPS auto-advances through Points of Interest; each stop has
3 depth tiers (Snapshot 60s / Guide 3–4min / Deep Dive 8–12min). Core differentiator:
no competitor (VoiceMap, Rick Steves, izi.TRAVEL) has depth-tiered narration.

**GitHub:** https://github.com/virtuousityai/ai-audio-campus-tour-platform  
**Current version:** v0.2.0  
**Working directory:** `/Users/sathiyankutty/Documents/claude-code/ai-audio-campus-tour-platform/`

---

## Architecture

```
nginx:3030  ──/──▶  frontend (React/Vite) :5174
            ──/api/──▶  backend (FastAPI) :8001
                            ├── PostgreSQL :5433
                            └── Redis     :6380
```

### Frontend — `frontend/`
- React 18 + TypeScript + Vite + Tailwind CSS (mobile-first PWA)
- **State:** TanStack Query v5 (server cache) + Zustand v4 (local/persisted)
  - `userStore` — persisted to localStorage (XP, completed tours, tier)
  - `tourStore` — session-only (current POI, active depth tab)
- **Key hooks:**
  - `useTTS` — Puter.js (xai/leo) → Web Speech API fallback; audio blob cache
  - `useGPS` — `watchPosition` + Haversine proximity; returns `nearestPoiIndex`
  - `useOffline` — `navigator.onLine` + online/offline events
- **Error Boundaries:** at Map, Player, Discovery, GPS seams — no cascade failures
- **Service worker:** two-cache strategy — `audio-tour-v1` (shell, cache-first) + `audio-tour-api-v1` (API, network-first)
- **Path alias:** `@/` → `src/`

### Backend — `backend/`
- FastAPI + async SQLAlchemy + asyncpg + PostgreSQL
- **Models:** `City → Tour → POI → Narration` (all UUIDs, asyncpg)
- **Endpoints:**
  - `GET /cities` — all published cities with tour_count
  - `GET /tours?city_slug=` — tours for a city
  - `GET /pois?tour_id=` — POIs + inline narrations (3 tiers each), sorted snapshot→guide→deepdive
  - `GET /health` — liveness check
- **Seed:** `db/seed.py` — idempotent, per-city slug checks; runs on every startup
- **CORS:** `http://localhost:5174`, `http://localhost:3030`, `http://localhost:5173`

### Infra — `docker-compose.yml`
| Service | Image | Port | Notes |
|---------|-------|------|-------|
| postgres | postgres:16-alpine | 5433 | healthcheck; `init.sql` creates schema |
| redis | redis:7-alpine | 6380 | session + future rate limits |
| backend | local build | 8001 | hot-reload via volume mount |
| frontend | local build | 5174 | node_modules as anonymous volume |
| nginx | nginx:alpine | 3030 | proxies `/` → frontend, `/api/` → backend |

---

## Seeded Content (v0.2.0)

| City | University | POIs | Narrations |
|------|-----------|------|-----------|
| Princeton, NJ | Princeton University | 7 | 21 |
| Ann Arbor, MI | University of Michigan | 8 | 24 |
| College Station, TX | Texas A&M University | 8 | 24 |

All POIs have 3-tier narrations (snapshot/guide/deepdive). Seed is idempotent — safe to restart.

---

## Design System

**Colors (CSS vars in `index.css`):**
```
--ink: #1C1812      (body text)
--navy: #1B2A4A     (headers, nav)
--gold: #B8860B     (accents, active states)
--gold-light: #F5E6C8
--stone: #F8F5F0    (background)
--sage: #5C7A5C     (success, GPS active)
```

**Fonts:**
- `Cormorant Garamond` — display titles, POI names
- `DM Sans` — all UI text, labels, body

**Mobile-first breakpoints:** 320px base → 768px tablet → 1024px desktop

---

## Known Gotchas

### asyncpg + PostgreSQL arrays
Always pass Python lists for `TEXT[]` columns:
```python
# CORRECT
"categories": ["History", "Architecture"]

# WRONG — asyncpg will throw "sized iterable expected (got type 'str')"
"categories": "{History,Architecture}"
```

### Seed early-return bug (fixed in v0.2.0)
`seed_database()` originally returned early when Princeton existed, skipping UMICH/TAMU.
Pattern: each city now has its own `async with AsyncSessionLocal()` block with independent
`if slug not found → insert else skip` logic. Never use a single early `return` in seed.

### Service worker cache busting
After any frontend change: bump `CACHE_NAME` in `public/sw.js`:
```js
const SHELL_CACHE = 'audio-tour-v2'   // increment this
const API_CACHE   = 'audio-tour-api-v2'
```
Then hard-reload in browser (Cmd+Shift+R) + clear site data on iOS Safari.

### Docker node_modules volume
`frontend/node_modules` is an anonymous Docker volume. Do NOT volume-mount it from host.
If you get module-not-found errors: `docker compose down -v && docker compose up --build`.

### Tours API city_slug filter
`GET /tours?city_slug=ann-arbor` currently returns ALL tours (filter not wired in backend).
Frontend uses `city_id` from the city object to filter client-side. Fix this in Phase 2.

### Puter.js TTS
Loaded dynamically via `<script>` tag in `useTTS.ts`. Free, no API key needed.
Falls through to `window.speechSynthesis` if Puter fails. Audio is cached by text hash
in a `Map<string, string>` (object URLs) — avoids re-requesting on replay.

---

## Running Locally

```bash
cd /Users/sathiyankutty/Documents/claude-code/ai-audio-campus-tour-platform

# Start all services
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# TypeScript check
docker exec audio-tour-frontend npx tsc --noEmit

# Verify seed
curl http://localhost:8001/cities | python3 -m json.tool
curl "http://localhost:8001/pois?tour_id=<id>" | python3 -c "import sys,json; p=json.load(sys.stdin); print(len(p), 'POIs')"

# Access app
open http://localhost:3030
```

---

## Phase Status

| Phase | Status | Version | Summary |
|-------|--------|---------|---------|
| 1A — Foundation | ✅ Done | v0.1.0 | Scaffold, tour player, Princeton seed, DepthSelector, TTS |
| 1B — GPS + Multi-city | ✅ Done | v0.2.0 | GPS hook, auto-advance, UMICH+TAMU seed, offline PWA |
| 2 — AI Chat + Engagement | 🔜 Next | v0.3.0 | AI guide chat, streak/Daily Discovery, chapter markers |
| 3 — Creator + Social | 📋 Planned | v0.4.0+ | Creator CMS, badges, cross-city collections |

---

## Workflow

Every task follows **A → B → C → D**:

**A. Plan** — state goal, list files, identify agents  
**B. Agent team** — parallel agents, non-overlapping files, self-contained prompts  
**C. Progress chart** — ━━━ format, always, updated per step  
**D. Commit+push** — update docs first, multi-line commit, semver tag, push --tags

No auto-commits. Only commit/push when explicitly asked.
