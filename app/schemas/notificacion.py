from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NotificacionBase(BaseModel):
    mensaje: str = Field(..., min_length=1)
    tipo: Optional[str] = Field(None, max_length=50)
    fecha_programada: datetime
    es_leido: bool = False


class NotificacionCreate(BaseModel):
    """Datos que el sistema envía al crear una notificación."""
    mensaje: str = Field(..., min_length=1)
    tipo: Optional[str] = Field(None, max_length=50)
    fecha_programada: datetime


class NotificacionUpdate(BaseModel):
    """Solo permite marcar la notificación como leída."""
    es_leido: Optional[bool] = None


class NotificacionOut(NotificacionBase):
    """Datos que devuelve la API."""
    id_notificacion: int
    id_usuario: int
    id_tarea: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)