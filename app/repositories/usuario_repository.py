"""Capa de Persistencia (Repositorio/DAO) para Usuarios con Borrado Lógico (DDSI-16)."""
from datetime import datetime
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(
        self,
        rol: Optional[str] = None,
        q: Optional[str] = None,
        incluir_eliminados: bool = False,
    ) -> list[Usuario]:
        query = self.db.query(Usuario)
        if not incluir_eliminados:
            query = query.filter(Usuario.eliminado.is_(False))
        if rol:
            query = query.filter(Usuario.rol == rol)
        if q:
            like = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Usuario.identificacion.ilike(like),
                    Usuario.codigo.ilike(like),
                    Usuario.nombres.ilike(like),
                    Usuario.apellidos.ilike(like),
                    Usuario.correo_institucional.ilike(like),
                )
            )
        return query.order_by(Usuario.id).all()

    def obtener_por_identificacion_o_codigo(self, identificador: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(
                Usuario.eliminado.is_(False),
                or_(Usuario.identificacion == identificador, Usuario.codigo == identificador),
            )
            .first()
        )

    def crear(self, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(**data.model_dump(), eliminado=False)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def borrado_logico(self, usuario: Usuario) -> Usuario:
        usuario.eliminado = True
        usuario.fecha_eliminacion = datetime.utcnow()
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
