from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())
    estado = Column(Boolean, default=True)

    # Relaciones
    asignaturas = relationship("Asignatura", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario")