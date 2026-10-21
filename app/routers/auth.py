"""Controlador HTTP (Router) para Autenticación."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioOut
from app.services.auth_service import UsuarioService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginRequest(BaseModel):
    identificador: str


@router.post("/login", response_model=UsuarioOut)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return UsuarioService(db).autenticar(req.identificador)
