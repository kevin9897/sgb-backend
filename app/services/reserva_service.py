"""Capa de Lógica de Negocio (Service) para Reservas."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import REGLAS_COLECCION, RolUsuario
from app.models.prestamo import Reserva
from app.repositories.multa_repository import MultaRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.prestamo import ReservaCreate


class ReservaService:
    def __init__(self, db: Session):
        self.prestamo_repo = PrestamoRepository(db)
        self.recurso_repo = RecursoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.multa_repo = MultaRepository(db)

    def listar_reservas(self):
        return self.prestamo_repo.listar_reservas_activas()

    def crear_reserva(self, data: ReservaCreate) -> Reserva:
        usuario = self.usuario_repo.obtener_por_identificacion_o_codigo(data.identificacion_usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        bib = self.usuario_repo.obtener_por_identificacion_o_codigo(data.identificacion_bibliotecario)
        if not bib or bib.rol != RolUsuario.BIBLIOTECARIO:
            raise HTTPException(status_code=403, detail="Identificación de bibliotecario inválida")

        if self.multa_repo.tiene_multas_pendientes(usuario.identificacion):
            raise HTTPException(status_code=400, detail="Usuario con multas pendientes no puede reservar")

        recurso = self.recurso_repo.obtener_por_codigo(data.codigo_recurso)
        if not recurso:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")

        if not REGLAS_COLECCION[recurso.coleccion]["permite_reserva"]:
            raise HTTPException(
                status_code=400,
                detail="Las reservas solo aplican para Colección General y Tabletas",
            )

        cola_actual = self.prestamo_repo.listar_reservas_activas(recurso.codigo_recurso)
        orden = len(cola_actual) + 1

        reserva = Reserva(
            identificacion_usuario=usuario.identificacion,
            codigo_recurso=recurso.codigo_recurso,
            dias_restantes_prestamo=5,
            identificacion_bibliotecario=bib.identificacion,
            orden_cola=orden,
            activa=True,
        )
        return self.prestamo_repo.guardar_reserva(reserva)
