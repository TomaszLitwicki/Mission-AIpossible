# 🐴 Horse Owner

Aplikacja webowa wspierająca jeźdźca w opiece nad końmi oraz planowaniu i analizie treningów.\
Projekt łączy pasję do koni z nauką programowania i wykorzystaniem sztucznej inteligencji (AI) w praktyce.

---

## 🎯 Cel projektu

Celem jest stworzenie prostego i funkcjonalnego narzędzia, które pozwoli właścicielowi koni:

- prowadzić historię treningów i opieki,
- przechowywać ważne kontakty w jednym miejscu,
- analizować postępy za pomocą AI,
- planować profilaktykę zdrowotną i harmonogramy opieki.

---

## 🧩 Stack technologiczny

**Backend:** Python + Flask\
**Frontend:** Jinja2 + HTML + CSS\
**Baza danych:** SQLite\
**Hosting:** PythonAnywhere\
**AI:** OpenAI API (wsparcie analityczne, nie diagnostyczne)

---

## 📱 Moduły aplikacji

| Moduł                    | Opis                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------- |
| **Konie (Horses)**       | Dane koni (imię, rasa, wiek, chip, maść, opis). CRUD + zdjęcie.                     |
| **Treningi (Trainings)** | Data, typ, czas, RPE, notatki. Analiza AI i rekomendacje.                           |
| **Opieka (Care)**        | Szczepienia, werkowanie, zęby, odrobaczenia, przypomnienia.                         |
| **Kontakty (Contacts)**  | Weterynarz, kowal, fizjoterapeuta, transport.                                       |
| **AI Asystent**          | Wsparcie w analizie treningów, planowaniu opieki i reagowaniu w sytuacjach nagłych. |

---

## 🗃️ Baza danych (SQLite)

Struktura relacji:

```
users 1 ──< horses 1 ──< training_sessions
   │           └────< care_events
   └────────< contacts
```

---

## 🦯 Nawigacja

- **Dashboard:** przegląd koni, ostatnich treningów i nadchodzących zabiegów.
- **Konie:** lista, profil, zakładki (Treningi / Opieka / Notatki).
- **Treningi:** filtrowanie, dodawanie, analiza AI.
- **Opieka:** kalendarz, statusy, plan AI.
- **Kontakty:** lista z numerami i rolami.
- **AI Asystent:** tekstowy formularz zapytań do modelu AI.
- **Konto:** profil, ustawienia, wylogowanie.

---

## 🎨 UI / Design

Kolory inspirowane naturą stajni:

- Stable Green `#5E7B5B`
- Hay Beige `#E9DFC8`
- Saddle Brown `#6B4E3D`
- Fence Light `#F7F7F7`

Czcionki: *Merriweather* (nagłówki) + *Roboto* (tekst)\
Interfejs responsywny, dostępny na desktop i mobile.

---

## 🚀 Plan MVP

1. Routing Flask + Dashboard
2. CRUD dla Horses i Trainings
3. Moduły Care i Contacts
4. Wdrożenie AI (analiza treningów)
5. Testy, README i wdrożenie na PythonAnywhere

---

## 🔧 Jak uruchomić projekt lokalnie

1. **Sklonuj repozytorium**

   ```bash
   git clone https://github.com/twoj-login/horse_owner.git
   cd horse_owner
   ```

2. **Utwórz i aktywuj wirtualne środowisko**

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   source .venv/bin/activate   # Linux / macOS
   ```

3. **Zainstaluj zależności**

   ```bash
   pip install -r requirements.txt
   ```

4. **Zainicjalizuj bazę danych**

   ```bash
   flask --app app init-db
   ```

5. **Uruchom aplikację**

   ```bash
   flask --app app run --debug
   ```

   Następnie otwórz w przeglądarce: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔮 Kierunki rozwoju

- Logowanie użytkowników (Flask-Login / Supabase Auth)
- Wykresy (Chart.js)
- Eksport danych do CSV / PDF
- Przypomnienia o terminach
- Migracja bazy do Supabase (PostgreSQL)

---

**Autor:** Tomasz\
**Repozytorium:** [Horse Owner](https://github.com/)\
**Cel:** stworzenie realnej aplikacji webowej łączącej pasję do koni z nauką programowania i sztucznej inteligencji.

---

