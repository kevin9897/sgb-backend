"""Controlador HTTP (Router) para Reservas."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.prestamo import ReservaCreate, ReservaOut
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("", response_model=list[ReservaOut])
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService(db).listar_reservas()


@router.post("", response_model=ReservaOut)
def crear_reserva(data: ReservaCreate, db: Session = Depends(get_db)):
    return ReservaService(db).crear_reserva(data)
