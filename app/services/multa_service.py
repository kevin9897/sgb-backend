"""Capa de Lógica de Negocio (Service) para Multas."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.multa_repository import MultaRepository


class MultaService:
    def __init__(self, db: Session):
        self.multa_repo = MultaRepository(db)

    def listar_multas(self, identificacion_usuario: Optional[str] = None):
        return self.multa_repo.listar(identificacion_usuario)

    def pagar_multa(self, multa_id: int):
        multa = self.multa_repo.pagar(multa_id)
        if not multa:
            raise HTTPException(status_code=404, detail="Multa no encontrada")
        return multa
