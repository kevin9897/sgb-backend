"""Controlador HTTP (Router) para Cálculo Automático de Multas y Pago Simulado (DDSI-5 / HU0002)."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.multa import MultaOut, MultaSimuladaCreate, PagoSimuladoRequest
from app.services.multa_service import MultaService

router = APIRouter(prefix="/multas", tags=["Multas y Pago Simulado"])


@router.get("", response_model=list[MultaOut])
def listar_multas(identificacion_usuario: Optional[str] = None, db: Session = Depends(get_db)):
    return MultaService(db).listar_multas(identificacion_usuario=identificacion_usuario)


@router.post("/calcular", response_model=MultaOut)
def calcular_y_registrar_multa(data: MultaSimuladaCreate, db: Session = Depends(get_db)):
    return MultaService(db).generar_multa_automatica(data)


@router.post("/{multa_id}/pagar", response_model=MultaOut)
def pagar_multa(
    multa_id: int,
    req: Optional[PagoSimuladoRequest] = None,
    db: Session = Depends(get_db),
):
    metodo = req.metodo_pago if req else "PSE_SIMULADO"
    return MultaService(db).pagar_multa(multa_id, metodo_pago=metodo)
