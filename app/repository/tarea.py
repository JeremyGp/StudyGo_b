from sqlalchemy.orm import Session

from app.models.tarea import Tarea
from app.schemas.tarea import TareaUpdate


def obtener_por_id(db: Session, id_tarea: int):
    return db.query(Tarea).filter(
        Tarea.id_tarea == id_tarea
    ).first()


def listar_por_asignatura(db: Session, id_asignatura: int):
    return db.query(Tarea).filter(
        Tarea.id_asignatura == id_asignatura
    ).all()


def crear(db: Session, tarea: Tarea):
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


def actualizar(db: Session, tarea: Tarea, datos: TareaUpdate):
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)

    db.commit()
    db.refresh(tarea)
    return tarea


def eliminar(db: Session, tarea: Tarea):
    db.delete(tarea)
    db.commit()