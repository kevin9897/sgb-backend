"""Capa de Lógica de Negocio (Service) para Usuarios y Borrado Lógico (DDSI-16)."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import RolUsuario
from app.repositories.auditoria_repository import AuditoriaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)
        self.auditoria_repo = AuditoriaRepository(db)

    def listar_usuarios(
        self,
        rol: Optional[str] = None,
        q: Optional[str] = None,
        incluir_eliminados: bool = False,
    ):
        return self.repo.listar(rol=rol, q=q, incluir_eliminados=incluir_eliminados)

    def crear_usuario(self, data: UsuarioCreate):
        if self.repo.obtener_por_identificacion_o_codigo(data.identificacion):
            raise HTTPException(status_code=400, detail="La identificación de usuario ya está registrada")
        if data.rol == RolUsuario.ESTUDIANTE and not data.codigo:
            raise HTTPException(status_code=400, detail="El código estudiantil es obligatorio para estudiantes")
        if data.rol != RolUsuario.ESTUDIANTE:
            data.codigo = None
        if data.codigo and self.repo.obtener_por_identificacion_o_codigo(data.codigo):
            raise HTTPException(status_code=400, detail="El código estudiantil ya está registrado")
        creado = self.repo.crear(data)
        self.auditoria_repo.registrar_evento(
            accion="USUARIO_CREADO",
            entidad="Usuario",
            entidad_codigo=creado.identificacion,
            usuario_actor="30000001",
            detalle=f"Registro de usuario {creado.nombres} {creado.apellidos} ({creado.rol.value})",
        )
        return creado

    def eliminar_logico(self, identificacion: str, bibliotecario_id: str = "30000001"):
        usuario = self.repo.obtener_por_identificacion_o_codigo(identificacion)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        eliminado = self.repo.borrado_logico(usuario)
        self.auditoria_repo.registrar_evento(
            accion="USUARIO_BORRADO_LOGICO",
            entidad="Usuario",
            entidad_codigo=identificacion,
            usuario_actor=bibliotecario_id,
            detalle=f"Borrado lógico de usuario {usuario.nombres} {usuario.apellidos}",
        )
        return eliminado

    def autenticar(self, identificador: str):
        usuario = self.repo.obtener_por_identificacion_o_codigo(identificador)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
