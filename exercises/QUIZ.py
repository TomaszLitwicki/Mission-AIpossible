from openai import OpenAI
from dotenv import load_dotenv
import json
import random

load_dotenv()

client = OpenAI()

print("QUIZ ZEN - Zwierzęta Edukacja Natura")

print("Następuje generowanie pytań przez AI w kategoriach:")
print("Z - zwierzęta")
print("E - edukacja")
print("N - natura")
print("Poczekaj chwilę na AI, zaraz pojawi się opcja wyboru kategorii...")

# {
#     "tresc": "Które zwierzę potrafi spać stojąc?",
#     "odpowiedzi": {
#       "A": "Kot",
#       "B": "Pies",
#       "C": "Kangur",
#       "D": "Koń"
#     },
#     "poprawna": "D"
#   }

def wczytaj_pytania (kategoria):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "user", "content":
                "Stwórz 10 pytań quizowych o " + kategoria + " w formacie JSON:\n"
                "{ \"quizy\": [\n"
                "  {\"tresc\": \"...?\", \"odpowiedzi\": {\"A\":\"...\",\"B\":\"...\",\"C\":\"...\",\"D\":\"...\"}, \"poprawna\":\"...\"},\n"
                "  ... (10 elementów)\n"
                "] }"
             }
        ]
    )
    data = json.loads(response.output_text)
    return data["quizy"]

punkty = 0
PYTANIA = {
    "zwierzeta": wczytaj_pytania('zwierzeta'),
    "edukacja": wczytaj_pytania('edukacja'),
    "natura": wczytaj_pytania('natura')
}

idx_zwierzeta = list(range(len(PYTANIA['zwierzeta'])))
idx_edukacja= list(range(len(PYTANIA['edukacja'])))
idx_natura= list(range(len(PYTANIA['natura'])))

mapa_pozostale_idx = {
    "zwierzeta": idx_zwierzeta,
    "edukacja":  idx_edukacja,
    "natura":    idx_natura
}

def podaj_kategorie () -> str:
    print("Wybierz kategorię pytania:")
    print('1-"Zwierzęta 2-"Edukacja" 3-"Natura" :',end='')
    while True:
        kategoria = input()
        match kategoria:
            case '1':
                return 'zwierzeta'
            case '2':
                return 'edukacja'
            case '3':
                return 'natura'
            case _:
                print('Podaj jedną z liczb {1,2,3} odpowiadających kategorii - ', end='')


def losowanie_idx (pozostale_idx: list[int]) -> int:
    idx = random.choice(pozostale_idx)
    return idx


def wyswietl_pytanie (kategoria, idx) -> bool:
    pytania = PYTANIA[kategoria]
    print(pytania[idx]['tresc'])
    print(pytania[idx]['odpowiedzi'])

    odp = podaj_odpowiedz()

    if odp == (pytania[idx]['poprawna']):
        print("DOBRZE!")
        return True
    else:
        print(f"ŹLE!!! Poprawna odpowiedź to {pytania[idx]['poprawna']}")
        return False


def podaj_odpowiedz () -> str:
    while True:
        odp = input('Podaj odpowiedz A,B,C,D: ').strip().upper()
        if odp in {'A','B','C','D'}:
            return odp
        else:
            print("Podaj A,B,C lub D")


for i in range (5):
    kategoria = podaj_kategorie()
    print(f"Wybrałeś kategorię: {kategoria}.")
    pozostale_idx = mapa_pozostale_idx[kategoria]
    print(f'lista dostępnych pytań w tej kategorii: {pozostale_idx}')
    idx = losowanie_idx(pozostale_idx)
    print(f"Wylosowano pytanie spod indeksu {idx}.\n")
    pozostale_idx.remove(idx)
    wynik = wyswietl_pytanie(kategoria, idx)
    if wynik == True:
        punkty += 1
    print(f"Masz {punkty} punktów.\n")

print(f"\nKONIEC GRY! Dziękuję za wspólną zabawę. Osiągnąłeś wynik {punkty} punktów na 5 możliwych :)")

