from app.imc import calcul_imc, categorie_imc

def test_calcul_imc():
    imc = calcul_imc(81, 1.80)
    assert round(imc, 2) == round(81 / (1.8**2), 2)

def test_categories():
    assert categorie_imc(18.4) == "maigre"
    assert categorie_imc(18.5) == "normal"
    assert categorie_imc(24.9) == "normal"
    assert categorie_imc(25.0) == "surpoids"
    assert categorie_imc(29.9) == "surpoids"
    assert categorie_imc(30.0) == "obesite"
