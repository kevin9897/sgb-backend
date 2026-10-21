"""Exportación central de Repositorios/DAO (Capa de Persistencia)."""
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.multa_repository import MultaRepository

__all__ = ["UsuarioRepository", "RecursoRepository", "PrestamoRepository", "MultaRepository"]
