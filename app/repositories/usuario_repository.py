"""Capa de Persistencia (Repositorio/DAO) para Usuarios."""
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, rol: Optional[str] = None) -> list[Usuario]:
        q = self.db.query(Usuario)
        if rol:
            q = q.filter(Usuario.rol == rol)
        return q.order_by(Usuario.id).all()

    def obtener_por_identificacion_o_codigo(self, identificador: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(or_(Usuario.identificacion == identificador, Usuario.codigo == identificador))
            .first()
        )

    def crear(self, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(**data.model_dump())
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
