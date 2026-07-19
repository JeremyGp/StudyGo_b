from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AsignaturaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    ciclo: str = Field(..., max_length=20)
    docente: str = Field(..., min_length=2, max_length=100)


class AsignaturaCreate(AsignaturaBase):
    """Datos que el cliente envía al crear una asignatura."""
    pass


class AsignaturaUpdate(BaseModel):
    """Todos los campos son opcionales."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    ciclo: Optional[str] = Field(None, max_length=20)
    docente: Optional[str] = Field(None, min_length=2, max_length=100)


class AsignaturaOut(AsignaturaBase):
    """Datos que devuelve la API."""
    id_asignatura: int
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)