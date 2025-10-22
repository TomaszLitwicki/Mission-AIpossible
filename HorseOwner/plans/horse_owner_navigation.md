# Horse Owner – Schemat nawigacji aplikacji

## 🔁 Przepływ użytkownika (User Flow)

### 1. Użytkownik niezalogowany

```
[Strona logowania / rejestracji]
       │
       ▼
 [Zaloguj się / Utwórz konto]
       │  (jeśli dane poprawne)
       ▼
 [Dashboard]
```

### 2. Użytkownik zalogowany – główny przepływ

```
[Dashboard]
   │
   ├──▶ [Konie] ─▶ [Profil konia]
   │                 ├──▶ [Treningi konia]
   │                 │       ├──▶ [Dodaj trening]
   │                 │       ├──▶ [Analiza AI]
   │                 │       └──▶ [Powrót do profilu]
   │                 ├──▶ [Opieka konia]
   │                 │       ├──▶ [Dodaj wpis opieki]
   │                 │       ├──▶ [Plan AI]
   │                 │       └──▶ [Powrót do profilu]
   │                 └──▶ [Notatki konia]
   │
   ├──▶ [Treningi] ─▶ [Lista wszystkich treningów]
   │                 ├──▶ [Filtruj po koniu]
   │                 ├──▶ [Dodaj nowy trening]
   │                 └──▶ [Analizuj treningi AI]
   │
   ├──▶ [Opieka] ─▶ [Kalendarz opieki]
   │                ├──▶ [Dodaj nowy wpis]
   │                ├──▶ [Generuj plan AI]
   │                └──▶ [Edycja wpisu]
   │
   ├──▶ [Kontakty] ─▶ [Lista kontaktów]
   │                 ├──▶ [Dodaj kontakt]
   │                 ├──▶ [Edytuj kontakt]
   │                 └──▶ [Zadzwoń / Usuń]
   │
   ├──▶ [AI Asystent] ─▶ [Formularz AI]
   │                     ├──▶ [Temat: trening / opieka / żywienie / SOS]
   │                     ├──▶ [Wysłanie zapytania]
   │                     └──▶ [Wyświetlenie odpowiedzi]
   │
   └──▶ [Konto ▼]
          ├──▶ [Mój profil]
          ├──▶ [Ustawienia]
          └──▶ [Wyloguj się → Strona logowania]
```

## 🧭 Logika nawigacji (Navigation Logic)

- **Menu główne (navbar):** dostępne po zalogowaniu, widoczne na każdej stronie:\
  `[Dashboard] [Konie] [Treningi] [Opieka] [Kontakty] [AI Asystent] [Konto ▼]`
- **Logo „Horse Owner”**: kliknięcie = powrót do Dashboardu.
- **Przyciski powrotu (Back)** w widokach szczegółowych, np. „Powrót do konia” / „Powrót do listy”.
- **AI integracja:** dostępna z poziomu Dashboardu, zakładek profilu konia i osobnej strony Asystenta.
- **Autoryzacja:** wszystkie trasy (poza logowaniem i rejestracją) chronione przez `@login_required`.

## 🗺️ Mapa nawigacji uproszczona

```
[Login/Register]
      ↓
[Dashboard]
 ├──▶ Horses
 │     └──▶ Horse Profile
 │            ├──▶ Trainings
 │            └──▶ Care
 ├──▶ Trainings
 ├──▶ Care
 ├──▶ Contacts
 ├──▶ AI Assistant
 └──▶ Account
```

## 💡 Dodatki UX

- Breadcrumbs (ścieżka nawigacji): np. `Konie > Mira > Treningi`
- Ikony w menu dla szybkiego rozpoznania sekcji.
- Kolory aktywnej zakładki w nawigacji.
- Responsywne menu na mobile (ikonki w dolnym pasku zamiast tekstu).

