from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Asignatura(Base):
    __tablename__ = "asignaturas"

    id_asignatura = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    ciclo = Column(String(20), nullable=False)
    docente = Column(String(100), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), index=False)

    #Relaciones
    usuario = relationship("Usuario", back_populates="asignaturas")
    tareas = relationship("Tarea", back_populates="asignatura")
    horarios = relationship("Horario", back_populates="asignatura")
