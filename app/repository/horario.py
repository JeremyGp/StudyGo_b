from sqlalchemy.orm import Session

from app.models.horario import Horario
from app.schemas.horario import HorarioUpdate


def obtener_por_id(db: Session, id_horario: int):
    return db.query(Horario).filter(
        Horario.id_horario == id_horario
    ).first()


def listar_por_asignatura(db: Session, id_asignatura: int):
    return db.query(Horario).filter(
        Horario.id_asignatura == id_asignatura
    ).all()


def crear(db: Session, horario: Horario):
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario


def actualizar(db: Session, horario: Horario, datos: HorarioUpdate):
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(horario, campo, valor)

    db.commit()
    db.refresh(horario)
    return horario


def eliminar(db: Session, horario: Horario):
    db.delete(horario)
    db.commit()