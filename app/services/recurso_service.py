"""Capa de Lógica de Negocio (Service) para Recursos Bibliográficos, Generador de Códigos y Borrado Lógico."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import RolUsuario
from app.repositories.auditoria_repository import AuditoriaRepository
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.recurso import DarDeBajaRequest, RecursoCreate
from app.utils import generar_codigo_recurso_por_coleccion


class RecursoService:
    def __init__(self, db: Session):
        self.recurso_repo = RecursoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.auditoria_repo = AuditoriaRepository(db)

    def listar_recursos(
        self,
        coleccion: Optional[str] = None,
        estado: Optional[str] = None,
        q: Optional[str] = None,
        incluir_eliminados: bool = False,
    ):
        return self.recurso_repo.listar(
            coleccion=coleccion,
            estado=estado,
            q=q,
            incluir_eliminados=incluir_eliminados,
        )

    def crear_recurso(self, data: RecursoCreate):
        if not data.codigo_recurso or not data.codigo_recurso.strip():
            consecutivo = self.recurso_repo.contar_por_coleccion(data.coleccion) + 1
            data.codigo_recurso = generar_codigo_recurso_por_coleccion(data.coleccion, consecutivo)
        if self.recurso_repo.obtener_por_codigo(data.codigo_recurso):
            raise HTTPException(status_code=400, detail="El código de recurso ya existe")
        creado = self.recurso_repo.crear(data)
        self.auditoria_repo.registrar_evento(
            accion="RECURSO_CREADO",
            entidad="Recurso",
            entidad_codigo=creado.codigo_recurso,
            usuario_actor="30000001",
            detalle=f"Alta de recurso '{creado.titulo}' en colección {creado.coleccion.value}",
        )
        return creado

    def dar_de_baja(self, codigo_recurso: str, req: DarDeBajaRequest):
        bib = self.usuario_repo.obtener_por_identificacion_o_codigo(req.identificacion_bibliotecario)
        if not bib or bib.rol != RolUsuario.BIBLIOTECARIO:
            raise HTTPException(status_code=403, detail="Solo un bibliotecario puede dar de baja un recurso")
        recurso = self.recurso_repo.obtener_por_codigo(codigo_recurso)
        if not recurso:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        baja = self.recurso_repo.dar_de_baja(recurso, req.identificacion_bibliotecario, req.motivo)
        self.auditoria_repo.registrar_evento(
            accion="RECURSO_BORRADO_LOGICO",
            entidad="Recurso",
            entidad_codigo=codigo_recurso,
            usuario_actor=req.identificacion_bibliotecario,
            detalle=f"Baja lógica de recurso ({req.motivo})",
        )
        return baja
