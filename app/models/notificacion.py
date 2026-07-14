# notificacion.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id_notificacion = Column(Integer, primary_key=True, index=True)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50))
    fecha_programada = Column(DateTime)
    leido = Column(Boolean, default=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"))
    fecha_creacion = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="notificaciones")
    tarea = relationship("Tarea", back_populates="notificaciones")