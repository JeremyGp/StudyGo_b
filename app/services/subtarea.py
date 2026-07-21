from sqlalchemy.orm import Session

from app.models.enums import EstadoTarea
from app.models.subtarea import Subtarea
from app.repository import subtarea as subtarea_repository
from app.schemas.subtarea import SubtareaCreate, SubtareaUpdate


def crear_subtarea(db: Session,datos: SubtareaCreate,id_tarea: int) -> Subtarea:
    """Crea una nueva subtarea."""
    nueva_subtarea = Subtarea(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        estado=EstadoTarea.PENDIENTE,
        orden=datos.orden,
        id_tarea=id_tarea
    )

    return subtarea_repository.crear(db,nueva_subtarea)


def obtener_subtarea_por_id(db: Session,id_subtarea: int) -> Subtarea | None:

    return subtarea_repository.obtener_por_id(db,id_subtarea)


def listar_subtareas(db: Session,id_tarea: int) -> list[Subtarea]:

    return subtarea_repository.listar_por_tarea(db,id_tarea)


def actualizar_subtarea(db: Session,id_subtarea: int,datos: SubtareaUpdate) -> Subtarea | None:

    subtarea = subtarea_repository.obtener_por_id(db,id_subtarea)

    if subtarea is None:
        return None

    return subtarea_repository.actualizar(db,subtarea,datos)


def eliminar_subtarea(db: Session,id_subtarea: int) -> bool:

    subtarea = subtarea_repository.obtener_por_id(db,id_subtarea)

    if subtarea is None:
        return False

    subtarea_repository.eliminar(db,subtarea)

    return True