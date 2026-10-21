from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PrestamoCreate(BaseModel):
    identificacion_usuario: str
    codigo_recurso: str
    identificacion_bibliotecario: str


class PrestamoOut(BaseModel):
    id: int
    codigo_prestamo: str
    identificacion_usuario: str
    codigo_recurso: str
    fecha_hora_prestamo: datetime
    fecha_devolucion: datetime
    fecha_devolucion_real: Optional[datetime] = None
    identificacion_bibliotecario: str
    renovaciones_realizadas: int
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class ReservaCreate(BaseModel):
    identificacion_usuario: str
    codigo_recurso: str
    identificacion_bibliotecario: str


class ReservaOut(BaseModel):
    id: int
    identificacion_usuario: str
    codigo_recurso: str
    fecha_hora_reserva: datetime
    dias_restantes_prestamo: int
    identificacion_bibliotecario: str
    orden_cola: int
    activa: bool
    model_config = ConfigDict(from_attributes=True)


class RenovacionCreate(BaseModel):
    codigo_prestamo: str
    identificacion_bibliotecario: str


class RenovacionOut(BaseModel):
    id: int
    codigo_prestamo: str
    codigo_recurso: str
    identificacion_usuario: str
    identificacion_bibliotecario: str
    fecha_renovacion: datetime
    model_config = ConfigDict(from_attributes=True)
