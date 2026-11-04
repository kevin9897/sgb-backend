"""Punto de entrada de la API del Sistema de Gestión Bibliotecaria (DDSI1-2, DDSI1-8)."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401
from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
from app.models.recurso import Recurso
from app.models.usuario import Usuario
from app.routers import auth, multas, prestamos, recursos, reservas, usuarios
from seed import poblar_base_de_datos


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        poblar_base_de_datos(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="SGB - Universidad de Madeira",
    description="API N-Tier (Controladores -> Servicios -> Repositorios/DAO -> Supabase PostgreSQL)",
    version="1.1.0",
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
        "usuarios_registrados": db.query(Usuario).count(),
        "recursos_registrados": db.query(Recurso).count(),
    }


@app.post("/api/v1/seed", tags=["Sistema"])
def ejecutar_seed(db: Session = Depends(get_db)):
    """Ejecuta o verifica la carga de datos semilla (DDSI1-8: Seed Data)."""
    poblar_base_de_datos(db)
    return {
        "mensaje": "Seed Data verificado en Supabase PostgreSQL",
        "usuarios": db.query(Usuario).count(),
        "recursos": db.query(Recurso).count(),
    }


app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(recursos.router, prefix="/api/v1")
app.include_router(prestamos.router, prefix="/api/v1")
app.include_router(reservas.router, prefix="/api/v1")
app.include_router(multas.router, prefix="/api/v1")
