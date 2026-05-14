# Personalization System Design
## AI Audio Tour Platform
*Updated: 2026-05-13 | Based on full competitive analysis*

---

## 🧠 Core Insight from Research

> **Zero apps offer depth-of-learning selection. This is the single clearest white space in the entire category.**

Every competitor (VoiceMap, Rick Steves, GPSmyCity, Action Tour Guide, izi.TRAVEL) delivers one fixed narration length per stop. The Blinkist pattern (summary vs. full vs. extended) — standard in every audiobook and education app — has never been applied to walking tours.

---

## 🎚️ Depth Tiers: The "Tuning Fork" System

### 3-Level Model per POI

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  SNAPSHOT        GUIDE           DEEP DIVE               │
│  ─────────       ────────        ─────────               │
│  60–90 sec       3–4 min         8–12 min                │
│                                                          │
│  "What is it"    "The story"     "The expert layer"      │
│                                                          │
│  Perfect for:    Perfect for:    Perfect for:            │
│  rushed visitor  most visitors   enthusiast / student    │
│  passing by      touring         researching             │
│                                                          │
│  FREE            FREE            PREMIUM                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### What each tier contains

| Layer | Snapshot | Guide | Deep Dive |
|-------|---------|-------|-----------|
| Essential fact | ✅ | ✅ | ✅ |
| Story narrative | ❌ | ✅ | ✅ |
| Historical context | ❌ | ✅ | ✅ |
| Architectural/artistic detail | ❌ | ❌ | ✅ |
| Insider detail / hidden stories | ❌ | ❌ | ✅ |
| Connected facts (what happened here next?) | ❌ | ❌ | ✅ |
| Recommended reading / further exploration | ❌ | ❌ | ✅ |

### Where the depth selector lives

```
[Tour Stop Screen]
───────────────────────────────────────────────────────────
  Nassau Hall, Princeton University

  [SNAPSHOT]  [GUIDE ✓]  [DEEP DIVE]   ← depth pills
  
  ┌─────────────────────────────────────┐
  │  ▶  ∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙        │  3:42 remaining
  └─────────────────────────────────────┘
  
  "Still curious?" → [Ask your guide...]   ← AI chat
───────────────────────────────────────────────────────────
```

---

## 🏷️ Content Category System

### Primary Categories (always show 3–4 relevant per POI)

```
🏛 History          📖 Stories & Myths      🏗 Architecture
🍽 Food & Drink     🎨 Art & Culture         🌿 Nature & Parks
👻 Mysteries        💡 Science & Innovation  🎭 Entertainment
👥 People & Lives   🕊 Social Movements      💰 Commerce & Trade
🔍 Hidden Gems      📸 Photo Spots           🚶 Locals Only
```

### How Categories Work

**1. Pre-Tour Personalization (Smartify Pattern)**
```
┌─────────────────────────────────────────────────────┐
│  Before you start...                                 │
│                                                      │
│  What matters most to you today?                     │
│  (tap up to 3)                                       │
│                                                      │
│  [🏛 History]  [🍽 Food]   [🏗 Architecture]         │
│  [👻 Mysteries] [🎨 Art]   [💡 Science]              │
│  [🌿 Nature]   [📖 Stories] [👥 People]              │
│                                                      │
│  How much time do you have?                          │
│  [30 min]  [1 hour ✓]  [2+ hours]                   │
│                                                      │
│  Depth preference?                                   │
│  [Quick hits]  [Balanced ✓]  [Maximum detail]        │
│                                                      │
│  [Start your tour →]                                 │
└─────────────────────────────────────────────────────┘
```

**2. Per-Stop Category Badges**  
Each stop shows which categories it hits. User can tap a category to hear a "themed segment" within the narration.

```
Stop: Metropolitan Museum, NY
Categories: [🏛 History] [🎨 Art] [🏗 Architecture] [👥 People]

Default narration: art + history blend (Guide depth)
On tap [🏗 Architecture]: adds 90-sec architectural deep-note
On tap [👥 People]:        adds 90-sec "who built it, who visits" human story
```

**3. Category Filtering on Discovery**  
```
[Discover in New York City]
─────────────────────────────
Filter: [All] [History] [Food] [Architecture] [Mysteries]

Featured:  Greenwich Village Literary Walk   🏛📖  4.8★
Trending:  Lower East Side Food History     🍽🕊  4.9★
New:       Hidden Speakeasies of Manhattan  👻🍽  4.7★
```

