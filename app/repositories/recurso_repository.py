"""Capa de Persistencia (Repositorio/DAO) para Recursos Bibliográficos."""
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.constants import EstadoRecurso
from app.models.recurso import Recurso
from app.schemas.recurso import RecursoCreate


class RecursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(
        self,
        coleccion: Optional[str] = None,
        estado: Optional[str] = None,
        q: Optional[str] = None,
    ) -> list[Recurso]:
        query = self.db.query(Recurso)
        if coleccion:
            query = query.filter(Recurso.coleccion == coleccion)
        if estado:
            query = query.filter(Recurso.estado == estado)
        if q:
            like = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Recurso.codigo_recurso.ilike(like),
                    Recurso.titulo.ilike(like),
                    Recurso.autores.ilike(like),
                    Recurso.isbn_issn.ilike(like),
                )
            )
        return query.order_by(Recurso.id).all()

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
