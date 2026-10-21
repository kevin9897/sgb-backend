"""Capa de Lógica de Negocio (Service) para Préstamos y Renovaciones."""
from datetime import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import (
    EstadoRecurso,
    REGLAS_COLECCION,
    RolUsuario,
    calcular_valor_multa,
)
from app.models.multa import Multa
from app.models.prestamo import Prestamo, Renovacion
from app.repositories.multa_repository import MultaRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.prestamo import PrestamoCreate, RenovacionCreate
from app.utils import calcular_fecha_devolucion, contar_dias_habiles


class PrestamoService:
    def __init__(self, db: Session):
        self.prestamo_repo = PrestamoRepository(db)
        self.recurso_repo = RecursoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.multa_repo = MultaRepository(db)

    def listar_prestamos(self, solo_activos: bool = False):
        return self.prestamo_repo.listar_prestamos(solo_activos=solo_activos)

    def registrar_prestamo(self, data: PrestamoCreate) -> Prestamo:
        usuario = self.usuario_repo.obtener_por_identificacion_o_codigo(data.identificacion_usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        bib = self.usuario_repo.obtener_por_identificacion_o_codigo(data.identificacion_bibliotecario)
        if not bib or bib.rol != RolUsuario.BIBLIOTECARIO:
            raise HTTPException(status_code=403, detail="Identificación de bibliotecario inválida")

        if self.multa_repo.tiene_multas_pendientes(usuario.identificacion):
            raise HTTPException(
                status_code=400,
                detail="El usuario tiene multas sin pagar y no puede usar préstamos ni reservas",
            )

        recurso = self.recurso_repo.obtener_por_codigo(data.codigo_recurso)
        if not recurso:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        if recurso.estado not in (EstadoRecurso.DISPONIBLE, EstadoRecurso.RESERVADO):
            raise HTTPException(status_code=400, detail=f"Recurso no disponible (estado actual: {recurso.estado})")

        # Si está reservado, verificar que sea el primero en la cola
        reservas = self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)
        if reservas:
            primera = reservas[0]
            if primera.identificacion_usuario != usuario.identificacion:
                raise HTTPException(status_code=400, detail="El recurso está reservado para otro usuario en la cola")
            primera.activa = False

        ahora = datetime.utcnow()
        fecha_dev = calcular_fecha_devolucion(recurso.coleccion, ahora)
        codigo_prestamo = f"PR-{uuid.uuid4().hex[:8].upper()}"

        prestamo = Prestamo(
            codigo_prestamo=codigo_prestamo,
            identificacion_usuario=usuario.identificacion,
            codigo_recurso=recurso.codigo_recurso,
            fecha_hora_prestamo=ahora,
            fecha_devolucion=fecha_dev,
            identificacion_bibliotecario=bib.identificacion,
            renovaciones_realizadas=0,
            activo=True,
        )
        self.recurso_repo.actualizar_estado(recurso, EstadoRecurso.PRESTADO)
        return self.prestamo_repo.guardar_prestamo(prestamo)

    def renovar_prestamo(self, data: RenovacionCreate) -> Renovacion:
        prestamo = self.prestamo_repo.obtener_por_codigo(data.codigo_prestamo)
        if not prestamo or not prestamo.activo:
            raise HTTPException(status_code=404, detail="Préstamo activo no encontrado")

        recurso = self.recurso_repo.obtener_por_codigo(prestamo.codigo_recurso)
        regla = REGLAS_COLECCION[recurso.coleccion]

        if prestamo.renovaciones_realizadas >= regla["max_renovaciones"]:
            raise HTTPException(
                status_code=400,
                detail=f"Máximo de renovaciones alcanzado ({regla['max_renovaciones']}) para {recurso.coleccion}",
            )

        # Reservas impiden que quien tenga el recurso lo renueve
        if self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso):
            raise HTTPException(status_code=400, detail="No se puede renovar: el recurso tiene reservas activas")

        prestamo.renovaciones_realizadas += 1
        prestamo.fecha_devolucion = calcular_fecha_devolucion(recurso.coleccion, prestamo.fecha_devolucion)
        self.prestamo_repo.guardar_prestamo(prestamo)

        renovacion = Renovacion(
            codigo_prestamo=prestamo.codigo_prestamo,
            codigo_recurso=prestamo.codigo_recurso,
            identificacion_usuario=prestamo.identificacion_usuario,
            identificacion_bibliotecario=data.identificacion_bibliotecario,
        )
        return self.prestamo_repo.guardar_renovacion(renovacion)

    def devolver_prestamo(self, codigo_prestamo: str) -> Prestamo:
        prestamo = self.prestamo_repo.obtener_por_codigo(codigo_prestamo)
        if not prestamo or not prestamo.activo:
            raise HTTPException(status_code=404, detail="Préstamo activo no encontrado")

        ahora = datetime.utcnow()
        prestamo.fecha_devolucion_real = ahora
        prestamo.activo = False

        recurso = self.recurso_repo.obtener_por_codigo(prestamo.codigo_recurso)
        reservas = self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)
        if reservas:
            self.recurso_repo.actualizar_estado(recurso, EstadoRecurso.RESERVADO)
            reservas[0].dias_restantes_prestamo = 5
        else:
            self.recurso_repo.actualizar_estado(recurso, EstadoRecurso.DISPONIBLE)

        # Verificar atraso y generar multa si corresponde
        dias_atraso = contar_dias_habiles(prestamo.fecha_devolucion.date(), ahora.date())
        if dias_atraso > 0:
            valor = calcular_valor_multa(dias_atraso)
            self.multa_repo.crear(
                Multa(
                    codigo_prestamo=prestamo.codigo_prestamo,
                    codigo_recurso=prestamo.codigo_recurso,
                    identificacion_usuario=prestamo.identificacion_usuario,
                    dias_multa=dias_atraso,
                    valor_cop=valor,
                    pagada=False,
                )
            )

        return self.prestamo_repo.guardar_prestamo(prestamo)
