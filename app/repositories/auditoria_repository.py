"""Capa de Persistencia (Repositorio/DAO) para el Esquema de Auditoría (DDSI-16 / HT-02)."""
from sqlalchemy.orm import Session
from app.models.auditoria import AuditoriaLog
from app.utils import generar_codigo_institucional


class AuditoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def registrar_evento(
        self,
        accion: str,
        entidad: str,
        entidad_codigo: str,
        usuario_actor: str,
        detalle: str,
    ) -> AuditoriaLog:
        evento = AuditoriaLog(
            codigo_evento=generar_codigo_institucional("AUD"),
            accion=accion,
            entidad=entidad,
            entidad_codigo=entidad_codigo,
            usuario_actor=usuario_actor,
            detalle=detalle,
        )
        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)
        return evento

    def listar(self, limite: int = 100) -> list[AuditoriaLog]:
        return (
            self.db.query(AuditoriaLog)
            .order_by(AuditoriaLog.id.desc())
            .limit(limite)
            .all()
        )