---

## 🎯 Personalization Architecture

### 3-Layer Personalization

```
Layer 1: GLOBAL PROFILE (persists across sessions)
────────────────────────────────────────────────────────
  • Preferred depth tier (Snapshot / Guide / Deep Dive)
  • Preferred categories (top 3)
  • Preferred session length
  • Language
  • Accessibility preferences (closed captions on/off)

Layer 2: TRIP CONTEXT (per-tour / per-trip session)
────────────────────────────────────────────────────────
  • "I'm in a hurry" toggle (locks to Snapshot globally)
  • Group mode toggle (enables shared playback)
  • Override depth per stop

Layer 3: IN-STOP REAL-TIME (per-POI adaptation)
────────────────────────────────────────────────────────
  • User lingers >5 min at a stop → "Want to hear more?"
  • User skips in first 30s → log as "not interested in this category"
  • User asks AI question → log topic interest for recommendation engine
  • User replays a stop → flag as high-interest for creator analytics
```

### Preference Learning (Implicit Signals)

| Signal | What we infer |
|--------|---------------|
| Skips audio in first 30s | Too long → suggest shorter depth tier |
| Replays a stop | High interest → increase related content |
| Taps "Ask your guide" | Curious mode → surface more Deep Dive content |
| Selects Deep Dive > 3 stops | User is an enthusiast → default to Deep Dive |
| Completes 100% of tour | High-engagement visitor → pitch new tour immediately |
| Drops off at stop 3 of 10 | Tour too long → pitch shorter tours next session |

---

## 🔁 Engagement Loop Design

### The Full Retention Loop (Nothing Like This Exists Today)

```
DAY 0 — Onboarding
   3-question quiz → first personalized tour (free, Guide depth)
   
DAY 0 — First Tour
   GPS autoplay → Depth selector per stop → AI chat at 1 stop
   Completion screen → share card + "Explorer" badge
   
DAY 1 — Daily Discovery
   Push: "Your 5-minute story for today: The secret garden of the Cloisters..."
   Single POI story, podcast-mode (no GPS needed), Snapshot depth
   → Streak starts: 🔥 1 day

DAY 3 — Streak Mechanic
   "🔥 3-day streak. You've learned 3 stories about New York this week."
   Unlock: "Neighborhood Expert: Upper West Side" badge (3 stops completed)
   
WEEK 1 — Cross-Sell
   "You loved Architecture stories. Here are 4 tours across 3 cities."
   First cross-city collection: "Brutalist Giants: NYC, London, Berlin"
   → Deep Dive tier pitch (Premium)

WEEK 2 — Creator Follow
   "The guide who created your favorite tour just published in Rome."
   → Follow creator → get notified → pre-download for upcoming trip

MONTH 1 — Social
   "3 of your contacts completed the Brooklyn Bridge tour."
   → Compare notes → geo-stamped comment at Stop 5
```

---

## 📱 Podcast-Era UX (All Missing from Competitor Apps)

### Features Borrowed from Podcast Apps

| Feature | Why it matters | Where it lives |
|---------|---------------|----------------|
| **Playback speed** (0.75x, 1x, 1.25x, 1.5x) | Walkers move at different speeds; some want to absorb more slowly | Player controls |
| **Chapter markers** (one per stop) | Skip to Stop 4 without rewinding; resume exactly | Progress bar |
| **Download queue** (pre-trip planning) | "Download my 3 Rome tours before I fly" | Trip planner |
| **Auto-download on Wi-Fi** | Seamless offline prep | Settings |
| **Completion history** | "Tours I've done" page; brag rights; social comparison | Profile |
| **Resume from exact position** | Left at stop 6 last Tuesday; pick up exactly there | Auto-saved |
| **Cross-device sync** | Started on phone, finish on tablet | Account-linked |
| **Share a specific stop** | "Listen to this story about Nero at 2:14" | Stop overflow menu |

---

## 🃏 Gamification Layer

### Earning System

```
XP Triggers:
  Complete a stop        →  +10 XP
  Complete a tour        →  +50 XP
  Deep Dive stop         →  +25 XP bonus
  Ask AI guide a question →  +5 XP
  5-day streak            →  +100 XP bonus
  Rate a tour             →  +15 XP
  Share a tour            →  +20 XP

Levels:
  0–100    Wanderer
  100–500  Explorer
  500–2K   Local
  2K–10K   Insider
  10K+     Storyteller
```

