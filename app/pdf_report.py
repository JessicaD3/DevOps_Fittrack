from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from app.db import get_conn

def generate_pdf_report(user_id: int, out_path: str = "report.pdf") -> str:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT nom, prenom, taille_m FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close(); conn.close()
        raise ValueError("User introuvable")

    nom, prenom, taille_m = user

    cur.execute("""
        SELECT date_log, poids_kg, imc, categorie_imc
        FROM weight_logs
        WHERE user_id=%s
        ORDER BY date_log
    """, (user_id,))
    weights = cur.fetchall()

    cur.execute("""
        SELECT date_log, SUM(calories) as total_cal
        FROM meal_logs
        WHERE user_id=%s
        GROUP BY date_log
        ORDER BY date_log
    """, (user_id,))
    calories_by_day = cur.fetchall()

    cur.close()
    conn.close()

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"FitTrack - Rapport utilisateur: {prenom} {nom}", styles["Title"]))
    story.append(Paragraph(f"Taille: {taille_m} m", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Journal de suivi (poids / IMC / categorie)", styles["Heading2"]))
    data = [["Date", "Poids (kg)", "IMC", "Categorie"]]
    for d, p, imc, cat in weights:
        data.append([str(d), str(p), str(imc), str(cat)])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Synthese calories (par jour)", styles["Heading2"]))
    cal_data = [["Date", "Calories totales"]]
    total = 0
    for d, c in calories_by_day:
        cal_data.append([str(d), int(c)])
        total += int(c)

    cal_table = Table(cal_data)
    cal_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
    ]))
    story.append(cal_table)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Total calories (periode): {total}", styles["Normal"]))

    doc = SimpleDocTemplate(out_path, pagesize=A4)
    doc.build(story)
    return out_path
