"""Modelos de Recursos Bibliográficos para las 6 colecciones y sus ejemplares."""
from datetime import date
from sqlalchemy import Column, Date, Enum, Float, Integer, String, Text
from app.constants import EstadoRecurso, TipoColeccion
from app.database import Base


class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_recurso = Column(String(50), unique=True, nullable=False, index=True)
    coleccion = Column(Enum(TipoColeccion), nullable=False, index=True)
    estado = Column(Enum(EstadoRecurso), default=EstadoRecurso.DISPONIBLE, nullable=False, index=True)

    # Campos comunes y específicos según la colección
    titulo = Column(String(200), nullable=False)  # Título / Nombre del mapa / Marca-Modelo
    isbn_issn = Column(String(40), nullable=True)  # ISBN (libros/diccionarios) o ISSN (revistas)
    resumen_descripcion = Column(Text, nullable=True)
    autores = Column(String(200), nullable=True)
    editorial = Column(String(150), nullable=True)
    fecha_publicacion = Column(Date, nullable=True)
    volumen = Column(String(30), nullable=True)
    numero_edicion = Column(String(30), nullable=True)
    idioma = Column(String(50), nullable=True)
    numero_paginas = Column(Integer, nullable=True)

    # Dimensiones (cm para General/Reserva, pulgadas para Referencia)
    ancho = Column(Float, nullable=True)
    alto = Column(Float, nullable=True)
    profundidad = Column(Float, nullable=True)
    unidad_dimension = Column(String(15), nullable=True)  # 'cm' o 'pulgadas'
    tipo_encuadernacion = Column(String(30), nullable=True)  # 'Tapa blanda' o 'Tapa dura'

    # Hemeroteca
    periodicidad = Column(String(50), nullable=True)

    # Mapoteca
    formato_mapa = Column(String(20), nullable=True)  # jpg, pdf, shape, dwg

    # Tecnoteca (Laptops y Tabletas)
    numero_equipo = Column(String(50), nullable=True)
    marca = Column(String(80), nullable=True)
    modelo = Column(String(80), nullable=True)
    cargador = Column(String(80), nullable=True)
    funda = Column(String(80), nullable=True)

    cantidad_ejemplares = Column(Integer, default=1, nullable=False)
    motivo_baja = Column(Text, nullable=True)
    bibliotecario_baja_id = Column(String(30), nullable=True)
