import csv
import json
import os
from typing import List, Dict, Any

import streamlit as st
from dotenv import load_dotenv

# --- Config & Env ---
load_dotenv()

# --- Data types ---
FridgeItem = Dict[str, Any]
Recipe = Dict[str, Any]


# --- CSV utilities ---
def load_fridge(csv_path: str) -> List[FridgeItem]:
    """Load fridge items from CSV (columns: name,quantity,unit). Quantity is float.
    Returns list of dicts: {name: str, quantity: float, unit: str}
    """
    items: List[FridgeItem] = []
    if not os.path.exists(csv_path):
        return items
    with open(csv_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                quantity = float(str(row.get("quantity", "0")).replace(",", "."))
            except ValueError:
                quantity = 0.0
            items.append({
                "name": str(row.get("name", "")).strip(),
                "quantity": quantity,
                "unit": str(row.get("unit", "")).strip(),
            })
    return items


def save_fridge(csv_path: str, items: List[FridgeItem]) -> None:
    """Save fridge items back to CSV using the same 3-column schema."""
    fieldnames = ["name", "quantity", "unit"]
    with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            # Keep simple formatting; store quantity as int if integral, else float
            q = it.get("quantity", 0)
            if isinstance(q, float) and q.is_integer():
                q_out = int(q)
            else:
                q_out = q
            writer.writerow({
                "name": it.get("name", ""),
                "quantity": q_out,
                "unit": it.get("unit", ""),
            })


def normalize_key(name: str, unit: str) -> str:
    return f"{name.strip().lower()}|{unit.strip().lower()}"


# --- LLM integration ---
def read_prompt_template(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Minimal inline fallback prompt if file missing
        return (
            "Jesteś asystentem kulinarnym. Użytkownik ma w domu następujące składniki:\n\n"
            "{{ingredients}}\n\n"
            "Na ich podstawie zaproponuj dokładnie 3 przepisy w formacie JSON:\n"
            "{\n\"recipes\": [\n{\n\"title\": \"...\",\n\"ingredients\": [\n{\"name\": \"...\", \"quantity\": ..., \"unit\": \"...\"}\n],\n\"steps\": [\"...\", \"...\"]\n}\n]\n}\n\n"
            "Nie dodawaj żadnego komentarza ani tekstu spoza JSON.\n"
            "Nie wymyślaj składników spoza listy – możesz użyć tylko tych podanych.\n"
        )


def format_ingredients_for_prompt(items: List[FridgeItem]) -> str:
    # Simple, readable bullet list
    lines = []
    for it in items:
        # Keep exact name and unit to encourage correct matching
        lines.append(f"- {it['name']}: {it['quantity']} {it['unit']}")
    return "\n".join(lines)


def extract_json(text: str) -> str:
    """Extract the first JSON object from text. Returns '{}' if not found."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return "{}"


def llm_suggest_recipes(items: List[FridgeItem]) -> Dict[str, Any]:
    """Ask LLM for exactly 3 recipes. Returns parsed dict with key 'recipes'.
    Falls back to a local dummy set if API key missing or any error occurs.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "suggest_recipes.txt")
    template = read_prompt_template(prompt_path)
    ingredients_str = format_ingredients_for_prompt(items)
    prompt = template.replace("{{ingredients}}", ingredients_str)

    try:
        # Lazy import so app can run without openai installed until needed
        from openai import OpenAI
        client = OpenAI()

        # Using a lightweight model suitable for JSON outputs
        resp = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Zwracaj wyłącznie czysty JSON, bez komentarzy."},
                {"role": "user", "content": prompt},
            ],
        )
        content = resp.choices[0].message.content or "{}"
        text_json = extract_json(content)
        data = json.loads(text_json)
        # Basic validation
        if not isinstance(data, dict) or "recipes" not in data:
            return dummy_recipes(items)
        # Ensure it's exactly 3 recipes if possible
        if isinstance(data.get("recipes"), list):
            data["recipes"] = data["recipes"][:3]
        return data
    except Exception:
        return dummy_recipes(items)


