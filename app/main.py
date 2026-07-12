from fastapi import FastAPI

from app.core.config import settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)
@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}"
    }