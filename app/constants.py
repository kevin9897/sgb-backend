"""Constantes y reglas de negocio del Sistema de Gestión Bibliotecaria (Universidad de Madeira)."""
from enum import Enum


class RolUsuario(str, Enum):
    ESTUDIANTE = "ESTUDIANTE"
    PROFESOR = "PROFESOR"
    BIBLIOTECARIO = "BIBLIOTECARIO"


class TipoColeccion(str, Enum):
    GENERAL = "GENERAL"
    RESERVA = "RESERVA"
    REFERENCIA = "REFERENCIA"
    HEMEROTECA = "HEMEROTECA"
    MAPOTECA = "MAPOTECA"
    TECNOTECA_LAPTOP = "TECNOTECA_LAPTOP"
    TECNOTECA_TABLETA = "TECNOTECA_TABLETA"


class EstadoRecurso(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    PRESTADO = "PRESTADO"
    RESERVADO = "RESERVADO"
    PERDIDO = "PERDIDO"
    DADO_DE_BAJA = "DADO_DE_BAJA"


# Reglas de préstamo y renovación por colección
REGLAS_COLECCION = {
    TipoColeccion.GENERAL: {"dias_prestamo": 15, "max_renovaciones": 5, "permite_reserva": True},
    TipoColeccion.RESERVA: {"dias_prestamo": 5, "max_renovaciones": 0, "permite_reserva": False},
    TipoColeccion.REFERENCIA: {"dias_prestamo": 3, "max_renovaciones": 2, "permite_reserva": False},
    TipoColeccion.HEMEROTECA: {"dias_prestamo": 1, "max_renovaciones": 1, "permite_reserva": False},
    TipoColeccion.MAPOTECA: {"dias_prestamo": 1, "max_renovaciones": 0, "permite_reserva": False, "hora_limite": 21},
    TipoColeccion.TECNOTECA_LAPTOP: {"dias_prestamo": 7, "max_renovaciones": 2, "permite_reserva": False},
    TipoColeccion.TECNOTECA_TABLETA: {"dias_prestamo": 7, "max_renovaciones": 2, "permite_reserva": True},
}

DIAS_PARA_PERDIDO = 120
DIAS_VIGENCIA_RESERVA = 5


def calcular_valor_multa(dias_habiles_atraso: int) -> int:
    """
    Calcula la multa en COP según días hábiles de atraso:
    - 1er día: 1000 COP
    - 2º al 7º día: 2500 COP
    - 8º día en adelante: 2500 + 100 COP por cada día adicional desde el 8º
    """
    if dias_habiles_atraso <= 0:
        return 0
    if dias_habiles_atraso == 1:
        return 1000
    if 2 <= dias_habiles_atraso <= 7:
        return 2500
    return 2500 + (dias_habiles_atraso - 7) * 100
