from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id_proyecto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)
    id_creador = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    creador = relationship("Usuario", back_populates="proyectos_creados")
    tareas = relationship("Tarea", back_populates="proyecto")