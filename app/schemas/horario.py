from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import DiasSemana


class HorarioBase(BaseModel):
    dia_semana: DiasSemana
    hora_inicio: time
    hora_fin: time
    aula: str = Field(..., min_length=1, max_length=50)


class HorarioCreate(HorarioBase):
    """Datos que el cliente envía al crear un horario."""
    pass


class HorarioUpdate(BaseModel):
    """Todos los campos son opcionales."""
    dia_semana: Optional[DiasSemana] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    aula: Optional[str] = Field(None, min_length=1, max_length=50)


class HorarioOut(HorarioBase):
    """Datos que devuelve la API."""
    id_horario: int
    id_asignatura: int

    model_config = ConfigDict(from_attributes=True)