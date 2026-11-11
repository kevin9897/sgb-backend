"""Capa de Lógica de Negocio (Service) para Cálculo Automático de Multas y Pago Simulado (DDSI-5 / HU0002)."""
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import calcular_valor_multa
from app.models.multa import Multa
from app.repositories.auditoria_repository import AuditoriaRepository
from app.repositories.multa_repository import MultaRepository
from app.schemas.multa import MultaSimuladaCreate
from app.utils import generar_codigo_institucional


class MultaService:
    def __init__(self, db: Session):
        self.multa_repo = MultaRepository(db)
        self.auditoria_repo = AuditoriaRepository(db)

    def listar_multas(self, identificacion_usuario: Optional[str] = None):
        return self.multa_repo.listar(identificacion_usuario)

    def generar_multa_automatica(self, data: MultaSimuladaCreate) -> Multa:
        if data.dias_habiles_atraso <= 0:
            raise HTTPException(status_code=400, detail="Los días hábiles de atraso deben ser mayores a 0")
        valor = calcular_valor_multa(data.dias_habiles_atraso)
        codigo_pr = generar_codigo_institucional("PR")
        multa = self.multa_repo.crear(
            Multa(
                codigo_prestamo=codigo_pr,
                codigo_recurso=data.codigo_recurso,
                identificacion_usuario=data.identificacion_usuario,
                dias_multa=data.dias_habiles_atraso,
                valor_cop=valor,
                pagada=False,
            )
        )
        self.auditoria_repo.registrar_evento(
            accion="MULTA_CALCULADA",
            entidad="Multa",
            entidad_codigo=codigo_pr,
            usuario_actor=data.identificacion_bibliotecario,
            detalle=f"Cálculo automático de multa ({data.dias_habiles_atraso} días hábiles): ${valor} COP a usuario {data.identificacion_usuario}",
        )
        return multa

    def pagar_multa(self, multa_id: int, metodo_pago: str = "PSE_SIMULADO"):
        multa = self.multa_repo.pagar(multa_id, metodo_pago=metodo_pago)
        if not multa:
            raise HTTPException(status_code=404, detail="Multa no encontrada")
        self.auditoria_repo.registrar_evento(
            accion="MULTA_PAGO_SIMULADO",
            entidad="Multa",
            entidad_codigo=multa.referencia_pago or str(multa.id),
            usuario_actor=multa.identificacion_usuario,
            detalle=f"Pago simulado vía {metodo_pago} por ${multa.valor_cop} COP (Ref: {multa.referencia_pago})",
        )
        return multa
