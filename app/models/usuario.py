from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)

    # Relaciones
    tareas_creadas = relationship("Tarea", foreign_keys="Tarea.id_creador", back_populates="creador")
    tareas_asignadas = relationship("Tarea", foreign_keys="Tarea.id_responsable", back_populates="responsable")
    proyectos_creados = relationship("Proyecto", back_populates="creador")
    comentarios = relationship("Comentario", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario")