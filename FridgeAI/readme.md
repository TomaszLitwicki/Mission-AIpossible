# Fridge & Recipe AI — asystent gotowania (MVP)

Prosta aplikacja webowa w **Python + Streamlit** korzystająca z **LLM**, która proponuje 3 przepisy na podstawie zawartości lodówki (CSV), pozwala wybrać przepis i po ugotowaniu odejmuje zużyte składniki z pliku `fridge.csv`. Jeśli nie ma możliwości połączenia się LLM zostanie wygenerowany sztuczny quasi przepis z istniejących produktów w formie testu - Dummy Recipes.

---

## Spis treści

- Wymagania
- Struktura projektu
- Instalacja
- Konfiguracja klucza API (.env)
- Uruchomienie aplikacji
- Użycie (flow)
- Format pliku `fridge.csv`
- Najczęstsze problemy
- Bezpieczeństwo

---

## Wymagania

- Python **3.11+**
- Konto i klucz API (np. OpenAI)
- (Opcjonalnie) wirtualne środowisko `venv`

---

## Struktura projektu

```
FridgeAI/
├─ app.py
├─ AGENTS.md
├─ fridge.csv
├─ prompts/
│  └─ suggest_recipes.txt
├─ requirements.txt
└─ .env               # lokalny plik z kluczami – NIE commitować
```

---

## Instalacja

W katalogu projektu:

```bash
# 1) (opcjonalnie) utwórz i aktywuj wirtualne środowisko
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# (macOS/Linux)
# source .venv/bin/activate

# 2) Zainstaluj zależności
pip install -r requirements.txt
```

---

## Konfiguracja klucza API (.env)

1. W katalogu projektu \*\*utwórz plik \*\*\`\` (jeśli go nie ma).
2. Otwórz `.env` i **wklej swój klucz API** w formacie:
   ```env
   OPENAI_API_KEY=sk-twoj_klucz_api_tutaj
   ```
   > Jeśli zostawisz pustą wartość, aplikacja się nie połączy z LLM, więc zostanie wygenerowany sztuczny przepis testowy z istniejących składnikó - dummy recipes.

> **Uwaga:** plik `.env` jest ignorowany przez Git (`.gitignore`). Nie commituj prawdziwych kluczy do repozytorium.

---

## Uruchomienie aplikacji

W katalogu projektu:

```bash
streamlit run app.py
```

Aplikacja otworzy się pod lokalnym adresem (np. `http://localhost:8501`).

---

## Użycie (flow)

1. Upewnij się, że `fridge.csv` zawiera Twoje składniki.
2. W aplikacji kliknij **Zaproponuj przepisy**.
3. Wybierz jeden z 3 przepisów.
4. Wyświetl kroki i ugotuj.
5. Kliknij **Ugotowane!** – aplikacja odejmie wykorzystane ilości z `fridge.csv`.

---

## Format pliku `fridge.csv`

Wymagany nagłówek i 3 kolumny:

```csv
name,quantity,unit
jajko,6,szt
mleko,1,l
mąka,500,g
```

- `name` — nazwa składnika
- `quantity` — liczba (może być ułamkowa, np. `0.5`)
- `unit` — jednostka (`szt`, `g`, `kg`, `ml`, `l`)

> W MVP odejmowanie ilości działa tylko w **tej samej jednostce** (brak automatycznych konwersji).

---

## Najczęstsze problemy

- **Brak klucza API** – uzupełnij `OPENAI_API_KEY` w `.env`.
- \`\` – zainstaluj zależności w aktywnym `.venv`.
- **Polskie znaki w CSV** – zapisz `fridge.csv` w **UTF-8**.
- **Aplikacja nie otwiera przeglądarki** – wejdź ręcznie na `http://localhost:8501`.

---

## Bezpieczeństwo

- Nigdy nie commituj prawdziwego `.env` do repo.
- Wyciek klucza → **od razu** unieważnij w panelu dostawcy i wygeneruj nowy.

---

Made with 🍳 + 🧠 by Tomasz Litwicki

