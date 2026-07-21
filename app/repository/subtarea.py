from sqlalchemy.orm import Session

from app.models.subtarea import Subtarea
from app.schemas.subtarea import SubtareaUpdate


def obtener_por_id(db: Session, id_subtarea: int):
    return db.query(Subtarea).filter(
        Subtarea.id_subtarea == id_subtarea
    ).first()


def listar_por_tarea(db: Session, id_tarea: int):
    return db.query(Subtarea).filter(
        Subtarea.id_tarea == id_tarea
    ).all()


def crear(db: Session, subtarea: Subtarea):
    db.add(subtarea)
    db.commit()
    db.refresh(subtarea)
    return subtarea


def actualizar(db: Session, subtarea: Subtarea, datos: SubtareaUpdate):
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(subtarea, campo, valor)

    db.commit()
    db.refresh(subtarea)
    return subtarea


def eliminar(db: Session, subtarea: Subtarea):
    db.delete(subtarea)
    db.commit()