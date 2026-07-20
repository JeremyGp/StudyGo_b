from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models

from app.database.base import Base
from app.database.database import engine
from app.core.config import settings
from app.routers import (usuario,asignatura,horario,tarea,notificacion)

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

#CORS
# React con Vite
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:8080/",],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

#ROUTERS
app.include_router(usuario.router)
app.include_router(asignatura.router)
app.include_router(horario.router)
app.include_router(tarea.router)
app.include_router(notificacion.router)

#Ruta principal
@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}"
    }