"""Capa de Persistencia (Repositorio/DAO) para Multas."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.multa import Multa


class MultaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, identificacion_usuario: Optional[str] = None) -> list[Multa]:
        q = self.db.query(Multa)
        if identificacion_usuario:
            q = q.filter(Multa.identificacion_usuario == identificacion_usuario)
        return q.order_by(Multa.id.desc()).all()

    def tiene_multas_pendientes(self, identificacion_usuario: str) -> bool:
        return (
            self.db.query(Multa)
            .filter(Multa.identificacion_usuario == identificacion_usuario, Multa.pagada.is_(False))
            .first()
            is not None
        )

    def crear(self, multa: Multa) -> Multa:
        self.db.add(multa)
        self.db.commit()
        self.db.refresh(multa)
        return multa

    def pagar(self, multa_id: int) -> Optional[Multa]:
        multa = self.db.query(Multa).filter(Multa.id == multa_id).first()
        if multa:
            multa.pagada = True
            self.db.commit()
            self.db.refresh(multa)
        return multa
