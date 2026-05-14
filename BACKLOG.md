# AI Audio Campus Tour Platform — Master Backlog
*Last updated: 2026-05-13*

---

## Overview

A self-serve, white-label AI audio guide platform for universities, corporate campuses,
museums, and real estate. Powered by Claude-generated narration with GPS-triggered
playback. Target customers are Directors of Visitor Experience at enterprise institutions.

**Pricing:** $1,500–$3,500/year (SaaS)
**Competitive gap:** Physical walking audio experience vs. 360 video platforms (YouVisit, Concept3D, StudentBridge)

---

## 📋 Feature Backlog

### AACP-1 — Core Audio Tour Platform (MVP)
**Priority:** HIGH — foundational product
**Size:** XL
**Description:** Self-serve platform where institutions can create and publish GPS-triggered
audio tours without engineering help.

**Key features:**
- Claude-generated narration per location point of interest (POI)
- GPS-triggered audio playback — audio auto-plays as visitor approaches a POI
- CMS for self-onboarding — institutions add/edit locations, upload photos, write POI prompts
- White-label branding — institution logo, colors, custom subdomain
- Mobile-first PWA (works on iOS and Android without app install)
- Visitor-facing tour player with map view and list view

**Technical requirements:**
- Geolocation API for GPS triggering (configurable radius per POI)
- Claude API integration for narration generation
- Audio file storage and streaming (generated MP3s per POI)
- CMS backend for institution admin portal
- Multi-tenant architecture — each institution has isolated data

---

### AACP-2 — Stripe Payments & Subscription Management
**Priority:** HIGH — required for monetization
**Size:** M
**Description:**
- Stripe integration for subscription billing ($1,500–$3,500/year tiers)
- Trial period (30 days) with self-serve onboarding
- Upgrade/downgrade plan management
- Usage-based limits per tier (number of POIs, number of audio minutes generated)
- Admin billing portal (Stripe Customer Portal)

---

### AACP-3 — Institution Self-Onboarding CMS
**Priority:** HIGH
**Size:** L
**Description:** No-code admin dashboard for institution staff to:
- Create and manage tour routes
- Add/edit/delete POIs (name, description, GPS coordinates, photos)
- Generate narration via Claude (one-click or custom prompt)
- Preview audio before publishing
- Publish / unpublish tours
- View visitor analytics (tour starts, POIs visited, completion rate)

---

### AACP-4 — Visitor Tour Player (Mobile PWA)
**Priority:** HIGH
**Size:** L
**Description:** Mobile-first experience for visitors walking the campus/museum:
- Map view showing all POIs with progress indicators
- Auto-play audio when entering GPS radius of a POI
- Manual mode — tap any POI to play its narration
- Offline-capable — cache narration audio for areas with poor signal
- Accessible controls (pause, replay, skip)
- Institution branding on player screen

---

### AACP-5 — Distribution & Go-to-Market Setup
**Priority:** HIGH
**Size:** M
**Description:** Inbound distribution channels:
- SEO-optimized landing page (targeting "campus audio tour", "museum audio guide" keywords)
- Admissions office outreach — direct sales to university admissions teams
- Alumni association partnerships — feature in alumni weekend events
- Demo tour (live example anyone can take to experience the product)

---

### AACP-6 — Consumer Version (Phase 2)
**Priority:** LOW — second phase after enterprise traction
**Size:** XL
**Description:** Consumer-facing version for cities and attractions:
- Public tours for city districts, parks, historic sites
- User-generated tour creation (anyone can build and publish a tour)
- Discovery feed — browse tours by location/category
- Rating and review system
- Freemium model with premium tour purchases

---

## 🧭 Recommended Build Order

```
1. AACP-1: Core GPS-triggered audio tour player (MVP) + demo institution
2. AACP-2: Stripe payments + subscription tiers
3. AACP-3: Institution self-onboarding CMS
4. AACP-4: Polish mobile PWA player (offline, branding, analytics)
5. AACP-5: Go-to-market — SEO + admissions outreach
6. AACP-6: Consumer version (post-enterprise validation)
```

---

## 🎯 Target Customer Profile

| Attribute | Detail |
|---|---|
| **Primary buyer** | Director of Visitor Experience |
| **Institutions** | Universities, corporate campuses, museums, real estate developers |
| **Price point** | $1,500–$3,500/year |
| **Competition** | YouVisit, Concept3D, StudentBridge (360 video-based, not audio-first) |
| **Key differentiator** | Physical walking audio experience; Claude AI narration; GPS-triggered |

---

*Source: Project Backlog item from Reminders — 2026-05-13*
