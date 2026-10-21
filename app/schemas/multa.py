from pydantic import BaseModel, ConfigDict


class MultaOut(BaseModel):
    id: int
    codigo_prestamo: str
    codigo_recurso: str
    identificacion_usuario: str
    dias_multa: int
    valor_cop: int
    pagada: bool
    model_config = ConfigDict(from_attributes=True)
