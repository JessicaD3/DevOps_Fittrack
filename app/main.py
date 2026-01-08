import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from app.db import get_conn
from app.imc import calcul_imc, categorie_imc
from app.pdf_report import generate_pdf_report
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=BASE_DIR / "templates",
    static_folder=BASE_DIR / "static"
)

def get_height_from_jenkins_or_default():

    val = os.getenv("HEIGHT_M", "1.70")
    return float(val)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/users/new")
def user_new_form():
    return render_template("user_new.html")

@app.post("/users/new")
def user_new_submit():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    sexe = request.form["sexe"]
    date_naissance = request.form["date_naissance"]

    taille_m = get_height_from_jenkins_or_default()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (nom, prenom, sexe, date_naissance, taille_m) VALUES (%s,%s,%s,%s,%s)",
        (nom, prenom, sexe, date_naissance, taille_m),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

@app.get("/weights/new")
def weight_new_form():
    return render_template("weight_new.html")

@app.post("/weights/new")
def weight_new_submit():
    user_id = int(request.form["user_id"])
    date_log = request.form["date_log"]
    poids_kg = float(request.form["poids_kg"])

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT taille_m FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return "User introuvable", 404

    taille_m = float(row[0])
    imc = round(calcul_imc(poids_kg, taille_m), 2)
    cat = categorie_imc(imc)

    cur.execute(
        "INSERT INTO weight_logs (user_id, date_log, poids_kg, imc, categorie_imc) VALUES (%s,%s,%s,%s,%s)",
        (user_id, date_log, poids_kg, imc, cat),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

@app.get("/meals/new")
def meal_new_form():
    return render_template("meal_new.html")

@app.post("/meals/new")
def meal_new_submit():
    user_id = int(request.form["user_id"])
    date_log = request.form["date_log"]
    type_repas = request.form["type_repas"]
    calories = int(request.form["calories"])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meal_logs (user_id, date_log, type_repas, calories) VALUES (%s,%s,%s,%s)",
        (user_id, date_log, type_repas, calories),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

@app.get("/suivi")
def suivi():
    conn = get_conn()
    cur = conn.cursor()

    
    cur.execute("""
        SELECT date_log, poids_kg, imc, categorie_imc
        FROM weight_logs
        ORDER BY date_log
    """)
    weights = cur.fetchall()

    
    cur.execute("""
        SELECT date_log, type_repas, calories
        FROM meal_logs
        ORDER BY date_log
    """)
    meals = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "suivi.html",
        weights=weights,
        meals=meals
    )


@app.get("/report")
def report():
    user_id = int(request.args.get("user_id", "1"))
    out_path = generate_pdf_report(user_id=user_id, out_path="report.pdf")
    return send_file(out_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
