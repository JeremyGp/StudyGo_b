from sqlalchemy.orm import Session

from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionUpdate


def obtener_por_id(db: Session, id_notificacion: int):
    return db.query(Notificacion).filter(
        Notificacion.id_notificacion == id_notificacion
    ).first()


def listar_por_usuario(db: Session, id_usuario: int):
    return db.query(Notificacion).filter(
        Notificacion.id_usuario == id_usuario
    ).all()


def crear(db: Session, notificacion: Notificacion):
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    return notificacion


def actualizar(db: Session, notificacion: Notificacion, datos: NotificacionUpdate):
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(notificacion, campo, valor)

    db.commit()
    db.refresh(notificacion)
    return notificacion


def eliminar(db: Session, notificacion: Notificacion):
    db.delete(notificacion)
    db.commit()