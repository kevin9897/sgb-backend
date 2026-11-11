from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MultaSimuladaCreate(BaseModel):
    identificacion_usuario: str = "10000001"
    codigo_recurso: str = "GEN-001"
    dias_habiles_atraso: int = 3
    identificacion_bibliotecario: str = "30000001"


class PagoSimuladoRequest(BaseModel):
    metodo_pago: str = "PSE_SIMULADO"


class MultaOut(BaseModel):
    id: int
    codigo_prestamo: str
    codigo_recurso: str
    identificacion_usuario: str
    dias_multa: int
    valor_cop: int
    pagada: bool
    referencia_pago: Optional[str] = None
    metodo_pago: Optional[str] = None
    fecha_pago: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class AuditoriaOut(BaseModel):
    id: int
    codigo_evento: str
    accion: str
    entidad: str
    entidad_codigo: str
    usuario_actor: str
    detalle: str
    fecha_evento: datetime
    model_config = ConfigDict(from_attributes=True)
