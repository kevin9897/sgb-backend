"""Controlador HTTP (Router) para Recursos Bibliográficos."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recurso import DarDeBajaRequest, RecursoCreate, RecursoOut
from app.services.recurso_service import RecursoService

router = APIRouter(prefix="/recursos", tags=["Recursos Bibliográficos"])


@router.get("", response_model=list[RecursoOut])
def listar_recursos(
    coleccion: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return RecursoService(db).listar_recursos(coleccion=coleccion, estado=estado)


@router.post("", response_model=RecursoOut)
def crear_recurso(data: RecursoCreate, db: Session = Depends(get_db)):
    return RecursoService(db).crear_recurso(data)


@router.post("/{codigo_recurso}/baja", response_model=RecursoOut)
def dar_de_baja(codigo_recurso: str, req: DarDeBajaRequest, db: Session = Depends(get_db)):
    return RecursoService(db).dar_de_baja(codigo_recurso, req)
