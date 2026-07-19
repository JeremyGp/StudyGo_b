from sqlalchemy import Column, Integer, String, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.enums import DiasSemana


class Horario(Base):
    __tablename__ = "horarios"

    id_horario = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(Enum(DiasSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    aula = Column(String(50), nullable=False)
    id_asignatura = Column(Integer, ForeignKey("asignaturas.id_asignatura"))

    asignatura = relationship("Asignatura", back_populates="horarios")