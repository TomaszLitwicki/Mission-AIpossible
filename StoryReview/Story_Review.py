from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

print("STORY REVIEW")


def language_choice():
    return input ("What language is this story written in: ")

def scoring_scale():
    print("""
What type of scale is this story using?
S - school → integer score from 1 (worst) to 6 (best)  
P - percentage → integer score from 0% (poor) to 100% (perfect)  
D - descriptive → one short sentence summarizing story quality""")
    while True:
        scale = input("Enter S, P or D: ").upper().strip()
        if scale in ["S", "P", "D"]:
            break
        else:
            print("Please enter correct scale type")
    match scale:
        case "S":
            scale_type = "school"
        case "P":
            scale_type = "percentage"
        case "D":
            scale_type = "descriptive"
    return scale_type


def corrected_story():
    print("""
Do you want to correct this story?
Y - yes  
N - no""")
    while True:
        corrected = input("Enter Y or N: ").upper().strip()
        if corrected in ["Y", "N"]:
            break
    if corrected == "Y":
        corrected = "True"
    elif corrected == "N":
        corrected = "False"
    return corrected


def want_continuation():
    print("""
Do you want to continue reading this story?
Y - yes  
N - no""")
    while True:
        want_continuation = input("Enter Y or N: ").upper().strip()
        if want_continuation in ["Y", "N"]:
            break
    if want_continuation == "Y":
        want_continuation = "True"
    elif want_continuation == "N":
        want_continuation = "False"
    return want_continuation


def story_load():
    with open("story_file/story.txt", "r", encoding='utf-8') as file:
        story = file.read()
    return story


def main(language_choice, scoring_scale, corrected_story, want_continuation, story_load):

    response = client.responses.parse(
      prompt={
        "id": "pmpt_68f18209f4488197a8b1688b17cd3944061764dafe139767",
        "version": "2",
        "variables": {
          "language": language_choice,
          "scale_type": scoring_scale,
          "want_corrected": corrected_story,
          "want_continuation": want_continuation,
          "story": story_load
        }
      }
    )
    data = json.loads(response.output[-1].content[0].text)

    print(f"\nOCENA: {data['overall_score']}")

    issues = data["found_issues"]
    print("\nBŁĘDY:")
    print(" - ortograficzne:", ", ".join(issues["spelling"]) if issues["spelling"] else "brak")
    print(" - interpunkcyjne:", ", ".join(issues["punctuation"]) if issues["punctuation"] else "brak")
    print(" - gramatyczne/składniowe:", ", ".join(issues["grammar_syntax"]) if issues["grammar_syntax"] else "brak")
    print(" - logiczne:", ", ".join(issues["logic"]) if issues["logic"] else "brak")

    print("\nPOPRAWIONA WERSJA:")
    print(data["improved_text"] or "— brak —")

    print("\nKONTYNUACJA HISTORII:")
    print(data["continuation_text"] or "— brak —")

if __name__ == "__main__":
    main(language_choice(), scoring_scale(), corrected_story(), want_continuation(), story_load())