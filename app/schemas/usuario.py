from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.constants import RolUsuario


class UsuarioBase(BaseModel):
    identificacion: str
    codigo: Optional[str] = None
    nombres: str
    apellidos: str
    correo_institucional: str
    plan: Optional[str] = None
    semestre: Optional[int] = None
    rol: RolUsuario


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioOut(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
