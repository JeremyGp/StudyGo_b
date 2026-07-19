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