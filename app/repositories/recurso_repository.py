"""Capa de Persistencia (Repositorio/DAO) para Recursos Bibliográficos."""
from typing import Optional
from sqlalchemy.orm import Session
from app.constants import EstadoRecurso
from app.models.recurso import Recurso
from app.schemas.recurso import RecursoCreate


class RecursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, coleccion: Optional[str] = None, estado: Optional[str] = None) -> list[Recurso]:
        q = self.db.query(Recurso)
        if coleccion:
            q = q.filter(Recurso.coleccion == coleccion)
        if estado:
            q = q.filter(Recurso.estado == estado)
        return q.order_by(Recurso.id).all()

    def obtener_por_codigo(self, codigo_recurso: str) -> Optional[Recurso]:
        return self.db.query(Recurso).filter(Recurso.codigo_recurso == codigo_recurso).first()

    def crear(self, data: RecursoCreate) -> Recurso:
        recurso = Recurso(**data.model_dump(), estado=EstadoRecurso.DISPONIBLE)
        self.db.add(recurso)
        self.db.commit()
        self.db.refresh(recurso)
        return recurso

    def actualizar_estado(self, recurso: Recurso, nuevo_estado: EstadoRecurso) -> Recurso:
        recurso.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(recurso)
        return recurso

    def dar_de_baja(self, recurso: Recurso, bibliotecario_id: str, motivo: str) -> Recurso:
        recurso.estado = EstadoRecurso.DADO_DE_BAJA
        recurso.bibliotecario_baja_id = bibliotecario_id
        recurso.motivo_baja = motivo
        self.db.commit()
        self.db.refresh(recurso)
        return recurso
