"""Modelos de Préstamos, Reservas y Renovaciones."""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_prestamo = Column(String(40), unique=True, nullable=False, index=True)
    identificacion_usuario = Column(String(30), nullable=False, index=True)
    codigo_recurso = Column(String(50), nullable=False, index=True)
    fecha_hora_prestamo = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_devolucion = Column(DateTime, nullable=False)
    fecha_devolucion_real = Column(DateTime, nullable=True)
    identificacion_bibliotecario = Column(String(30), nullable=False)
    renovaciones_realizadas = Column(Integer, default=0, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    identificacion_usuario = Column(String(30), nullable=False, index=True)
    codigo_recurso = Column(String(50), nullable=False, index=True)
    fecha_hora_reserva = Column(DateTime, default=datetime.utcnow, nullable=False)
    dias_restantes_prestamo = Column(Integer, default=5, nullable=False)
    identificacion_bibliotecario = Column(String(30), nullable=False)
    orden_cola = Column(Integer, default=1, nullable=False)
    activa = Column(Boolean, default=True, nullable=False)


class Renovacion(Base):
    __tablename__ = "renovaciones"

    id = Column(Integer, primary_key=True, index=True)
    codigo_prestamo = Column(String(40), nullable=False, index=True)
    codigo_recurso = Column(String(50), nullable=False)
    identificacion_usuario = Column(String(30), nullable=False)
    identificacion_bibliotecario = Column(String(30), nullable=False)
    fecha_renovacion = Column(DateTime, default=datetime.utcnow, nullable=False)
