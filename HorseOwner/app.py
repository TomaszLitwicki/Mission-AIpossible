from flask import Flask, g, render_template
import sqlite3
import os

from flask import request, redirect, url_for, flash

from datetime import date

TRAINING_LABELS = {
    'dressage': 'Ujeżdżenie',
    'jumping': 'Skoki',
    'trail': 'Teren',
    'groundwork': 'Z ziemi',
    'other': 'Inne'
}

HORSE_LABELS = {
    "name": "Imię",
    "breed": "Rasa",
    "sex": "Płeć",
    "birth_date": "Data ur.",
    "color": "Maść",
    "origin": "Pochodzenie",
    "notes": "Notatki",
}

HORSE_FIELDS_ORDER = ["name", "breed", "sex", "birth_date", "color", "origin", "notes"]

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)
DB_PATH = os.path.join(app.instance_path, "horse_owner.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.context_processor
def inject_today():
    return {"today": date.today().isoformat()}

#--- Feature 3 ---

@app.route("/horses/<int:horse_id>")
def horse_detail(horse_id):
    db = get_db()

    # 1) Dane konia
    horse = db.execute("SELECT * FROM horses WHERE id = ?", (horse_id,)).fetchone()
    if horse is None:
        flash("Nie znaleziono takiego konia.", "warning")
        return redirect(url_for("index"))

    horse_dict = dict(horse)

    # 2) Treningi tego konia (najnowsze najpierw)
    trainings = db.execute("""
        SELECT id, date, time, duration_min, type, score, satisfied, notes
        FROM trainings
        WHERE horse_id = ?
        ORDER BY date DESC, time DESC
    """, (horse_id,)).fetchall()

    # 3) Zabiegi pielęgnacyjne (z tabeli 'treatments') dla tego konia
    treatments = db.execute("""
        SELECT id, name, date, status, notes
        FROM treatments
        WHERE horse_id = ?
        ORDER BY date DESC
    """, (horse_id,)).fetchall()

    # 4) Placeholder pod wynik AI (przekazany przez redirect po POST)
    ai_user_msg = request.args.get("ai_user_msg", "")
    ai_reply = request.args.get("ai_reply", "")

    return render_template(
        "horses/detail.html",
        horse_dict=horse_dict,
        trainings=trainings,
        treatments=treatments,
        TRAINING_LABELS=TRAINING_LABELS,
        HORSE_LABELS=HORSE_LABELS,
        HORSE_FIELDS_ORDER=HORSE_FIELDS_ORDER,
        ai_user_msg=ai_user_msg,
        ai_reply=ai_reply
    )


@app.route("/horses/<int:horse_id>/ai", methods=["POST"])
def horse_ai(horse_id):
    # Na razie: zbieramy tekst i wracamy na stronę z placeholderem odpowiedzi.
    user_msg = (request.form.get("user_msg") or "").strip()
    ai_reply = "(tu w następnym etapie wstawimy prawdziwą odpowiedź LLM)"
    return redirect(url_for(
        "horse_detail",
        horse_id=horse_id,
        ai_user_msg=user_msg,
        ai_reply=ai_reply
    ))

#--- Feature 2 ---
@app.route("/treatments")
def treatments_list():
    db = get_db()
    rows = db.execute("""
        SELECT tr.id, tr.name, tr.date, tr.status, tr.notes,
               h.name AS horse_name, h.id AS horse_id
        FROM treatments tr
        JOIN horses h ON h.id = tr.horse_id
        ORDER BY tr.date DESC, h.name
    """).fetchall()
    return render_template("treatments/list.html", treatments=rows)

@app.route("/treatments/toggle/<int:tr_id>", methods=["POST"])
def treatments_toggle(tr_id):
    db = get_db()
    # flip 0 -> 1, 1 -> 0
    db.execute("""
        UPDATE treatments
        SET status = CASE status WHEN 1 THEN 0 ELSE 1 END
        WHERE id = ?
    """, (tr_id,))
    db.commit()
    return redirect("/treatments")

@app.route("/treatments/new", methods=["GET","POST"])
def treatments_new():
    db = get_db()
    if request.method == "POST":
        horse_id = request.form.get("horse_id", type=int)
        name = request.form.get("name", type=str)
        date = request.form.get("date", type=str)
        notes = request.form.get("notes", type=str)
        errors = []
        if not horse_id: errors.append("Wybierz konia.")
        if not name: errors.append("Podaj nazwę zabiegu.")
        if not date: errors.append("Podaj datę (YYYY-MM-DD).")
        if errors:
            horses = db.execute("SELECT id, name FROM horses ORDER BY name").fetchall()
            return render_template("treatments/new.html", horses=horses, errors=errors, form=request.form)
        db.execute("""
            INSERT INTO treatments (horse_id, name, date, status, notes)
            VALUES (?, ?, ?, 0, ?)
        """, (horse_id, name, date, notes))
        db.commit()
        return redirect("/treatments")

    horses = db.execute("SELECT id, name FROM horses ORDER BY name").fetchall()
    return render_template("treatments/new.html", horses=horses)


@app.route("/trainings")
def trainings_list():
    """
    Lista wszystkich treningów z prostymi filtrami:
      - ?horse_id=ID
      - ?period=week|month   (month = date('now','-1 month'))
      - ?satisfied=1|0
    Sort: najnowsze najpierw (data DESC, time DESC)
    """
    db = get_db()

    # 1) Pobranie listy koni do selecta filtra
    horses = db.execute(
        "SELECT id, name FROM horses ORDER BY name"
    ).fetchall()

    # 2) Filtry z query string
    horse_id = request.args.get("horse_id", type=int)
    period   = request.args.get("period")       # None | "week" | "month"
    satisfied = request.args.get("satisfied")   # None | "1" | "0"

    where = []
    params = {}

    if horse_id:
        where.append("t.horse_id = :horse_id")
        params["horse_id"] = horse_id

    if period == "week":
        # 7 dni wstecz
        where.append("t.date >= date('now','-7 days')")
    elif period == "month":
        # „od tego samego dnia miesiąc temu” – SQLite: -1 month uwzględnia 30/31
        where.append("t.date >= date('now','-1 month')")

    if satisfied in ("0", "1"):
        where.append("t.satisfied = :satisfied")
        params["satisfied"] = int(satisfied)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    # 3) Pobranie wyników
    trainings = db.execute(f"""
        SELECT t.id, t.date, t.time, t.duration_min, t.type, t.score, t.satisfied,
               t.notes,
               h.name AS horse_name, h.id AS horse_id
        FROM trainings t
        JOIN horses h ON h.id = t.horse_id
        {where_sql}
        ORDER BY t.date DESC, COALESCE(t.time,'00:00') DESC
    """, params).fetchall()

    return render_template(
        "trainings/list.html",
        trainings=trainings,
        horses=horses,
        labels=TRAINING_LABELS,
        current_filters={"horse_id": horse_id, "period": period, "satisfied": satisfied},
    )


@app.route("/trainings/new", methods=["GET", "POST"])
def trainings_new():
    db = get_db()

    if request.method == "POST":
        horse_id = request.form.get("horse_id", type=int)
        date = request.form.get("date", type=str)         # YYYY-MM-DD
        time = request.form.get("time", type=str)         # HH:MM lub ''
        duration_min = request.form.get("duration_min", type=int)
        ttype = request.form.get("type", type=str)
        score = request.form.get("score", type=int)       # może być puste → None
        satisfied = request.form.get("satisfied", type=int)  # 0/1
        notes = request.form.get("notes", type=str)

        # Minimalna walidacja
        errors = []
        if not horse_id:
            errors.append("Wybierz konia.")
        if not date:
            errors.append("Podaj datę.")
        if duration_min is None or duration_min <= 0:
            errors.append("Czas trwania musi być dodatni (minuty).")
        if ttype not in TRAINING_LABELS:
            errors.append("Niepoprawny typ treningu.")
        if satisfied not in (0, 1):
            errors.append("Zadowolenie: wybierz TAK lub NIE.")
        if score is not None and not (1 <= score <= 10):
            errors.append("Ocena (score) musi być w zakresie 1–10 albo pusta.")

        if errors:
            # Prosta informacja – w MVP można wyświetlić w szablonie
            return render_template(
                "trainings/new.html",
                errors=errors,
                horses=db.execute("SELECT id, name FROM horses ORDER BY name").fetchall(),
                labels=TRAINING_LABELS,
                form=request.form
            )

        # Pusta godzina → NULL
        time_val = time if time else None
        score_val = score if score is not None else None

        db.execute("""
            INSERT INTO trainings (horse_id, date, time, duration_min, type, score, satisfied, notes)
            VALUES (:horse_id, :date, :time, :duration_min, :type, :score, :satisfied, :notes)
        """, {
            "horse_id": horse_id, "date": date, "time": time_val,
            "duration_min": duration_min, "type": ttype, "score": score_val,
            "satisfied": satisfied, "notes": notes
        })
        db.commit()

        return redirect(url_for("trainings_list"))

    # GET – formularz
    horses = db.execute("SELECT id, name FROM horses ORDER BY name").fetchall()
    return render_template("trainings/new.html", horses=horses, labels=TRAINING_LABELS)


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db = get_db()
        with open("schema.sql", "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
    print("Baza została zainicjalizowana.")


@app.cli.command("seed-db")
def seed_db():
    with app.app_context():
        db = get_db()
        with open("seed.sql", "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
    print("Dodano przykładowe dane do bazy.")


@app.route("/ping")
def ping():
    return "pong"


@app.route("/horses")
def horses_list():
    db = get_db()
    rows = db.execute("SELECT id, name, breed, sex, birth_date, color, origin, notes FROM horses ORDER BY name").fetchall()
    return render_template("horses/list.html", horses=rows)


@app.route("/")
def index():
    db = get_db()
    horses = db.execute(
        """
        SELECT id, name, breed, sex, birth_date, color, origin, notes
        FROM horses
        ORDER BY name
        """
    ).fetchall()

    last_trainings = db.execute(
        """
        SELECT t.id, t.date, t.time, t.duration_min, t.type, t.score, t.satisfied,
        h.name AS horse_name
        FROM trainings t
        JOIN horses h ON h.id = t.horse_id
        ORDER BY t.date DESC, COALESCE(t.time, '00:00') DESC
        LIMIT 5
        """
    ).fetchall()

    pending_treatments = db.execute("""
        SELECT tr.id, tr.name, tr.date, tr.status,
               h.name AS horse_name
        FROM treatments tr
        JOIN horses h ON h.id = tr.horse_id
        WHERE tr.status = 0
        ORDER BY tr.date ASC, h.name
    """).fetchall()

    return render_template("index.html",
                           horses=horses,
                           last_trainings=last_trainings,
                           pending_treatments=pending_treatments)


if __name__ == "__main__":
    app.run(debug=True)
