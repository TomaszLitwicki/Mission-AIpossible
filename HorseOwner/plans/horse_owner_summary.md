# Horse Owner – Podsumowanie pomysłu

## Cel projektu
Aplikacja webowa wspierająca jeźdzca w opiece nad koniem oraz planowaniu i analizie treningów. Projekt łączy pasję do koni z nauką programowania, a jego celem jest stworzenie realnie użytecznego narzędzia w codziennej pracy z koniem.

## Stack technologiczny
- **Backend:** Python + Flask
- **Frontend:** Jinja2 + HTML + CSS
- **Baza danych:** SQLite (możliwość przejścia na Supabase/PostgreSQL w przyszłości)
- **Hosting:** PythonAnywhere
- **AI:** OpenAI API (funkcje wspomagające, nie diagnostyczne)

## Główne moduły aplikacji

### 1. Konie (Horses)
- Dane: imię, rasa, płeć, wiek, numer mikroczipu, pochodzenie, maść, opis, zdjęcie.
- Funkcje: dodawanie, edycja, usuwanie, przegląd, upload zdjęcia.

### 2. Treningi (Trainings)
- Dane: data, typ (ujeżdżenie, skoki, teren), czas trwania, intensywność (RPE), notatki.
- Funkcje: CRUD + analiza postępów z AI.
- AI: analiza ostatnich treningów, propozycje kolejnych ćwiczeń.

### 3. Opieka (Care)
- Podsekcje: szczepienia, odrobaczenia, werkowanie, zęby.
- Dane: data, nazwa, notatki, termin kolejnej czynności.
- AI: generowanie planu profilaktyki rocznej.

### 4. Kontakty (Contacts)
- Weterynarz, kowal, fizjoterapeuta, transport.
- Dane: nazwa, telefon, region, notatki.

### 5. Moduł AI (Support)
- **Weterynaria (Vets):** generowanie listy pytań do rozmowy z lekarzem na podstawie objawów.
- **Żywienie (Feeding):** opis planu żywieniowego, propozycje sezonowe.
- **Opieka (Care plan):** automatyczny harmonogram profilaktyki.
- **SOS:** szybkie kroki w nagłych sytuacjach + kontakty awaryjne.
- **Analiza treningów (Training Analysis):** streszczenie postępów, pomysły na kolejne sesje.

## Architektura projektu (MVP)
```
/horse_owner
  app.py
  config.py
  /models.py
  /services/ai.py
  /forms/
  /templates/
    base.html
    horses/*.html
    trainings/*.html
    care/*.html
    contacts/*.html
    ai/*.html
  /static/
    css/, js/, uploads/
  requirements.txt
  README.md
  .env
```

## Baza danych (SQLite)
**Horse**: id, name, microchip, breed, sex, birth_date, color, origin, notes, photo_path  
**TrainingSession**: id, horse_id, date, type, duration, rpe, goal, notes  
**CareEvent**: id, horse_id, category, name, date, next_due, notes  
**Contact**: id, role, name, phone, area, notes  

## Plan MVP (Tydzień 4)
1. **Dzień 1:** szkic projektu, repozytorium, routing Flask, pierwsze widoki.
2. **Dzień 2:** CRUD dla Horses i Trainings.
3. **Dzień 3:** Care + Contacts + refaktoryzacja + wdrożenie.
4. **Dzień 4:** dodanie funkcji AI (analiza treningów).
5. **Dzień 5:** testy, poprawki, README + dokumentacja projektu.

## Pomysły na rozwój (po kursie)
- Logowanie użytkowników (Flask-Login / Supabase Auth)
- Wykresy statystyczne (Chart.js)
- Eksport danych do CSV lub PDF
- Przypomnienia mailowe / powiadomienia o terminach
- Przeniesienie bazy na Supabase i rozdzielenie front/back

## Uwagi
- AI nie daje diagnoz medycznych – tylko rekomendacje i wsparcie komunikacyjne.
- Dane użytkownika przechowywane lokalnie (SQLite) w wersji MVP.
- Prosty, czytelny interfejs (Dashboard, listy, karty, formularze).

---
**Autor:** Tomasz  
**Projekt:** Horse Owner  
**Cel:** stworzenie realnej aplikacji webowej łączącej pasję do koni z nauką programowania i wykorzystaniem AI.

