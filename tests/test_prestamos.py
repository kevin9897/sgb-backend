from datetime import datetime
from app.constants import REGLAS_COLECCION, TipoColeccion
from app.utils import calcular_fecha_devolucion


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


def test_mapoteca_devolucion_21h():
    inicio = datetime(2026, 10, 21, 10, 30)
    dev = calcular_fecha_devolucion(TipoColeccion.MAPOTECA, inicio)
    assert dev.hour == 21 and dev.minute == 0