### Badges (Collection Mechanic)

```
City Badges:         Complete 3 tours in a city → "NYC Explorer"
Category Badges:     5 history stops → "Time Traveler"
Streak Badges:       7-day streak → "Devoted Wanderer"
Deep Dive Badges:    10 Deep Dive stops → "The Enthusiast"
Country Badges:      Tours in 5 countries → "Global Citizen"
Creator Badges:      Tour rated 5 stars by 50 users → "Storyteller"
Hidden Badges:       Discover a "secret POI" (off main route) → "Urban Explorer"
```

### City Completion Map
```
[Your New York City]
───────────────────────────────────────────────────────
  ████ ████ ████ ████ ████ ████ ░░░░ ░░░░ ░░░░ ░░░░
  10 neighborhoods mapped     4 neighborhoods to go
  
  Completed: Greenwich Village ✅  Brooklyn Bridge ✅  
             Central Park ✅      Harlem ✅
  Next:      Lower East Side     The Bronx     Astoria
───────────────────────────────────────────────────────
```

---

## 🤖 AI Guide Chat: "Ask Your Guide"

### Design

```
[During stop narration, after audio completes]

  Nassau Hall, Princeton

  ┌────────────────────────────────────────────┐
  │ 💬 Ask your guide about this stop...       │
  └────────────────────────────────────────────┘

  Recent questions here:
  • "When was it built exactly?"        → answered
  • "What about the fire in 1802?"      → answered

  [Ask a new question...]
```

### AI Context Injected per Conversation

```python
system_prompt = f"""
You are a knowledgeable audio tour guide at {poi.name} in {city.name}.
The visitor has completed {user.stops_visited} stops and prefers {user.depth_tier} depth.
Their interests include: {", ".join(user.categories)}.
They are currently hearing the "{current_depth_tier}" version of this stop.

Stay in character as a local expert. Be conversational, not encyclopedic.
If they ask something outside this location, gently redirect.
Limit answers to 3–4 sentences unless they explicitly ask for more.

POI context:
{poi.full_context_blob}
"""
```

### What users ask (design for these)
- "Who built this?"
- "What happened here exactly?"
- "Any hidden stories about this place?"
- "What's the best photo angle?"
- "Why should I care about this?"
- "What's nearby that I shouldn't miss?"
- "What's this building's style called?"

---

## 🌍 Multi-Country / Multi-City Structure

### Hierarchy
```
Platform
└── Country (United States)
    └── City (New York City)
        └── Neighborhood / Zone (Greenwich Village)
            └── Tour (The Literary Walk)
                └── POI (White Horse Tavern)
                    └── Narration (Snapshot | Guide | Deep Dive)
                    └── Categories [History, Food, People]
                    └── AI Context Blob
```

### Discovery UX
```
Home Screen
────────────────────────────────────────────────────────
  [🌍 Browse by country]  [🏙 Browse by city]  [🔥 Trending]
  
  Based on your interests (🏛 History, 🏗 Architecture):
  ┌──────────────────┐  ┌──────────────────┐
  │  Rome: Ancient   │  │  Paris: Haussmann │
  │  Quarter Walk    │  │  Architecture     │
  │  ★ 4.9  1h 20m  │  │  ★ 4.8  45 min   │
  └──────────────────┘  └──────────────────┘
  
  Continuing your trip to Tokyo →
  [Pre-download 3 saved tours]  [Build a new tour]
────────────────────────────────────────────────────────
```

---

## 💰 Freemium Tier Design

### Tier Model

| Feature | Free | Explorer ($4.99/mo) | Local ($9.99/mo) |
|---------|------|---------------------|-----------------|
| Tours available | 3/month | Unlimited | Unlimited |
| Depth tiers | Snapshot + Guide | All 3 | All 3 |
| AI Guide chat | 3 questions/tour | 10 questions/tour | Unlimited |
| Offline downloads | 1 tour | 5 tours | Unlimited |
| Cities | 1 | All | All |
| Playback speed | 1x only | Full control | Full control |
| Daily Discovery | ✅ | ✅ | ✅ |
| Ad-free | ❌ | ✅ | ✅ |
| Early creator tours | ❌ | ❌ | ✅ |
| Revenue share (creators) | ❌ | ❌ | 30% of plays |

