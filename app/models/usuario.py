from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())
    estado = Column(Boolean, default=True)

    # Relaciones
    asignaturas = relationship("Asignatura", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario")

    def __init__(self, **kwargs):
        try:
            # Valida que solo se usen atributos definidos para evitar errores de configuración
            # en la construcción del modelo y facilitar la detección temprana de problemas.
            allowed_fields = {"id_usuario", "nombre", "correo", "contrasena_hash", "fecha_registro", "estado"}
            invalid_fields = set(kwargs) - allowed_fields
            if invalid_fields:
                raise ValueError(f"Campos no permitidos para Usuario: {sorted(invalid_fields)}")
            super().__init__(**kwargs)
        except ValueError as exc:
            raise ValueError(f"Error al inicializar Usuario: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar Usuario: {exc}") from exc