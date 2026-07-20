from app.models.enums import EstadoTarea
from sqlalchemy.orm import Session

from app.models.tarea import Tarea
from app.repository import tarea as tarea_repository
from app.schemas.tarea import TareaCreate, TareaUpdate


def crear_tarea(db: Session,datos: TareaCreate,id_asignatura: int) -> Tarea:
    """Crea una nueva tarea."""
    if datos.fecha_limite <= datos.fecha_inicio:
        raise ValueError(
            "La fecha límite debe ser posterior a la fecha de inicio."
        )

    nueva_tarea = Tarea(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        fecha_inicio=datos.fecha_inicio,
        fecha_limite=datos.fecha_limite,
        prioridad=datos.prioridad,
        estado=EstadoTarea.PENDIENTE,
        horas_estimadas=datos.horas_estimadas,
        id_asignatura=id_asignatura
    )

    return tarea_repository.crear(db,nueva_tarea)


def obtener_tarea_por_id(db: Session,id_tarea: int) -> Tarea | None:

    return tarea_repository.obtener_por_id(
        db,
        id_tarea
    )


def listar_tareas(db: Session,id_asignatura: int) -> list[Tarea]:

    return tarea_repository.listar_por_asignatura(
        db,
        id_asignatura
    )


def actualizar_tarea(db: Session,id_tarea: int,datos: TareaUpdate) -> Tarea | None:

    tarea = tarea_repository.obtener_por_id(db,id_tarea)

    if tarea is None:
        return None

    return tarea_repository.actualizar(db,tarea,datos)


def eliminar_tarea(db: Session,id_tarea: int) -> bool:

    tarea = tarea_repository.obtener_por_id(db,id_tarea)

    if tarea is None:
        return False

    tarea_repository.eliminar(db,tarea)

    return True