def dummy_recipes(items: List[FridgeItem]) -> Dict[str, Any]:
    # Build a trivial set of suggestions using up to first few ingredients
    top = items[:5]
    def q(n):
        try:
            return float(n)
        except Exception:
            return 1.0
    recipes = []
    if len(top) >= 2:
        a, b = top[0], top[1]
        recipes.append({
            "title": f"Prosty miks: {a['name']} + {b['name']}",
            "ingredients": [
                {"name": a['name'], "quantity": max(1.0, q(a['quantity']) * 0.2), "unit": a['unit']},
                {"name": b['name'], "quantity": max(1.0, q(b['quantity']) * 0.2), "unit": b['unit']},
            ],
            "steps": [
                f"Połącz {a['name']} i {b['name']}.",
                "Dopraw do smaku i podaj.",
            ],
        })
    if len(top) >= 3:
        c = top[2]
        recipes.append({
            "title": f"Sałatka z {c['name']}",
            "ingredients": [
                {"name": c['name'], "quantity": max(1.0, q(c['quantity']) * 0.3), "unit": c['unit']},
            ],
            "steps": [
                f"Pokrój {c['name']} i wymieszaj.",
                "Podawaj świeże.",
            ],
        })
    if len(top) >= 1:
        a = top[0]
        recipes.append({
            "title": f"Szybkie danie z {a['name']}",
            "ingredients": [
                {"name": a['name'], "quantity": max(1.0, q(a['quantity']) * 0.1), "unit": a['unit']},
            ],
            "steps": [
                f"Użyj {a['name']} jako bazy.",
                "Krótko podgrzej i podaj.",
            ],
        })
    # Ensure exactly 3 (pad if needed)
    while len(recipes) < 3:
        recipes.append({
            "title": "Propozycja rezerwowa",
            "ingredients": [],
            "steps": ["Brak kroków – uzupełnij składniki."],
        })
    return {"recipes": recipes[:3]}


# --- Cooking / update logic ---
def cook_recipe(fridge: List[FridgeItem], recipe: Recipe) -> List[FridgeItem]:
    by_key = {normalize_key(it["name"], it["unit"]): it for it in fridge}
    for ing in recipe.get("ingredients", []):
        name = str(ing.get("name", "")).strip()
        unit = str(ing.get("unit", "")).strip()
        try:
            needed = float(ing.get("quantity", 0))
        except Exception:
            needed = 0.0
        k = normalize_key(name, unit)
        if k in by_key:
            current = float(by_key[k].get("quantity", 0))
            new_val = max(0.0, current - max(0.0, needed))
            by_key[k]["quantity"] = new_val
    # Return list preserving original order
    return [by_key[normalize_key(it["name"], it["unit"])] for it in fridge]


# --- Streamlit UI ---
st.set_page_config(page_title="Fridge & Recipe AI – Asystent kuchenny", page_icon="🥗", layout="centered")
st.title("Fridge & Recipe AI – Asystent kuchenny")

DATA_PATH = os.path.join(os.path.dirname(__file__), "fridge.csv")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
os.makedirs(PROMPTS_DIR, exist_ok=True)

if "recipes" not in st.session_state:
    st.session_state["recipes"] = None
if "selected_idx" not in st.session_state:
    st.session_state["selected_idx"] = 0

# Load and show fridge
fridge_items = load_fridge(DATA_PATH)

st.subheader("Zawartość lodówki:")
if fridge_items:
    st.table([{"name": it["name"], "quantity": it["quantity"], "unit": it["unit"]} for it in fridge_items])
else:
    st.info("Brak danych w lodówce. Edytuj plik fridge.csv, aby dodać składniki.")

# Suggest recipes button
if st.button("Zaproponuj przepisy"):
    with st.spinner("Pytam model LLM o 3 przepisy..."):
        st.session_state["recipes"] = llm_suggest_recipes(fridge_items)
        st.session_state["selected_idx"] = 0

# Show recipe suggestions
recipes_data = st.session_state.get("recipes")
if recipes_data and isinstance(recipes_data, dict) and recipes_data.get("recipes"):
    recs: List[Recipe] = recipes_data["recipes"]
    titles = [r.get("title", f"Przepis {i+1}") for i, r in enumerate(recs)]
    st.subheader("Wybierz przepis")
    idx = st.radio("Propozycje", options=list(range(len(recs))), format_func=lambda i: titles[i])
    st.session_state["selected_idx"] = int(idx)

    chosen = recs[st.session_state["selected_idx"]]

    st.markdown("**Składniki:**")
    ings = chosen.get("ingredients", [])
    if ings:
        for ing in ings:
            st.write(f"- {ing.get('name', '')}: {ing.get('quantity', '')} {ing.get('unit', '')}")
    else:
        st.write("(brak składników w tej propozycji)")

    st.markdown("**Kroki przygotowania:**")
    steps = chosen.get("steps", [])
    if steps:
        for i, step in enumerate(steps, start=1):
            st.write(f"{i}. {step}")
    else:
        st.write("(brak kroków)")

    if st.button("Ugotowane! ✅"):
        updated = cook_recipe(fridge_items, chosen)
        save_fridge(DATA_PATH, updated)
        st.success("Zaktualizowano lodówkę. Odświeżam widok...")
        # Clear state and rerun to show refreshed CSV
        st.session_state["recipes"] = None
        st.session_state["selected_idx"] = 0
        st.rerun()

st.caption("Wskazówka: Ustaw OPENAI_API_KEY w pliku .env, aby korzystać z prawdziwych propozycji LLM. Bez klucza używany jest tryb zastępczy (dummy).")
