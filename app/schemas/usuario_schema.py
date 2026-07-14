from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr #valida automáticamente el formato del correo. Requiere el paquete email-validator#


class UsuarioCreate(UsuarioBase):
    """Datos que el cliente envía al registrarse."""
    contrasena: str = Field(..., min_length=8, max_length=100) #Es lo que llega del frontend#


class UsuarioUpdate(BaseModel):
    """Todos los campos opcionales: solo se actualiza lo que venga."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    estado: Optional[bool] = None


class UsuarioOut(UsuarioBase):
    """Lo que la API devuelve. Nunca incluye la contraseña."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    estado: bool

    model_config = ConfigDict(from_attributes=True) #  es lo que permite convertir directamente un objeto SQLAlchemy (Usuario del modelo) en un UsuarioOut, sin armar el diccionario a mano.#