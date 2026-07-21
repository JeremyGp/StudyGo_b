from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.enums import EstadoTarea
from app.database.base import Base

class Subtarea(Base):
    __tablename__ = "subtareas"

    id_subtarea = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    estado = Column(Enum(EstadoTarea), nullable=False)
    orden = Column(Integer)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), index=True)

    tarea = relationship("Tarea", back_populates="subtareas")

    def __init__(self, **kwargs):
        try:
            # Se controla la creación de subtareas para evitar enviar campos inesperados y detectar
            # errores de configuración antes de intentar guardar el registro.
            allowed_fields = {"id_subtarea", "titulo", "descripcion", "estado", "orden", "id_tarea"}
            invalid_fields = set(kwargs) - allowed_fields
            if invalid_fields:
                raise ValueError(f"Campos no permitidos para Subtarea: {sorted(invalid_fields)}")
            super().__init__(**kwargs)
        except ValueError as exc:
            raise ValueError(f"Error al inicializar Subtarea: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar Subtarea: {exc}") from exc