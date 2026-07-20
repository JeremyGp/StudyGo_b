from sqlalchemy.orm import Session

from app.models.notificacion import Notificacion
from app.repository import notificacion as notificacion_repository
from app.schemas.notificacion import (
    NotificacionCreate,
    NotificacionUpdate
)


def crear_notificacion(db: Session,datos: NotificacionCreate,id_usuario: int,id_tarea: int | None = None) -> Notificacion:
    """Crea una nueva notificación."""

    nueva_notificacion = Notificacion(
        mensaje=datos.mensaje,
        tipo=datos.tipo,
        fecha_programada=datos.fecha_programada,
        leido=False,
        id_usuario=id_usuario,
        id_tarea=id_tarea
    )

    return notificacion_repository.crear(db,nueva_notificacion)


def obtener_notificacion_por_id(db: Session,id_notificacion: int) -> Notificacion | None:

    return notificacion_repository.obtener_por_id(db,id_notificacion)


def listar_notificaciones(db: Session,id_usuario: int) -> list[Notificacion]:

    return notificacion_repository.listar_por_usuario(db,id_usuario)


def actualizar_notificacion(db: Session,id_notificacion: int,datos: NotificacionUpdate) -> Notificacion | None:

    notificacion = notificacion_repository.obtener_por_id(db,id_notificacion)

    if notificacion is None:
        return None

    return notificacion_repository.actualizar(db,notificacion,datos)


def eliminar_notificacion(db: Session,id_notificacion: int) -> bool:

    notificacion = notificacion_repository.obtener_por_id(db,id_notificacion)

    if notificacion is None:
        return False

    notificacion_repository.eliminar(db,notificacion)

    return True