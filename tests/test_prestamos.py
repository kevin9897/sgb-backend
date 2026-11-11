from datetime import datetime
from app.constants import REGLAS_COLECCION, TipoColeccion
from app.utils import (
    calcular_fecha_devolucion,
    generar_codigo_institucional,
    generar_codigo_recurso_por_coleccion,
    validar_regla_renovacion,
)


def test_reglas_dias_y_renovaciones():
    assert REGLAS_COLECCION[TipoColeccion.GENERAL]["dias_prestamo"] == 15
    assert REGLAS_COLECCION[TipoColeccion.GENERAL]["max_renovaciones"] == 5
    assert REGLAS_COLECCION[TipoColeccion.RESERVA]["dias_prestamo"] == 5
    assert REGLAS_COLECCION[TipoColeccion.RESERVA]["max_renovaciones"] == 0
    assert REGLAS_COLECCION[TipoColeccion.REFERENCIA]["dias_prestamo"] == 3
    assert REGLAS_COLECCION[TipoColeccion.REFERENCIA]["max_renovaciones"] == 2
    assert REGLAS_COLECCION[TipoColeccion.HEMEROTECA]["dias_prestamo"] == 1
    assert REGLAS_COLECCION[TipoColeccion.HEMEROTECA]["max_renovaciones"] == 1
    assert REGLAS_COLECCION[TipoColeccion.MAPOTECA]["max_renovaciones"] == 0
    assert REGLAS_COLECCION[TipoColeccion.TECNOTECA_LAPTOP]["dias_prestamo"] == 7
    assert REGLAS_COLECCION[TipoColeccion.TECNOTECA_LAPTOP]["max_renovaciones"] == 2


def test_motor_reglas_renovacion_y_generador_codigos():
    ok, _ = validar_regla_renovacion(TipoColeccion.GENERAL, 2, False)
    assert ok is True
    bloqueado_reserva, _ = validar_regla_renovacion(TipoColeccion.GENERAL, 0, True)
    assert bloqueado_reserva is False
    bloqueado_tope, _ = validar_regla_renovacion(TipoColeccion.GENERAL, 5, False)
    assert bloqueado_tope is False
    bloqueado_coleccion, _ = validar_regla_renovacion(TipoColeccion.RESERVA, 0, False)
    assert bloqueado_coleccion is False

    assert generar_codigo_recurso_por_coleccion(TipoColeccion.GENERAL, 25) == "GEN-025"
    assert generar_codigo_institucional("PR").startswith("PR-")


def test_mapoteca_devolucion_21h():
    inicio = datetime(2026, 10, 21, 10, 30)
    dev = calcular_fecha_devolucion(TipoColeccion.MAPOTECA, inicio)
    assert dev.hour == 21 and dev.minute == 0
