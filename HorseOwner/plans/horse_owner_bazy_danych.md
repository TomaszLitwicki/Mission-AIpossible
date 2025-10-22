# Horse Owner 

---

# 🗃️ Schemat bazy danych (ERD) – SQLite

## Tabele i pola (PL / EN, typ, uwagi)

### 1) `users`

- `id` – INTEGER PK
- `email` – TEXT UNIQUE **(login / unique)**
- `password_hash` – TEXT **(hash, nigdy nie trzymamy hasła wprost)**
- `name` – TEXT (display name)
- `role` – TEXT CHECK(role IN ('owner','admin')) DEFAULT 'owner'
- `created_at` – TEXT (ISO datetime)

**Indeksy:** `idx_users_email`

---

### 2) `horses`

- `id` – INTEGER PK
- `user_id` – INTEGER FK → `users.id`
- `name` – TEXT
- `breed` – TEXT
- `sex` – TEXT CHECK(sex IN ('mare','stallion','gelding'))  *(klacz/ogier/wałach)*
- `birth_date` – TEXT (YYYY-MM-DD) lub `age_years` – INTEGER *(wybierz jeden wariant w MVP)*
- `microchip` – TEXT  *(numer transpondera; opcjonalnie)*
- `color` – TEXT *(maść)*
- `origin` – TEXT *(pochodzenie)*
- `notes` – TEXT
- `photo_path` – TEXT *(ścieżka do pliku w /static/uploads)*

**Kontrainty:** `UNIQUE(user_id, name)` *(unikalna nazwa konia w obrębie konta)*\
**Indeksy:** `idx_horses_user_id`, `idx_horses_microchip` *(opcjonalnie UNIQUE(user\_id, microchip) jeśli chcesz wymuszać)*

---

### 3) `training_sessions`

- `id` – INTEGER PK
- `user_id` – INTEGER FK → `users.id`
- `horse_id` – INTEGER FK → `horses.id`
- `date` – TEXT (YYYY-MM-DD)
- `type` – TEXT CHECK(type IN ('dressage','jumping','trail','groundwork','other'))
- `duration_min` – INTEGER *(czas w minutach)*
- `rpe` – INTEGER CHECK(rpe BETWEEN 1 AND 10) *(subiektywna intensywność)*
- `goal` – TEXT *(cel sesji)*
- `notes` – TEXT *(opis przebiegu)*

**Indeksy:** `idx_training_user_date (user_id, date)`, `idx_training_horse_date (horse_id, date)`

> *Rozszerzenie później:* tabela `training_tags` + `training_session_tags` (M\:N) jeśli zechcesz tagować sesje.

---

### 4) `care_events`

- `id` – INTEGER PK
- `user_id` – INTEGER FK → `users.id`
- `horse_id` – INTEGER FK → `horses.id`
- `category` – TEXT CHECK(category IN ('vaccination','deworming','hoof','teeth','other'))
- `name` – TEXT *(np. „Flu/Tetanus”, „Ivermectin”, „Werkowanie”)*
- `date` – TEXT (YYYY-MM-DD)
- `next_due` – TEXT (YYYY-MM-DD) *(termin kolejny; NULL jeśli brak)*
- `notes` – TEXT

**Indeksy:** `idx_care_user_date (user_id, date)`, `idx_care_horse_category (horse_id, category)`

---

### 5) `contacts`

- `id` – INTEGER PK
- `user_id` – INTEGER FK → `users.id`
- `role` – TEXT CHECK(role IN ('vet','farrier','physio','transport','other'))
- `name` – TEXT
- `phone` – TEXT
- `area` – TEXT *(obszar, region)*
- `notes` – TEXT

**Kontrainty:** `UNIQUE(user_id, role, name)` *(ten sam kontakt roli nie powtarza się dla użytkownika)*\
**Indeksy:** `idx_contacts_user_role (user_id, role)`

---

## Relacje (ERD ASCII)

```
 users 1 ──< horses 1 ──< training_sessions
    │            └──────< care_events
    └─────────────< contacts
```

Legenda: `A 1 ──< B` oznacza relację **jeden-do-wielu** (1\:N), gdzie `B` zawiera klucz obcy do `A`.

- Każdy rekord ma `user_id` → prywatność i filtrowanie po zalogowaniu.
- `horses` wiąże się z `training_sessions` i `care_events`.
- `contacts` należy do użytkownika, ale nie do konkretnego konia (prościej w MVP).

---

## Minimalne DDL (SQLite) – do migracji ręcznej

> *Cel: szkic – możesz wkleić do narzędzia migracji lub odpalić jednokrotnie przy starcie.*

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  name TEXT,
  role TEXT NOT NULL DEFAULT 'owner' CHECK(role IN ('owner','admin')),
  created_at TEXT
);

CREATE TABLE horses (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  breed TEXT,
  sex TEXT CHECK(sex IN ('mare','stallion','gelding')),
  birth_date TEXT,
  microchip TEXT,
  color TEXT,
  origin TEXT,
  notes TEXT,
  photo_path TEXT,
  UNIQUE(user_id, name)
);
CREATE INDEX idx_horses_user ON horses(user_id);

CREATE TABLE training_sessions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  horse_id INTEGER NOT NULL REFERENCES horses(id) ON DELETE CASCADE,
  date TEXT NOT NULL,
  type TEXT CHECK(type IN ('dressage','jumping','trail','groundwork','other')),
  duration_min INTEGER,
  rpe INTEGER CHECK(rpe BETWEEN 1 AND 10),
  goal TEXT,
  notes TEXT
);
CREATE INDEX idx_training_user_date ON training_sessions(user_id, date);
CREATE INDEX idx_training_horse_date ON training_sessions(horse_id, date);

CREATE TABLE care_events (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  horse_id INTEGER NOT NULL REFERENCES horses(id) ON DELETE CASCADE,
  category TEXT CHECK(category IN ('vaccination','deworming','hoof','teeth','other')),
  name TEXT,
  date TEXT NOT NULL,
  next_due TEXT,
  notes TEXT
);
CREATE INDEX idx_care_user_date ON care_events(user_id, date);
CREATE INDEX idx_care_horse_category ON care_events(horse_id, category);

CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role TEXT CHECK(role IN ('vet','farrier','physio','transport','other')),
  name TEXT NOT NULL,
  phone TEXT,
  area TEXT,
  notes TEXT,
  UNIQUE(user_id, role, name)
);
CREATE INDEX idx_contacts_user_role ON contacts(user_id, role);
```

---

## Zasady integralności i bezpieczeństwo

- **Wszystkie zapytania** muszą filtrować po `user_id = current_user.id`.
- **ON DELETE CASCADE** – usunięcie użytkownika/konia usuwa powiązane wpisy (uważaj w panelach admina).
- **Walidacja formularzy**: daty w formacie `YYYY-MM-DD`, max długości pól tekstowych, numer telefonu w `contacts`.
- **Import/Export**: przewidziany prosty eksport CSV dla `training_sessions` i `care_events`.

---

## Rozszerzenia „po MVP” (opcjonalne)

- `training_tags` (M\:N), `photos` (wiele zdjęć na konia), `events` (wizyty, kontuzje), `reminders` (przypomnienia e-mail/SMS), `shared_access` (współdzielenie konia z trenerem).
- Migracja do **Postgres (Supabase)** – wszystkie typy zgodne, CHECK zamienisz na `ENUM` lub pozostawisz `TEXT` z CHECK.

