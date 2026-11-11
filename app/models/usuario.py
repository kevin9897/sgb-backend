"""Modelos de Usuario con Borrado Lógico y Auditoría (DDSI-16 / HT-02)."""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from app.constants import RolUsuario
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    identificacion = Column(String(30), unique=True, nullable=False, index=True)
    codigo = Column(String(30), unique=True, nullable=True, index=True)  # Solo estudiante
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    plan = Column(String(100), nullable=True)
    semestre = Column(Integer, nullable=True)
    rol = Column(Enum(RolUsuario), nullable=False)

    # Borrado lógico y metadatos de auditoría (HT-02)
    eliminado = Column(Boolean, default=False, nullable=False, index=True)
    fecha_eliminacion = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
