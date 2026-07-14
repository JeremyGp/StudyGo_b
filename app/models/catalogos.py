from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Estado(Base):
    __tablename__ = "estados"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30), nullable=False)

    tareas = relationship("Tarea", back_populates="estado")


class Prioridad(Base):
    __tablename__ = "prioridades"

    id_prioridad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), nullable=False)

    tareas = relationship("Tarea", back_populates="prioridad")