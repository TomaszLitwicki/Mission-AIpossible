# AGENTS.md – FridgeAI Assistant (Cooking Web App)

**Autor:** Tomasz Litwicki  
**Projekt:** Zadanie z kursu *Ready4AI*  
**Cel:** Stworzenie **prostej aplikacji webowej w Pythonie z użyciem AI/LLM**, która dobiera przepisy kulinarne na podstawie zawartości lodówki użytkownika.  
**Styl:** Minimalistyczny, edukacyjny, przejrzysty – bez zbędnych technologii.

---

## 🔹 Kontekst
Aplikacja ma być **MVP (Minimum Viable Product)** – najprostsza wersja asystenta kuchennego:

- użytkownik posiada listę produktów w pliku CSV,
- aplikacja pyta model językowy (LLM) o 3 przepisy z tych składników,
- użytkownik wybiera jeden przepis,
- aplikacja wyświetla instrukcję gotowania,
- po ugotowaniu aplikacja odejmuje zużyte składniki z listy.

Brak logowania, dat ważności, planów posiłków i filtrów – tylko podstawowe działanie.

---

## 🔹 Główne funkcjonalności (MVP)

### 1️⃣ Wczytanie listy produktów z pliku CSV
- Plik `fridge.csv` ma dokładnie 3 kolumny:  
  `name,quantity,unit`
- Dane są wczytywane przy użyciu modułu `csv` i funkcji `with open` – **bez użycia Pandas**.
- Program tworzy listę słowników w Pythonie.

### 2️⃣ Generowanie propozycji przepisów przez LLM
- Funkcja wysyła do modelu LLM listę składników i prosi o **dokładnie 3 przepisy**.
- Model zwraca odpowiedź w **czystym JSON-ie**, bez komentarzy ani tekstu.
- Przykład formatu:

```json
{
  "recipes": [
    {
      "title": "Jajecznica z mlekiem",
      "ingredients": [
        {"name": "jajko", "quantity": 3, "unit": "szt"},
        {"name": "mleko", "quantity": 50, "unit": "ml"},
        {"name": "sól", "quantity": 1, "unit": "szczypta"}
      ],
      "steps": [
        "Roztrzep jajka z mlekiem.",
        "Dopraw solą i smaż na maśle."
      ]
    }
  ]
}
```

### 3️⃣ Wybór przepisu przez użytkownika
- Użytkownik wybiera 1 z 3 przepisów.
- Aplikacja wyświetla listę składników i instrukcje gotowania krok po kroku.

### 4️⃣ Aktualizacja listy produktów po ugotowaniu
- Po kliknięciu „Ugotowane!”:
  - Dla każdego składnika z przepisu znajdź odpowiedni wiersz w `fridge.csv` (po `name` i `unit`),
  - Odejmij zużytą ilość, nie schodząc poniżej zera,
  - Zapisz nowy stan pliku CSV.

---

## 🔹 Wymagania techniczne

**Język:** Python 3.11+  
**Biblioteki:**
- `streamlit` – interfejs użytkownika (frontend + backend w jednym)
- `csv` – obsługa plików danych
- `openai` – komunikacja z modelem językowym
- `dotenv` – wczytanie klucza API z pliku `.env`

**Środowisko:**
- IDE: PyCharm (Community lub Pro)
- Projekt działa lokalnie (bez wdrożenia do chmury)
- Plik `.env` zawiera klucz API:
  ```
  OPENAI_API_KEY=sk-xxxxx
  ```
  i jest ładowany przez `load_dotenv()`.

---

## 🔹 Struktura projektu

```
fridgeai/
│
├── app.py                   # Główna aplikacja Streamlit
├── fridge.csv               # Lista produktów (nazwa, ilość, jednostka)
├── prompts/
│   └── suggest_recipes.txt  # Wzorzec promptu do LLM
├── .env                     # Klucz API (lokalnie, nie commitować)
└── requirements.txt         # Lista bibliotek
```

---

## 🔹 Schemat przepływu danych

1. `app.py` wczytuje dane z `fridge.csv`.  
2. Po kliknięciu przycisku „Zaproponuj przepisy” wysyła prompt do LLM.  
3. Model zwraca JSON z trzema propozycjami przepisów.  
4. Użytkownik wybiera przepis i widzi jego składniki oraz kroki.  
5. Po potwierdzeniu – funkcja `cook_recipe()` aktualizuje `fridge.csv`.  
6. Nowy stan produktów jest od razu widoczny na ekranie.

---

## 🔹 Prompt do LLM (`prompts/suggest_recipes.txt`)

```
Jesteś asystentem kulinarnym. Użytkownik ma w domu następujące składniki:

{{ingredients}}

Na ich podstawie zaproponuj dokładnie 3 przepisy w formacie JSON:
{
  "recipes": [
    {
      "title": "...",
      "ingredients": [
        {"name": "...", "quantity": ..., "unit": "..."}
      ],
      "steps": ["...", "..."]
    }
  ]
}

Nie dodawaj żadnego komentarza ani tekstu spoza JSON.
Nie wymyślaj składników spoza listy – możesz użyć tylko tych podanych.
```

---

## 🔹 Styl kodowania i założenia projektowe

- Prostota i zrozumiałość ponad wydajność.  
- Każda funkcja powinna mieć jedną odpowiedzialność.  
- Zmiennych nie ukrywamy w klasach – kod proceduralny.  
- Dane (lodówka, przepisy, historia) trzymane lokalnie w plikach.  
- Kod ma być w pełni zrozumiały dla początkującego programisty.  
- Każdy etap działania aplikacji da się uruchomić osobno (np. test funkcji `load_fridge()` w terminalu).  
- W przyszłości projekt będzie rozszerzony o dodatkowe moduły (dodawanie produktów, historia gotowania itd.).

---

## 🔹 Zakres pracy agentów AI w IDE

Agenci AI (Junie, Copilot, Cursor, Codeium itp.) mogą:
- refaktoryzować kod w duchu prostoty i czytelności,  
- pilnować spójności formatów JSON i CSV,  
- sugerować krótsze, czystsze funkcje,  
- wykrywać błędy logiczne i konwersje typów,  
- nie wprowadzać nowych technologii bez potrzeby (np. baz danych, Pandas, Docker, JS, itp.).

**Priorytet:** czysty, zrozumiały kod – edukacyjny, nieprodukcyjny.

---

## 🔹 Etapy rozwoju projektu

**Etap I – MVP (obecny):**  
✅ Wczytywanie CSV  
✅ Komunikacja z LLM  
✅ Wybór przepisu  
✅ Odejmowanie składników  

**Etap II – Planowane rozszerzenia:**  
🔸 Dodawanie produktów  
🔸 Dopasowanie przepisów do braków  
🔸 Historia gotowania  
🔸 Lista zakupów  

---

## 🔹 Cel edukacyjny projektu

Projekt ma pokazać, że nawet początkujący programista może:
- połączyć prosty kod w Pythonie z LLM,  
- stworzyć użyteczną aplikację webową,  
- zrozumieć mechanizmy promptowania i przetwarzania JSON,  
- poznać podstawy integracji AI w aplikacjach.

---

**Koniec dokumentu.**

