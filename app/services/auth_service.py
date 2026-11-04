"""Capa de Lógica de Negocio (Service) para Usuarios y Autenticación (DDSI1-5, DDSI1-10)."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import RolUsuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar_usuarios(self, rol: Optional[str] = None, q: Optional[str] = None):
        return self.repo.listar(rol=rol, q=q)

    def crear_usuario(self, data: UsuarioCreate):
        if self.repo.obtener_por_identificacion_o_codigo(data.identificacion):
            raise HTTPException(status_code=400, detail="La identificación de usuario ya está registrada")
        if data.rol == RolUsuario.ESTUDIANTE and not data.codigo:
            raise HTTPException(status_code=400, detail="El código estudiantil es obligatorio para estudiantes")
        if data.rol != RolUsuario.ESTUDIANTE:
            data.codigo = None
        if data.codigo and self.repo.obtener_por_identificacion_o_codigo(data.codigo):
            raise HTTPException(status_code=400, detail="El código estudiantil ya está registrado")
        return self.repo.crear(data)

    def autenticar(self, identificador: str):
        usuario = self.repo.obtener_por_identificacion_o_codigo(identificador)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
