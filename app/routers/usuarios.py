"""Controlador HTTP (Router) para Usuarios."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services.auth_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(rol: Optional[str] = None, db: Session = Depends(get_db)):
    return UsuarioService(db).listar_usuarios(rol=rol)


@router.post("", response_model=UsuarioOut)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService(db).crear_usuario(data)
