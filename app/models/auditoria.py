"""Modelo de Esquema de Auditoría (DDSI-16 / HT-02)."""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from app.database import Base


class AuditoriaLog(Base):
    __tablename__ = "auditoria_logs"

    id = Column(Integer, primary_key=True, index=True)
    codigo_evento = Column(String(40), unique=True, nullable=False, index=True)
    accion = Column(String(60), nullable=False, index=True)
    entidad = Column(String(50), nullable=False, index=True)
    entidad_codigo = Column(String(60), nullable=False)
    usuario_actor = Column(String(50), nullable=False)
    detalle = Column(Text, nullable=False)
    fecha_evento = Column(DateTime, default=datetime.utcnow, nullable=False)
