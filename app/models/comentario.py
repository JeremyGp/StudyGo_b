# comentario.py
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Comentario(Base):
    __tablename__ = "comentarios"

    id_comentario = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=False)

    usuario = relationship("Usuario", back_populates="comentarios")
    tarea = relationship("Tarea", back_populates="comentarios")