# Horse Owner 

---

# 🎨 UI – to, co zobaczy użytkownik (Style & Screens)

## Paleta kolorów (Color palette)

- **Stable Green** `#5E7B5B` – akcent / przyciski „primary”
- **Hay Beige** `#E9DFC8` – tła sekcji, delikatne wyróżnienia
- **Saddle Brown** `#6B4E3D` – nagłówki, linki w stanie hover
- **Field Gray** `#5A5F63` – podstawowy tekst
- **Fence Light** `#F7F7F7` – główne tło strony
- **Alert Red** `#C0392B` – stany krytyczne (SOS, po terminie)
- **Soon Yellow** `#F1C40F` – „nadchodzi”
- **Okay Green** `#27AE60` – „w porządku”

> Kontrast kolorów sprawdzony tak, by tekst na tle był czytelny (AA). Dla przycisków „primary” stosujemy białą czcionkę.

## Typografia (Typography)

- **Nagłówki:** "Merriweather" (serif), waga 600
- **Tekst:** "Roboto" (sans-serif), waga 400/500
- **Rozmiary bazowe:**
  - H1: 28–32px, H2: 22–24px, H3: 18–20px
  - Body: 16px, Small: 14px
- **Interlinia:** 1.5 dla treści akapitowych

## Siatka i spacing (Layout & Spacing)

- **Container max-width:** 1100px
- **Gutter:** 16px, **Section padding:** 24–32px
- **Karty (cards):** radius 14–16px, delikatny cień, tło `#FFFFFF`

## Ikony

- Zestaw: **Lucide** lub **Font Awesome**
- Przykłady: 🐴 (horse), 🏋️ (training), 💉 (care), 📞 (phone), 🧭 (dashboard)

---

## Komponenty UI (Component Kit)

### 1) Navbar (global)

- Logo „Horse Owner” po lewej, po prawej menu: **Konie | Treningi | Opieka | Kontakty | AI Asystent | Konto**
- Tło: `#FFFFFF`, cienka dolna ramka (`#E5E7EB`)
- Aktywna zakładka: kolor **Stable Green**, podkreślenie 2px

### 2) Przycisk (Button)

- Primary: tło **Stable Green**, tekst #FFF, hover → ciemniejszy odcień
- Secondary: obrys **Stable Green** na białym tle
- Danger: tło **Alert Red** (np. „Usuń”)

### 3) Karta (Card)

- Nagłówek H3, treść, przyciski akcji po prawej (ikonowe)
- Użycie: koń (mini-profil), wpis opieki, kontakt, skrót AI

### 4) Tabele / listy

- Wiersze zebra (`#FAFAFA`), nagłówek bold, kolumna akcji (ikony ✏️ 🗑️)
- W mobile tabela zmienia się w listę z etykietami

### 5) Pills / Statusy

- **🟢 OK** (Okay Green), **🟡 Soon** (F1C40F), **🔴 Late** (C0392B)
- Małe kapsułki z krótkim tekstem („w terminie”, „nadchodzi”, „po terminie”)

### 6) Formularze (Forms)

- Label nad polem, pola z radius 8px, obrys `#CBD5E1`
- Błędy: czerwony tekst + delikatne tło `#FDEDEC`
- Hinty: tekst w kolorze **Field Gray** 14px

---

## Ekrany (Screens)

### A) Dashboard

**Cel:** szybki przegląd koni, ostatnich treningów i nadchodzącej opieki + skrót do AI.

**Układ:**

1. Pasek powitalny: „Dzień dobry, Tomasz”
2. **Twoje konie** – 2–4 karty z miniaturami, przycisk „Zobacz wszystkie”
3. **Ostatnie treningi** – tabela 5 wierszy + „Dodaj trening” + „Analiza tygodnia (AI)”
4. **Nadchodzące zabiegi** – lista 3–4 pozycji ze statusem pill
5. **Szybki AI** – małe pole tekstowe + przycisk „Zapytaj”

**Microcopy:**

- „Brak koni? Dodaj pierwszego konia, aby zacząć.”
- „Nic w kalendarzu opieki na 14 dni.”

### B) Konie – lista

- Grid kart: zdjęcie, imię, rasa, wiek, przyciski: Profil, Treningi, Opieka
- Fab button „+ Dodaj konia” (prawy-dolny róg na mobile)

### C) Profil konia

- Header z imieniem i mini zdjęciem; przyciski: „Edytuj”, „Dodaj trening”, „Dodaj opiekę”
- Zakładki: **Treningi | Opieka | Notatki**
- Sekcja **AI**: „Analiza ostatnich 7 dni” (wynik jako lista punktów)

### D) Treningi – lista

- Filtry górne: [Konia ▼] [Data od… do…]
- Tabela: Data | Typ | Czas | RPE | Notatki | (ikony akcji)
- CTA: „Dodaj nowy trening” (primary) + „Analizuj z AI” (secondary)

### E) Opieka – kalendarz

- Tabela/lista wg daty; kolumna **Status (pill)**
- CTA: „Dodaj wpis” + „Generuj plan AI”

### F) Kontakty – lista

- Karty z ikoną roli (vet/farrier/physio/transport), nazwą i telefonem (link tel:)
- Akcje: edytuj / usuń

### G) AI Asystent

- Select: **Trening / Opieka / Żywienie / SOS**
- Textarea: „Opisz problem lub pytanie…”
- Wynik: ramka z nagłówkiem „Odpowiedź AI”, w treści listy punktów, ewentualnie ostrzeżenia (czerwony box)
- Stopka: **Disclaimer** (to nie porada medyczna)

### H) Logowanie / Rejestracja

- Środkowy panel na jasnym tle, logo 🐎
- Form: e-mail, hasło, checkbox „Zapamiętaj mnie”
- Link: „Nie masz konta? Zarejestruj się”

---

## Responsywność (Responsive)

- **Breakpointy:** 768px / 1024px
- Desktop: 2–3 kolumny kart; Mobile: 1 kolumna, stały bottom-bar (ikony: Konie, Treningi, Opieka, AI, Konto)
- Tabele → listy kartowe na mobile (etykieta + wartość)

---

## Dostępność (Accessibility)

- Kontrasty WCAG AA (tekst do tła ≥ 4.5:1)
- Focus states: wyraźne obramowanie przy tab-navigation
- Etykiety `aria-label` dla ikon (np. „Edytuj trening”)
- Formularze: połączone `label for` + `id`

---

## Teksty (copy) – spójnik językowy

- Przyciski: „Dodaj”, „Zapisz”, „Anuluj”, „Edytuj”, „Usuń”, „Analizuj z AI”
- Stany pustki (empty states): z krótkim wyjaśnieniem i CTA
- Wiadomości błędów: jednozdaniowe, konkretne; bez ujawniania wrażliwych danych

---

## Następny krok

- Na bazie tej specyfikacji możemy przygotować **szablony Jinja2**: `base.html`, `dashboard.html`, `horses/list.html`, `horses/detail.html`, `trainings/list.html`, `care/list.html`, `contacts/list.html`, `ai/assistant.html`, `auth/login.html`, `auth/register.html` – z minimalnym CSS (Bootstrap 5) i klasami pomocniczymi.

