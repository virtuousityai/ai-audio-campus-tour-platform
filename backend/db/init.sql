CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS cities (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name         VARCHAR NOT NULL,
  slug         VARCHAR UNIQUE NOT NULL,
  university   VARCHAR NOT NULL,
  country      VARCHAR NOT NULL DEFAULT 'US',
  state        VARCHAR,
  lat          DECIMAL(9,6) NOT NULL,
  lng          DECIMAL(9,6) NOT NULL,
  description  TEXT,
  hero_image   TEXT,
  published    BOOLEAN DEFAULT TRUE,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tours (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  city_id          UUID REFERENCES cities(id) ON DELETE CASCADE,
  name             VARCHAR NOT NULL,
  slug             VARCHAR NOT NULL,
  tagline          TEXT,
  duration_minutes INT DEFAULT 60,
  distance_meters  INT DEFAULT 2000,
  stop_count       INT DEFAULT 0,
  categories       TEXT[] DEFAULT '{}',
  cover_image      TEXT,
  published        BOOLEAN DEFAULT TRUE,
  created_at       TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(city_id, slug)
);

CREATE TABLE IF NOT EXISTS pois (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tour_id         UUID REFERENCES tours(id) ON DELETE CASCADE,
  position        INT NOT NULL,
  name            VARCHAR NOT NULL,
  tagline         TEXT,
  lat             DECIMAL(9,6) NOT NULL,
  lng             DECIMAL(9,6) NOT NULL,
  gps_radius_m    INT DEFAULT 30,
  walk_note       TEXT,
  categories      TEXT[] DEFAULT '{}',
  photo_url       TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tour_id, position)
);

CREATE TABLE IF NOT EXISTS narrations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  poi_id          UUID REFERENCES pois(id) ON DELETE CASCADE,
  depth_tier      VARCHAR NOT NULL CHECK (depth_tier IN ('snapshot','guide','deepdive')),
  script          TEXT NOT NULL,
  duration_sec    INT,
  audio_url       TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(poi_id, depth_tier)
);

CREATE TABLE IF NOT EXISTS users (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email                VARCHAR UNIQUE,
  name                 VARCHAR,
  tier                 VARCHAR DEFAULT 'free' CHECK (tier IN ('free','explorer','local')),
  preferred_depth      VARCHAR DEFAULT 'guide',
  preferred_categories TEXT[] DEFAULT '{}',
  preferred_duration   INT DEFAULT 60,
  xp                   INT DEFAULT 0,
  streak_current       INT DEFAULT 0,
  streak_longest       INT DEFAULT 0,
  last_active_date     DATE,
  created_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tour_sessions (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id            UUID REFERENCES users(id) ON DELETE CASCADE,
  tour_id            UUID REFERENCES tours(id),
  depth_tier         VARCHAR DEFAULT 'guide',
  current_poi_id     UUID REFERENCES pois(id),
  pois_completed     UUID[] DEFAULT '{}',
  started_at         TIMESTAMPTZ DEFAULT NOW(),
  last_active_at     TIMESTAMPTZ DEFAULT NOW(),
  completed_at       TIMESTAMPTZ,
  resume_position_sec INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_tours_city_id ON tours(city_id);
CREATE INDEX IF NOT EXISTS idx_pois_tour_id ON pois(tour_id);
CREATE INDEX IF NOT EXISTS idx_narrations_poi_id ON narrations(poi_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON tour_sessions(user_id);
