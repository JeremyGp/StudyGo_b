from sqlalchemy.orm import Session

from app.models.asignatura import Asignatura
from app.schemas.asignatura import AsignaturaUpdate


def obtener_por_id(db: Session, id_asignatura: int):
    return db.query(Asignatura).filter(
        Asignatura.id_asignatura == id_asignatura
    ).first()


def listar_por_usuario(db: Session, id_usuario: int):
    return db.query(Asignatura).filter(
        Asignatura.id_usuario == id_usuario
    ).all()


def crear(db: Session, asignatura: Asignatura):
    db.add(asignatura)
    db.commit()
    db.refresh(asignatura)
    return asignatura


def actualizar(db: Session, asignatura: Asignatura, datos: AsignaturaUpdate):
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(asignatura, campo, valor)

    db.commit()
    db.refresh(asignatura)
    return asignatura


def eliminar(db: Session, asignatura: Asignatura):
    db.delete(asignatura)
    db.commit()