### Freemium Upgrade Triggers (nudge moments)

1. User selects "Deep Dive" → "Unlock all depth levels →"
2. User exceeds 3 AI chat questions → "Keep the conversation going →"
3. User tries to download second tour → "Download unlimited tours →"
4. 5-day streak → "Keep your streak with unlimited daily discovery →"
5. Post-tour completion → "You've explored 3 of 5 tours in your city. Go unlimited →"

---

## 🗂 Content Creation: Depth-Layered Narration Generation

### Claude Prompt Structure (per POI per depth tier)

```python
SNAPSHOT_PROMPT = """
Write a 60-second audio narration for {poi.name} in {city.name}.
Requirements:
- Single essential fact or surprising hook
- Conversational, not encyclopedic
- End with a natural pause cue
- No more than 90 words
Categories to touch: {poi.selected_categories}
"""

GUIDE_PROMPT = """
Write a 3–4 minute audio narration for {poi.name} in {city.name}.
Requirements:
- Open with the Snapshot hook (reuse from tier 1)
- Develop into the narrative: who, what, when, why it matters
- Include 1 sensory detail (what it looked/smelled/sounded like)
- End with a transition to the next stop
- 400–500 words
Categories to prioritize: {", ".join(poi.selected_categories)}
"""

DEEP_DIVE_PROMPT = """
Write an 8–12 minute audio narration for {poi.name} in {city.name}.
Requirements:
- Open with the Guide narration (reuse from tier 2)
- Extend with: expert context, architectural/artistic/historical analysis
- Include at least 1 hidden or surprising fact
- Include at least 1 related story (person, event, or object)
- Suggest 1 thing to look for that most visitors miss
- End with a recommended next step (further reading, adjacent POI)
- 1,000–1,200 words
Categories to emphasize: {", ".join(poi.selected_categories)}
Expert angle for this POI: {poi.expert_angle}  # curator-set field
"""
```

### Audio Generation Pipeline

```
Creator writes POI prompt
        ↓
Claude generates 3-tier narration text
        ↓
Text → TTS (Claude TTS or ElevenLabs voice clone)
        ↓
MP3 stored in S3 (3 files per POI: snapshot.mp3, guide.mp3, deepdive.mp3)
        ↓
CDN distribution + pre-signed URLs for offline download
        ↓
Creator can preview + re-generate any tier individually
```

---

## 🏆 Competitive Positioning

| Axis | Us | Best Competitor |
|------|-----|-----------------|
| Depth tiers | **First in market** | Nobody |
| Interest categories | Per-stop filtering | VoiceMap (discovery only) |
| AI guide chat | In-tour Q&A | TalkieWalkie (prototype) |
| Daily habit loop | Streak + Daily Discovery | Nobody |
| Podcast UX | Full (speed, chapters, queue) | Nobody |
| Group experience | Group mode (Phase 2) | Nobody (since Detour 2018) |
| Freemium clarity | 3 tiers, clear upgrade triggers | Split across competitors |
| Creator marketplace | Revenue share + tools | VoiceMap (best existing) |

---

## 📋 Prioritized Feature Roadmap (by impact)

### Must-Ship Phase 1
1. GPS autoplay with configurable radius
2. 3-tier depth selector (Snapshot / Guide / Deep Dive)  ← biggest differentiator
3. 3-question pre-tour onboarding (interests, time, depth)
4. Interest category badges per POI
5. Completion tracking (tours done, stops visited)
6. Resume from exact position
7. Offline download with progress indicator

### Phase 2 Priorities
8. AI Guide chat (3 questions free, unlimited premium)
9. Daily Discovery mode (5-min micro-session, no GPS needed)
10. Streak mechanic (daily exploring habit)
11. Playback speed control (0.75x – 2x)
12. Chapter markers in progress bar
13. City completion map / neighborhood progress

### Phase 3 Priorities
14. Badge / achievement system
15. Cross-city thematic collections
16. Creator follow + notifications
17. Social: geo-stamped notes, friend activity
18. Group mode (shared playback, group pricing)
19. Download queue (pre-trip planning)

---

*Sources: VoiceMap, izi.TRAVEL, Questo, Smartify, Rick Steves Audio, Action Tour Guide, TalkieWalkie, SmartGuide, Blinkist, Duolingo — analyzed May 2026*
