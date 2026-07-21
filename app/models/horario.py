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

    def __init__(self, **kwargs):
        try:
            # Se valida el contenido del horario al instanciarlo para prevenir errores de negocio
            # y facilitar la identificación de datos incorrectos antes del guardado.
            allowed_fields = {"id_horario", "dia_semana", "hora_inicio", "hora_fin", "aula", "id_asignatura"}
            invalid_fields = set(kwargs) - allowed_fields
            if invalid_fields:
                raise ValueError(f"Campos no permitidos para Horario: {sorted(invalid_fields)}")
            super().__init__(**kwargs)
        except ValueError as exc:
            raise ValueError(f"Error al inicializar Horario: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar Horario: {exc}") from exc