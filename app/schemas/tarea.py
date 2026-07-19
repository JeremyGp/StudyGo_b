from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import EstadoTarea, PrioridadTarea


class TareaBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_limite: datetime
    prioridad: PrioridadTarea
    estado: EstadoTarea
    horas_estimadas: int = Field(..., gt=0)

class TareaCreate(BaseModel):
    """Datos que el cliente envia al crea."""
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_limite: datetime
    prioridad: PrioridadTarea
    horas_estimadas: int = Field(..., gt=0)

class TareaUpdate(BaseModel):
    """Todos los campos son opcionales."""
    titulo: Optional[str] = Field(None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_limite: Optional[datetime] = None
    prioridad: Optional[PrioridadTarea] = None
    estado: Optional[EstadoTarea] = None
    horas_estimadas: Optional[int] = Field(None, gt=0)


class TareaOut(TareaBase):
    """Datos que devuelve la API."""
    id_tarea: int
    titulo: str =  Field(..., min_length=2, max_length=150)
    fecha_creacion: datetime
    fecha_inicio_sugerida: Optional[datetime] = None
    id_asignatura: int

    model_config = ConfigDict(from_attributes=True)