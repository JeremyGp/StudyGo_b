from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Tarea(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_limite = Column(DateTime)
    id_estado = Column(Integer, ForeignKey("estados.id_estado"))
    id_prioridad = Column(Integer, ForeignKey("prioridades.id_prioridad"))
    id_creador = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_responsable = Column(Integer, ForeignKey("usuarios.id"))
    id_proyecto = Column(Integer, ForeignKey("proyectos.id_proyecto"))
    id_tarea_padre = Column(Integer, ForeignKey("tareas.id_tarea"))
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    estado = relationship("Estado", back_populates="tareas")
    prioridad = relationship("Prioridad", back_populates="tareas")
    creador = relationship("Usuario", foreign_keys=[id_creador], back_populates="tareas_creadas")
    responsable = relationship("Usuario", foreign_keys=[id_responsable], back_populates="tareas_asignadas")
    proyecto = relationship("Proyecto", back_populates="tareas")
    subtareas = relationship("Tarea", backref="tarea_padre", remote_side=[id_tarea])
    comentarios = relationship("Comentario", back_populates="tarea")
    notificaciones = relationship("Notificacion", back_populates="tarea")