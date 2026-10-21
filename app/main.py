"""Punto de entrada de la API del Sistema de Gestión Bibliotecaria."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401
from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
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
    description="API N-Tier (Controladores -> Servicios -> Repositorios/DAO -> PostgreSQL)",
    version="1.0.0",
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
    """Verifica que la API y la base de datos respondan."""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "conectada"}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(recursos.router, prefix="/api/v1")
app.include_router(prestamos.router, prefix="/api/v1")
app.include_router(reservas.router, prefix="/api/v1")
app.include_router(multas.router, prefix="/api/v1")
