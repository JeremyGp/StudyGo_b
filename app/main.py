from fastapi import FastAPI

import app.models

from app.database.base import Base
from app.database.database import engine
from app.core.config import settings

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)
@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}"
    }