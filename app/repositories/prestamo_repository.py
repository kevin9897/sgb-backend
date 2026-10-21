"""Capa de Persistencia (Repositorio/DAO) para Préstamos, Reservas y Renovaciones."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo, Renovacion, Reserva


class PrestamoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_prestamos(self, solo_activos: bool = False) -> list[Prestamo]:
        q = self.db.query(Prestamo)
        if solo_activos:
            q = q.filter(Prestamo.activo.is_(True))
        return q.order_by(Prestamo.id.desc()).all()

    def listar_renovaciones(self) -> list[Renovacion]:
        return self.db.query(Renovacion).order_by(Renovacion.id.desc()).all()

    def obtener_por_codigo(self, codigo_prestamo: str) -> Optional[Prestamo]:
        return self.db.query(Prestamo).filter(Prestamo.codigo_prestamo == codigo_prestamo).first()

    def guardar_prestamo(self, prestamo: Prestamo) -> Prestamo:
        self.db.add(prestamo)
        self.db.commit()
        self.db.refresh(prestamo)
        return prestamo

    def guardar_renovacion(self, renovacion: Renovacion) -> Renovacion:
        self.db.add(renovacion)
        self.db.commit()
        self.db.refresh(renovacion)
        return renovacion

    def listar_reservas_activas(self, codigo_recurso: Optional[str] = None) -> list[Reserva]:
        q = self.db.query(Reserva).filter(Reserva.activa.is_(True))
        if codigo_recurso:
            q = q.filter(Reserva.codigo_recurso == codigo_recurso)
        return q.order_by(Reserva.orden_cola.asc()).all()

    def guardar_reserva(self, reserva: Reserva) -> Reserva:
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
