"""Controlador HTTP (Router) para Usuarios y Borrado Lógico (DDSI-16)."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services.auth_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(
    rol: Optional[str] = None,
    q: Optional[str] = None,
    incluir_eliminados: bool = False,
    db: Session = Depends(get_db),
):
    return UsuarioService(db).listar_usuarios(
        rol=rol,
        q=q,
        incluir_eliminados=incluir_eliminados,
    )


@router.post("", response_model=UsuarioOut)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService(db).crear_usuario(data)


@router.delete("/{identificacion}", response_model=UsuarioOut)
def eliminar_usuario_logico(
    identificacion: str,
    bibliotecario_id: str = "30000001",
    db: Session = Depends(get_db),
):
    return UsuarioService(db).eliminar_logico(identificacion, bibliotecario_id=bibliotecario_id)
