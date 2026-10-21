"""Utilidades de fechas y días hábiles para multas y préstamos."""
from datetime import date, datetime, timedelta
from app.constants import REGLAS_COLECCION, TipoColeccion


def calcular_fecha_devolucion(coleccion: TipoColeccion, fecha_inicio: datetime) -> datetime:
    regla = REGLAS_COLECCION[coleccion]
    if coleccion == TipoColeccion.MAPOTECA:
        # 1 día hasta las 21:00 h
        return fecha_inicio.replace(hour=21, minute=0, second=0, microsecond=0)
    return fecha_inicio + timedelta(days=regla["dias_prestamo"])


def contar_dias_habiles(fecha_inicio: date, fecha_fin: date) -> int:
    """Cuenta días hábiles (lunes a viernes) de atraso entre dos fechas."""
    if fecha_fin <= fecha_inicio:
        return 0
    dias = 0
    actual = fecha_inicio + timedelta(days=1)
    while actual <= fecha_fin:
        if actual.weekday() < 5:  # 0=Lunes .. 4=Viernes
            dias += 1
        actual += timedelta(days=1)
    return dias
