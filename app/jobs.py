"""Tareas automáticas de negocio (120 días para PERDIDO, vencimiento de reservas de 5 días)."""
from datetime import datetime
from sqlalchemy.orm import Session
from app.constants import DIAS_PARA_PERDIDO, DIAS_VIGENCIA_RESERVA, EstadoRecurso
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.recurso_repository import RecursoRepository


def ejecutar_tareas_automaticas(db: Session) -> dict:
    prestamo_repo = PrestamoRepository(db)
    recurso_repo = RecursoRepository(db)
    ahora = datetime.utcnow()
    marcados_perdidos = 0
    reservas_vencidas = 0

    # 1. Después de 120 días sin devolver se cambia automáticamente a PERDIDO
    for prestamo in prestamo_repo.listar_prestamos(solo_activos=True):
        dias_sin_devolver = (ahora - prestamo.fecha_devolucion).days
        if dias_sin_devolver >= DIAS_PARA_PERDIDO:
            recurso = recurso_repo.obtener_por_codigo(prestamo.codigo_recurso)
            if recurso and recurso.estado != EstadoRecurso.PERDIDO:
                recurso_repo.actualizar_estado(recurso, EstadoRecurso.PERDIDO)
                marcados_perdidos += 1

    # 2. Si en 5 días el usuario no procede con el préstamo, la reserva se vence y pasa al siguiente
    for reserva in prestamo_repo.listar_reservas_activas():
        recurso = recurso_repo.obtener_por_codigo(reserva.codigo_recurso)
        if recurso and recurso.estado == EstadoRecurso.RESERVADO and reserva.orden_cola == 1:
            dias_transcurridos = (ahora - reserva.fecha_hora_reserva).days
            if dias_transcurridos >= DIAS_VIGENCIA_RESERVA or reserva.dias_restantes_prestamo <= 0:
                reserva.activa = False
                reservas_vencidas += 1
                prestamo_repo.guardar_reserva(reserva)
                # Reordenar cola restante
                cola_restante = prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)
                if cola_restante:
                    for idx, sig in enumerate(cola_restante, start=1):
                        sig.orden_cola = idx
                        if idx == 1:
                            sig.dias_restantes_prestamo = DIAS_VIGENCIA_RESERVA
                        prestamo_repo.guardar_reserva(sig)
                else:
                    recurso_repo.actualizar_estado(recurso, EstadoRecurso.DISPONIBLE)

    return {
        "recursos_marcados_perdidos": marcados_perdidos,
        "reservas_vencidas": reservas_vencidas,
    }
