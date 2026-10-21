from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.constants import EstadoRecurso, TipoColeccion


class RecursoCreate(BaseModel):
    codigo_recurso: str
    coleccion: TipoColeccion
    titulo: str
    isbn_issn: Optional[str] = None
    resumen_descripcion: Optional[str] = None
    autores: Optional[str] = None
    editorial: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    volumen: Optional[str] = None
    numero_edicion: Optional[str] = None
    idioma: Optional[str] = None
    numero_paginas: Optional[int] = None
    ancho: Optional[float] = None
    alto: Optional[float] = None
    profundidad: Optional[float] = None
    unidad_dimension: Optional[str] = None
    tipo_encuadernacion: Optional[str] = None
    periodicidad: Optional[str] = None
    formato_mapa: Optional[str] = None
    numero_equipo: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    cargador: Optional[str] = None
    funda: Optional[str] = None
    cantidad_ejemplares: int = 1


class DarDeBajaRequest(BaseModel):
    identificacion_bibliotecario: str
    motivo: str


class RecursoOut(RecursoCreate):
    id: int
    estado: EstadoRecurso
    motivo_baja: Optional[str] = None
    bibliotecario_baja_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
