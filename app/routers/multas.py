"""Controlador HTTP (Router) para Multas."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.multa import MultaOut
from app.services.multa_service import MultaService

router = APIRouter(prefix="/multas", tags=["Multas"])


@router.get("", response_model=list[MultaOut])
def listar_multas(identificacion_usuario: Optional[str] = None, db: Session = Depends(get_db)):
    return MultaService(db).listar_multas(identificacion_usuario=identificacion_usuario)


@router.post("/{multa_id}/pagar", response_model=MultaOut)
def pagar_multa(multa_id: int, db: Session = Depends(get_db)):
    return MultaService(db).pagar_multa(multa_id)
