"""Capa de Lógica de Negocio (Service) para Usuarios y Autenticación."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar_usuarios(self, rol: Optional[str] = None):
        return self.repo.listar(rol=rol)

    def crear_usuario(self, data: UsuarioCreate):
        if self.repo.obtener_por_identificacion_o_codigo(data.identificacion):
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        return self.repo.crear(data)

    def autenticar(self, identificador: str):
        usuario = self.repo.obtener_por_identificacion_o_codigo(identificador)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
