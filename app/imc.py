def calcul_imc(poids_kg: float, taille_m: float) -> float:
    if taille_m <= 0:
        raise ValueError("La taille doit être > 0")
    return poids_kg / (taille_m ** 2)

def categorie_imc(imc: float) -> str:
    if imc < 18.5:
        return "maigre"
    if imc < 25:
        return "normal"
    if imc < 30:
        return "surpoids"
    return "obesite"
