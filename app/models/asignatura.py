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

    def __init__(self, **kwargs):
        try:
            # Evita construir instancias con atributos inválidos y facilita el seguimiento de errores
            # en el momento de crear objetos de negocio.
            allowed_fields = {"id_asignatura", "nombre", "descripcion", "ciclo", "docente", "id_usuario"}
            invalid_fields = set(kwargs) - allowed_fields
            if invalid_fields:
                raise ValueError(f"Campos no permitidos para Asignatura: {sorted(invalid_fields)}")
            super().__init__(**kwargs)
        except ValueError as exc:
            raise ValueError(f"Error al inicializar Asignatura: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar Asignatura: {exc}") from exc
