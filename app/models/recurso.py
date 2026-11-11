"""Modelos de Recursos Bibliográficos con Borrado Lógico y Auditoría (DDSI-16 / HT-02)."""
from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, Integer, String, Text
from app.constants import EstadoRecurso, TipoColeccion
from app.database import Base


class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_recurso = Column(String(50), unique=True, nullable=False, index=True)
    coleccion = Column(Enum(TipoColeccion), nullable=False, index=True)
    estado = Column(Enum(EstadoRecurso), default=EstadoRecurso.DISPONIBLE, nullable=False, index=True)

    titulo = Column(String(200), nullable=False)
    isbn_issn = Column(String(40), nullable=True)
    resumen_descripcion = Column(Text, nullable=True)
    autores = Column(String(200), nullable=True)
    editorial = Column(String(150), nullable=True)
    fecha_publicacion = Column(Date, nullable=True)
    volumen = Column(String(30), nullable=True)
    numero_edicion = Column(String(30), nullable=True)
    idioma = Column(String(50), nullable=True)
    numero_paginas = Column(Integer, nullable=True)

    ancho = Column(Float, nullable=True)
    alto = Column(Float, nullable=True)
    profundidad = Column(Float, nullable=True)
    unidad_dimension = Column(String(15), nullable=True)
    tipo_encuadernacion = Column(String(30), nullable=True)

    periodicidad = Column(String(50), nullable=True)
    formato_mapa = Column(String(20), nullable=True)

    numero_equipo = Column(String(50), nullable=True)
    marca = Column(String(80), nullable=True)
    modelo = Column(String(80), nullable=True)
    cargador = Column(String(80), nullable=True)
    funda = Column(String(80), nullable=True)

    cantidad_ejemplares = Column(Integer, default=1, nullable=False)
    motivo_baja = Column(Text, nullable=True)
    bibliotecario_baja_id = Column(String(30), nullable=True)

    # Borrado lógico y auditoría (HT-02)
    eliminado = Column(Boolean, default=False, nullable=False, index=True)
    fecha_eliminacion = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
