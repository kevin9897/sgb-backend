"""Punto de entrada de la API del Sistema de Gestión Bibliotecaria (Sprints 1, 2 y 3)."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401
from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
from app.models.auditoria import AuditoriaLog
from app.models.recurso import Recurso
from app.models.usuario import Usuario
from app.repositories.auditoria_repository import AuditoriaRepository
from app.routers import auth, multas, prestamos, recursos, reservas, usuarios
from app.schemas.multa import AuditoriaOut
from seed import poblar_base_de_datos


def asegurar_columnas_auditoria_y_borrado_logico(db: Session):
    """Asegura en PostgreSQL/Supabase las columnas de borrado lógico y pago simulado sin borrar datos previos."""
    sentencias = [
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS eliminado BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS fecha_eliminacion TIMESTAMP NULL",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE recursos ADD COLUMN IF NOT EXISTS eliminado BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE recursos ADD COLUMN IF NOT EXISTS fecha_eliminacion TIMESTAMP NULL",
        "ALTER TABLE recursos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE multas ADD COLUMN IF NOT EXISTS referencia_pago VARCHAR(50) NULL",
        "ALTER TABLE multas ADD COLUMN IF NOT EXISTS metodo_pago VARCHAR(40) NULL",
        "ALTER TABLE multas ADD COLUMN IF NOT EXISTS fecha_pago TIMESTAMP NULL",
    ]
    for sql in sentencias:
        try:
            db.execute(text(sql))
            db.commit()
        except Exception:
            db.rollback()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            asegurar_columnas_auditoria_y_borrado_logico(db)
            poblar_base_de_datos(db)
            if db.query(AuditoriaLog).count() == 0:
                AuditoriaRepository(db).registrar_evento(
                    accion="SISTEMA_INICIALIZADO",
                    entidad="Sistema",
                    entidad_codigo="SGB-MADEIRA",
                    usuario_actor="SYSTEM",
                    detalle="Esquema relacional, borrado lógico y auditoría activos en PostgreSQL",
                )
        finally:
            db.close()
    except Exception as exc:
        print(f"[WARN] Inicio diferido de BD: {exc}")
    yield


app = FastAPI(
    title="SGB - Universidad de Madeira",
    description="API N-Tier (Controladores -> Servicios -> Repositorios/DAO -> Supabase PostgreSQL)",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", tags=["Sistema"])
def health(db: Session = Depends(get_db)):
    """Verifica que la API y la base de datos en Supabase respondan."""
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "database": settings.db_provider,
        "usuarios_registrados": db.query(Usuario).filter(Usuario.eliminado.is_(False)).count(),
        "recursos_registrados": db.query(Recurso).filter(Recurso.eliminado.is_(False)).count(),
        "eventos_auditoria": db.query(AuditoriaLog).count(),
    }


@app.get("/api/v1/auditoria", response_model=list[AuditoriaOut], tags=["Auditoría (HT-02)"])
def listar_auditoria(db: Session = Depends(get_db)):
    """Lista la bitácora del esquema de auditoría (DDSI-16 / HT-02)."""
    return AuditoriaRepository(db).listar(limite=100)


@app.post("/api/v1/seed", tags=["Sistema"])
def ejecutar_seed(db: Session = Depends(get_db)):
    """Ejecuta o verifica la carga de datos semilla (DDSI1-8: Seed Data)."""
    poblar_base_de_datos(db)
    return {
        "mensaje": "Seed Data verificado en Supabase PostgreSQL",
        "usuarios": db.query(Usuario).filter(Usuario.eliminado.is_(False)).count(),
        "recursos": db.query(Recurso).filter(Recurso.eliminado.is_(False)).count(),
    }


app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(recursos.router, prefix="/api/v1")
app.include_router(prestamos.router, prefix="/api/v1")
app.include_router(reservas.router, prefix="/api/v1")
app.include_router(multas.router, prefix="/api/v1")
