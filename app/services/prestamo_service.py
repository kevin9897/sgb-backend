"""Capa de Lógica de Negocio (Service) para Préstamos y Renovaciones (DDSI-13, DDSI-18, DDSI-16)."""
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import (
    EstadoRecurso,
    RolUsuario,
    calcular_valor_multa,
)
from app.models.multa import Multa
from app.models.prestamo import Prestamo, Renovacion
from app.repositories.auditoria_repository import AuditoriaRepository
from app.repositories.multa_repository import MultaRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.prestamo import PrestamoCreate, RenovacionCreate
from app.utils import (
    calcular_fecha_devolucion,
    contar_dias_habiles,
    generar_codigo_institucional,
    validar_regla_renovacion,
)


class PrestamoService:
    def __init__(self, db: Session):
        self.prestamo_repo = PrestamoRepository(db)
        self.recurso_repo = RecursoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.multa_repo = MultaRepository(db)
        self.auditoria_repo = AuditoriaRepository(db)

    def listar_prestamos(self, solo_activos: bool = False):
        return self.prestamo_repo.listar_prestamos(solo_activos=solo_activos)

    def registrar_prestamo(self, data: PrestamoCreate) -> Prestamo:
        usuario = self.usuario_repo.obtener_por_identificacion_o_codigo(data.identificacion_usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado o inactivo")

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
            raise HTTPException(status_code=404, detail="Recurso no encontrado o dado de baja")
        if recurso.estado not in (EstadoRecurso.DISPONIBLE, EstadoRecurso.RESERVADO):
            raise HTTPException(status_code=400, detail=f"Recurso no disponible (estado actual: {recurso.estado})")

        reservas = self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)
        if reservas:
            primera = reservas[0]
            if primera.identificacion_usuario != usuario.identificacion:
                raise HTTPException(status_code=400, detail="El recurso está reservado para otro usuario en la cola")
            primera.activa = False

        ahora = datetime.utcnow()
        fecha_dev = calcular_fecha_devolucion(recurso.coleccion, ahora)
        codigo_prestamo = generar_codigo_institucional("PR")

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
        guardado = self.prestamo_repo.guardar_prestamo(prestamo)
        self.auditoria_repo.registrar_evento(
            accion="PRESTAMO_CREADO",
            entidad="Prestamo",
            entidad_codigo=codigo_prestamo,
            usuario_actor=bib.identificacion,
            detalle=f"Préstamo de {recurso.codigo_recurso} a usuario {usuario.identificacion} hasta {fecha_dev.strftime('%Y-%m-%d %H:%M')}",
        )
        return guardado

    def renovar_prestamo(self, data: RenovacionCreate) -> Renovacion:
        prestamo = self.prestamo_repo.obtener_por_codigo(data.codigo_prestamo)
        if not prestamo or not prestamo.activo:
            raise HTTPException(status_code=404, detail="Préstamo activo no encontrado")

        recurso = self.recurso_repo.obtener_por_codigo(prestamo.codigo_recurso)
        tiene_reservas = len(self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)) > 0

        permitido, motivo = validar_regla_renovacion(
            recurso.coleccion,
            prestamo.renovaciones_realizadas,
            tiene_reservas,
        )
        if not permitido:
            raise HTTPException(status_code=400, detail=motivo)

        prestamo.renovaciones_realizadas += 1
        prestamo.fecha_devolucion = calcular_fecha_devolucion(recurso.coleccion, prestamo.fecha_devolucion)
        self.prestamo_repo.guardar_prestamo(prestamo)

        renovacion = Renovacion(
            codigo_prestamo=prestamo.codigo_prestamo,
            codigo_recurso=prestamo.codigo_recurso,
            identificacion_usuario=prestamo.identificacion_usuario,
            identificacion_bibliotecario=data.identificacion_bibliotecario,
        )
        guardada = self.prestamo_repo.guardar_renovacion(renovacion)
        self.auditoria_repo.registrar_evento(
            accion="PRESTAMO_RENOVADO",
            entidad="Renovacion",
            entidad_codigo=prestamo.codigo_prestamo,
            usuario_actor=data.identificacion_bibliotecario,
            detalle=f"Renovación #{prestamo.renovaciones_realizadas} del recurso {prestamo.codigo_recurso}",
        )
        return guardada

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
            self.auditoria_repo.registrar_evento(
                accion="MULTA_AUTOMATICA",
                entidad="Multa",
                entidad_codigo=prestamo.codigo_prestamo,
                usuario_actor=prestamo.identificacion_bibliotecario,
                detalle=f"Multa automática por {dias_atraso} días hábiles de atraso: ${valor} COP",
            )

        guardado = self.prestamo_repo.guardar_prestamo(prestamo)
        self.auditoria_repo.registrar_evento(
            accion="PRESTAMO_DEVUELTO",
            entidad="Prestamo",
            entidad_codigo=prestamo.codigo_prestamo,
            usuario_actor=prestamo.identificacion_bibliotecario,
            detalle=f"Devolución del recurso {prestamo.codigo_recurso} por usuario {prestamo.identificacion_usuario}",
        )
        return guardado
