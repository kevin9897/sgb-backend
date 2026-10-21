"""Controlador HTTP (Router) para Préstamos y Renovaciones."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.jobs import ejecutar_tareas_automaticas
from app.repositories.prestamo_repository import PrestamoRepository
from app.schemas.prestamo import (
    PrestamoCreate,
    PrestamoOut,
    RenovacionCreate,
    RenovacionOut,
)
from app.services.prestamo_service import PrestamoService

router = APIRouter(prefix="/prestamos", tags=["Préstamos y Renovaciones"])


@router.get("", response_model=list[PrestamoOut])
def listar_prestamos(solo_activos: bool = False, db: Session = Depends(get_db)):
    return PrestamoService(db).listar_prestamos(solo_activos=solo_activos)


@router.get("/renovaciones", response_model=list[RenovacionOut])
def listar_renovaciones(db: Session = Depends(get_db)):
    return PrestamoRepository(db).listar_renovaciones()


@router.post("", response_model=PrestamoOut)
def crear_prestamo(data: PrestamoCreate, db: Session = Depends(get_db)):
    return PrestamoService(db).registrar_prestamo(data)


@router.post("/renovar", response_model=RenovacionOut)
def renovar_prestamo(data: RenovacionCreate, db: Session = Depends(get_db)):
    return PrestamoService(db).renovar_prestamo(data)


@router.post("/{codigo_prestamo}/devolver", response_model=PrestamoOut)
def devolver_prestamo(codigo_prestamo: str, db: Session = Depends(get_db)):
    return PrestamoService(db).devolver_prestamo(codigo_prestamo)


@router.post("/ejecutar-jobs")
def correr_jobs(db: Session = Depends(get_db)):
    return ejecutar_tareas_automaticas(db)
