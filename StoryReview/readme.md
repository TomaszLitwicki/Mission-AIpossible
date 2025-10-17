# 📝 Story Review

Prosty projekt w Pythonie wykorzystujący model OpenAI do **analizy, korekty i kontynuacji opowiadań**. Program wczytuje tekst z pliku (można wkleić własny), przekazuje go do modelu AI wraz z wybranymi parametrami (język, skala oceny, korekta, kontynuacja) i wyświetla wynik w formacie JSON.

---

## ⚙️ Wymagania

- Python 3.10+
- `openai`
- `python-dotenv`

Instalacja zależności:

```bash
pip install openai python-dotenv
```

---

## 📂 Struktura projektu

```
Story_Review.py        # główny skrypt
storyp_prompt/rompt.md # definicja promptu AI
story_file/story.txt   # plik z opowiadaniem (wklej własny)
.env                   # plik z kluczem API
```

---

## 🔑 Plik .env

Utwórz plik `.env` w katalogu głównym projektu:

```
OPENAI_API_KEY=tu_wklej_swoj_klucz_API
```

---

## ▶️ Uruchomienie

W terminalu (wewnątrz katalogu projektu):

```bash
python Story_Review.py
```

Postępuj zgodnie z instrukcjami w terminalu, aby:

1. Wybrać język opowiadania.
2. Wybrać skalę oceny (szkolna / procentowa / opisowa).
3. Zadecydować, czy chcesz poprawioną wersję.
4. Zadecydować, czy chcesz kontynuację historii.

---

##

