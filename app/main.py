from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import app.models

from app.database.base import Base
from app.database.database import engine
from app.core.config import settings
from app.core.logging import configure_logging
from app.routers import (usuario, asignatura, horario, tarea, notificacion,dashboard)

logger = configure_logging()

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    # Captura las excepciones HTTP lanzadas intencionalmente por la API,
    # registra el problema y devuelve un mensaje seguro al cliente.
    logger.warning("HTTP %s en %s: %s", exc.status_code, _request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    # Maneja errores de entrada de datos, como cuerpos mal formados o campos inválidos,
    # evitando exponer detalles técnicos al usuario final.
    logger.warning("Error de validación en %s: %s", _request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Los datos enviados no son válidos."},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_request: Request, exc: IntegrityError) -> JSONResponse:
    # Captura errores de integridad de la base de datos, como violaciones de restricciones,
    # y los registra para depuración sin mostrar detalles internos al cliente.
    logger.exception("Error de integridad en %s", _request.url.path)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "No se pudo completar la operación por un conflicto de datos."},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(_request: Request, exc: SQLAlchemyError) -> JSONResponse:
    # Centraliza los errores generales de SQLAlchemy para registrar el fallo de manera
    # consistente y responder al cliente con un mensaje genérico y seguro.
    logger.exception("Error de base de datos en %s", _request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error al procesar la solicitud."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    # Sirve como respaldo para cualquier error no previsto, garantizando que quede registrado
    # y que la respuesta al usuario sea controlada y no revele información sensible.
    logger.exception("Error inesperado en %s", _request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error inesperado en el servidor."},
    )


#CORS
# React con Vite
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:8080/","http://localhost:8080"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

#ROUTERS
app.include_router(usuario.router)
app.include_router(asignatura.router)
app.include_router(horario.router)
app.include_router(tarea.router)
app.include_router(notificacion.router)
app.include_router(dashboard.router)

#Ruta principal
@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}"
    }
