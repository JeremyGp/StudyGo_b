from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
from app.models.enums import EstadoTarea, PrioridadTarea


class Tarea(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_inicio = Column(DateTime)
    fecha_inicio_sugerida = Column(DateTime)
    fecha_limite = Column(DateTime)
    horas_estimadas = Column(Integer)
    estado = Column(Enum(EstadoTarea), nullable=False)
    prioridad = Column(Enum(PrioridadTarea), nullable=False)
    id_asignatura = Column(Integer, ForeignKey("asignaturas.id_asignatura"), index=True)

    #Relaciones
    asignatura = relationship("Asignatura", back_populates="tareas")
    subtareas = relationship("Subtarea", back_populates="tarea")
    notificaciones = relationship("Notificacion", back_populates="tarea")

    def __init__(self, **kwargs):
        try:
            # Se valida la estructura de los datos al crear la tarea para detectar errores de diseño
            # en etapas tempranas y evitar inconsistencias en la persistencia.
            allowed_fields = {"id_tarea", "titulo", "descripcion", "fecha_creacion", "fecha_inicio_sugerida", "fecha_limite", "horas_estimadas", "estado", "prioridad", "id_asignatura"}
            invalid_fields = set(kwargs) - allowed_fields
            if invalid_fields:
                raise ValueError(f"Campos no permitidos para Tarea: {sorted(invalid_fields)}")
            super().__init__(**kwargs)
        except ValueError as exc:
            raise ValueError(f"Error al inicializar Tarea: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar Tarea: {exc}") from exc