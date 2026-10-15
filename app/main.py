"""Punto de entrada de la API del Sistema de Gestión Bibliotecaria."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401  (registra los modelos antes de crear las tablas)
from app.config import settings
from app.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas que no existan al arrancar
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SGB - Universidad de Madeira",
    description="API del Sistema de Gestión Bibliotecaria",
    version="0.1.0",
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

# Aquí se registrarán los routers, p. ej.:
# from app.routers import prestamos
# app.include_router(prestamos.router, prefix="/api/v1")
