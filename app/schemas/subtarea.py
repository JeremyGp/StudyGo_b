from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import EstadoTarea


class SubtareaBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: Optional[str] = None
    estado: EstadoTarea
    orden: int = Field(..., ge=1)


class SubtareaCreate(BaseModel):
    """Datos que el cliente envía al crear una subtarea."""
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: Optional[str] = None
    orden: int = Field(..., ge=1)


class SubtareaUpdate(BaseModel):
    """Todos los campos son opcionales."""
    titulo: Optional[str] = Field(None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    estado: Optional[EstadoTarea] = None
    orden: Optional[int] = Field(None, ge=1)


class SubtareaOut(SubtareaBase):
    """Datos que devuelve la API."""
    id_subtarea: int
    id_tarea: int

    model_config = ConfigDict(from_attributes=True)