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