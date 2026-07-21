from datetime import datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.enums import EstadoTarea
from app.models.notificacion import Notificacion
from app.models.tarea import Tarea
from app.repository import notificacion as notificacion_repository
from app.repository import tarea as tarea_repository
from app.schemas.notificacion import (
    NotificacionCreate,
    NotificacionUpdate
)


TIPO_RECORDATORIO_FECHA_LIMITE = "recordatorio_fecha_limite"
TIPO_RECORDATORIO_PROXIMA = "recordatorio_proxima_entrega"
TIPO_RECORDATORIO_VENCIDA = "recordatorio_tarea_vencida"


def crear_notificacion(db: Session,datos: NotificacionCreate,id_usuario: int,id_tarea: int | None = None) -> Notificacion:
    """Crea una nueva notificación."""

    nueva_notificacion = Notificacion(
        mensaje=datos.mensaje,
        tipo=datos.tipo,
        fecha_programada=datos.fecha_programada,
        es_leido=False,
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


def marcar_como_leida(db: Session,id_notificacion: int) -> Notificacion | None:
    """Marca una notificación como leída."""

    notificacion = notificacion_repository.obtener_por_id(db,id_notificacion)

    if notificacion is None:
        return None

    notificacion.es_leido = True
    db.commit()
    db.refresh(notificacion)

    return notificacion


def eliminar_notificacion(db: Session,id_notificacion: int) -> bool:

    notificacion = notificacion_repository.obtener_por_id(db,id_notificacion)

    if notificacion is None:
        return False

    notificacion_repository.eliminar(db,notificacion)

    return True


def generar_recordatorios_tarea(db: Session,id_tarea: int) -> list[Notificacion]:
    """Genera recordatorios automáticos para una tarea."""

    tarea = tarea_repository.obtener_por_id(db,id_tarea)

    if tarea is None:
        raise ValueError("Tarea no encontrada.")

    if tarea.fecha_limite is None:
        raise ValueError("La tarea debe tener una fecha límite.")

    if tarea.asignatura is None:
        raise ValueError("La tarea debe pertenecer a una asignatura.")

    id_usuario = tarea.asignatura.id_usuario
    ahora = datetime.now()
    recordatorios = []

    recordatorio_previo = crear_recordatorio_antes_fecha_limite(
        db,
        tarea,
        id_usuario
    )

    if recordatorio_previo is not None:
        recordatorios.append(recordatorio_previo)

    if tarea.estado != EstadoTarea.COMPLETADA:
        if ahora <= tarea.fecha_limite <= ahora + timedelta(days=1):
            recordatorio_proximo = crear_recordatorio_proxima_a_vencer(
                db,
                tarea,
                id_usuario
            )

            if recordatorio_proximo is not None:
                recordatorios.append(recordatorio_proximo)

        if tarea.fecha_limite < ahora:
            recordatorio_vencido = crear_recordatorio_tarea_vencida(
                db,
                tarea,
                id_usuario
            )

            if recordatorio_vencido is not None:
                recordatorios.append(recordatorio_vencido)

    return recordatorios


def crear_recordatorio_antes_fecha_limite(
    db: Session,
    tarea: Tarea,
    id_usuario: int
) -> Notificacion | None:
    """Crea un recordatorio un día antes de la fecha límite."""

    fecha_programada = tarea.fecha_limite - timedelta(days=1)

    if fecha_programada < datetime.now():
        fecha_programada = datetime.combine(
            datetime.now().date(),
            time(9, 0)
        )

    mensaje = f"La tarea '{tarea.titulo}' vence pronto. Revisa tu avance."

    return crear_recordatorio_si_no_existe(
        db,
        mensaje,
        TIPO_RECORDATORIO_FECHA_LIMITE,
        fecha_programada,
        id_usuario,
        tarea.id_tarea
    )


def crear_recordatorio_proxima_a_vencer(
    db: Session,
    tarea: Tarea,
    id_usuario: int
) -> Notificacion | None:
    """Crea una notificación cuando una tarea está próxima a vencer."""

    fecha_programada = datetime.now()
    mensaje = f"La tarea '{tarea.titulo}' está próxima a vencer."

    return crear_recordatorio_si_no_existe(
        db,
        mensaje,
        TIPO_RECORDATORIO_PROXIMA,
        fecha_programada,
        id_usuario,
        tarea.id_tarea
    )


def crear_recordatorio_tarea_vencida(
    db: Session,
    tarea: Tarea,
    id_usuario: int
) -> Notificacion | None:
    """Crea una notificación cuando una tarea ya está vencida."""

    fecha_programada = datetime.now()
    mensaje = f"La tarea '{tarea.titulo}' está vencida."

    return crear_recordatorio_si_no_existe(
        db,
        mensaje,
        TIPO_RECORDATORIO_VENCIDA,
        fecha_programada,
        id_usuario,
        tarea.id_tarea
    )


def crear_recordatorio_si_no_existe(
    db: Session,
    mensaje: str,
    tipo: str,
    fecha_programada: datetime,
    id_usuario: int,
    id_tarea: int
) -> Notificacion | None:
    """Crea una notificación evitando duplicados por tarea, tipo y fecha."""

    if existe_recordatorio(
        db,
        id_usuario,
        id_tarea,
        tipo,
        fecha_programada
    ):
        return None

    notificacion = Notificacion(
        mensaje=mensaje,
        tipo=tipo,
        fecha_programada=fecha_programada,
        es_leido=False,
        id_usuario=id_usuario,
        id_tarea=id_tarea
    )

    return notificacion_repository.crear(db,notificacion)


def existe_recordatorio(
    db: Session,
    id_usuario: int,
    id_tarea: int,
    tipo: str,
    fecha_programada: datetime
) -> bool:
    """Verifica si ya existe un recordatorio equivalente."""

    notificaciones = notificacion_repository.listar_por_usuario(db,id_usuario)
    fecha_objetivo = fecha_programada.date()

    return any(
        notificacion.id_tarea == id_tarea
        and notificacion.tipo == tipo
        and notificacion.fecha_programada is not None
        and notificacion.fecha_programada.date() == fecha_objetivo
        for notificacion in notificaciones
    )
