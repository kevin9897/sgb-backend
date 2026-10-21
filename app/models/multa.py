"""Modelo de Multas."""
from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base


class Multa(Base):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True, index=True)
    codigo_prestamo = Column(String(40), nullable=False, index=True)
    codigo_recurso = Column(String(50), nullable=False)
    identificacion_usuario = Column(String(30), nullable=False, index=True)
    dias_multa = Column(Integer, nullable=False)
    valor_cop = Column(Integer, nullable=False)
    pagada = Column(Boolean, default=False, nullable=False)
