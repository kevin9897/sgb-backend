# SGB Backend – Universidad de Madeira

API REST del Sistema de Gestión Bibliotecaria (Python + FastAPI + SQLAlchemy + PostgreSQL).

Forma parte del proyecto principal: https://github.com/kevin9897/desarrollo_Software_II

## Estructura
```
app/
  main.py        punto de entrada FastAPI (CORS, routers, creación de tablas)
  config.py      variables de entorno
  database.py    conexión a PostgreSQL
  security.py    login / JWT / roles
  constants.py   días de préstamo, renovaciones máximas, tarifas de multa
  jobs.py        tareas automáticas (perdidos >120 días, vencer reservas, multas)
  utils.py       días hábiles y fechas
  models/        tablas de la BD
  schemas/       validación Pydantic
  services/      reglas de negocio
  routers/       endpoints /api/v1/...
seed.py          datos iniciales
tests/           pruebas
render.yaml      despliegue en Render (API + PostgreSQL)
```

## Ejecutar
Lo recomendado es levantarlo desde el repositorio principal con `docker compose up --build`.

Solo el backend, con Docker:
```bash
cp .env.example .env     # ajustar DATABASE_URL a una BD accesible
docker build -t sgb-backend .
docker run -p 8000:8000 --env-file .env sgb-backend
```
Swagger: http://localhost:8000/docs

## Despliegue
Render → New → Blueprint → seleccionar este repositorio (usa `render.yaml`).
