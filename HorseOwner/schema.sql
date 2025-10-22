-- =========================================
-- HORSES: lista koni
-- =========================================
DROP TABLE IF EXISTS horses;
CREATE TABLE horses (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  breed TEXT,
  sex TEXT CHECK(sex IN ('mare','stallion','gelding')),
  birth_date TEXT,
  color TEXT,
  origin TEXT,
  notes TEXT
);
-- =========================================
-- TRAININGS: sesje treningowe koni
-- =========================================
DROP TABLE IF EXISTS trainings;
CREATE TABLE trainings (
  id INTEGER PRIMARY KEY,
  horse_id INTEGER NOT NULL REFERENCES horses(id) ON DELETE CASCADE,
  date TEXT NOT NULL,              -- YYYY-MM-DD
  time TEXT,                       -- HH:MM (lokalnie)
  duration_min INTEGER NOT NULL,   -- czas trwania w minutach
  type TEXT NOT NULL CHECK(type IN ('dressage','jumping','trail','groundwork','other')),
  score INTEGER CHECK(score BETWEEN 1 AND 10),   -- wynik/efekty 1-10
  satisfied INTEGER NOT NULL CHECK(satisfied IN (0,1)), -- 1=TAK, 0=NIE
  notes TEXT
);
CREATE INDEX idx_trainings_date ON trainings(date);
CREATE INDEX idx_trainings_horse_date ON trainings(horse_id, date);

-- =========================================
-- TREATMENTS: zabiegi (opieka)
-- =========================================
CREATE TABLE IF NOT EXISTS treatments (
  id INTEGER PRIMARY KEY,
  horse_id INTEGER NOT NULL REFERENCES horses(id) ON DELETE CASCADE,
  name TEXT NOT NULL,                 -- np. "Szczepienie", "Werkowanie", "Odrobaczenie"
  date TEXT NOT NULL,                 -- YYYY-MM-DD
  status INTEGER NOT NULL CHECK(status IN (0,1)) DEFAULT 0,  -- 0=NIE (plan), 1=TAK (wykonano)
  notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_treatments_horse_date ON treatments(horse_id, date);
CREATE INDEX IF NOT EXISTS idx_treatments_status_date ON treatments(status, date);
