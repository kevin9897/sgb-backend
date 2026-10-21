"""Capa de Lógica de Negocio (Service) para Recursos Bibliográficos."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import RolUsuario
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.recurso import DarDeBajaRequest, RecursoCreate


class RecursoService:
    def __init__(self, db: Session):
        self.recurso_repo = RecursoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def listar_recursos(self, coleccion: Optional[str] = None, estado: Optional[str] = None):
        return self.recurso_repo.listar(coleccion=coleccion, estado=estado)

    def crear_recurso(self, data: RecursoCreate):
        if self.recurso_repo.obtener_por_codigo(data.codigo_recurso):
            raise HTTPException(status_code=400, detail="El código de recurso ya existe")
        return self.recurso_repo.crear(data)

    def dar_de_baja(self, codigo_recurso: str, req: DarDeBajaRequest):
        bib = self.usuario_repo.obtener_por_identificacion_o_codigo(req.identificacion_bibliotecario)
        if not bib or bib.rol != RolUsuario.BIBLIOTECARIO:
            raise HTTPException(status_code=403, detail="Solo un bibliotecario puede dar de baja un recurso")
        recurso = self.recurso_repo.obtener_por_codigo(codigo_recurso)
        if not recurso:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        return self.recurso_repo.dar_de_baja(recurso, req.identificacion_bibliotecario, req.motivo)
