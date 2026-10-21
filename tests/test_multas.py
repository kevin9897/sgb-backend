from app.constants import calcular_valor_multa


def test_calculo_multas_segun_enunciado():
    assert calcular_valor_multa(0) == 0
    assert calcular_valor_multa(1) == 1000
    assert calcular_valor_multa(2) == 2500
    assert calcular_valor_multa(7) == 2500
    assert calcular_valor_multa(8) == 2600
    assert calcular_valor_multa(10) == 2800
