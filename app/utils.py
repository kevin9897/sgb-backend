"""
Utilidades de fechas, días hábiles y Motor de Reglas / Generador de Códigos (DDSI-18 / HT-05).
"""
from datetime import date, datetime, timedelta
import uuid
from app.constants import REGLAS_COLECCION, TipoColeccion

PREFIJOS_COLECCION = {
    TipoColeccion.GENERAL: "GEN",
    TipoColeccion.RESERVA: "RES",
    TipoColeccion.REFERENCIA: "REF",
    TipoColeccion.HEMEROTECA: "HEM",
    TipoColeccion.MAPOTECA: "MAP",
    TipoColeccion.TECNOTECA_LAPTOP: "LAP",
    TipoColeccion.TECNOTECA_TABLETA: "TAB",
}


def generar_codigo_institucional(prefijo: str, consecutivo: int | None = None) -> str:
    """
    Generador de códigos únicos institucionales (HT-05):
    - Con consecutivo: PR-2026-0001, GEN-021, etc.
    - Con sufijo único: PR-2026-A1B2C3
    """
    anio = datetime.utcnow().year
    if consecutivo is not None:
        return f"{prefijo}-{consecutivo:03d}"
    sufijo = uuid.uuid4().hex[:6].upper()
    return f"{prefijo}-{anio}-{sufijo}"


def generar_codigo_recurso_por_coleccion(coleccion: TipoColeccion, consecutivo: int) -> str:
    prefijo = PREFIJOS_COLECCION.get(coleccion, "REC")
    return f"{prefijo}-{consecutivo:03d}"


def validar_regla_renovacion(
    coleccion: TipoColeccion,
    renovaciones_actuales: int,
    tiene_reservas_activas: bool,
) -> tuple[bool, str]:
    """
    Motor de Reglas para Renovaciones por Colección (DDSI-18 / HT-05):
    - Verifica si hay reservas activas (bloquea renovación).
    - Verifica si la colección permite renovaciones y no supera el tope.
    """
    regla = REGLAS_COLECCION[coleccion]
    max_ren = regla["max_renovaciones"]

    if tiene_reservas_activas:
        return False, "No se puede renovar: el recurso tiene una cola de reserva activa."
    if max_ren == 0:
        return False, f"La colección {coleccion.value} no permite renovaciones (máx. 0)."
    if renovaciones_actuales >= max_ren:
        return False, f"Límite de renovaciones alcanzado ({renovaciones_actuales}/{max_ren}) para {coleccion.value}."
    return True, f"Renovación permitida ({renovaciones_actuales + 1}/{max_ren})."


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
