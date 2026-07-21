from sqlalchemy.orm import Session

from app.models.asignatura import Asignatura
from app.repository import asignatura as asignatura_repository
from app.schemas.asignatura import AsignaturaCreate, AsignaturaUpdate


def crear_asignatura(db: Session,datos: AsignaturaCreate,id_usuario: int) -> Asignatura:
    """Crea una nueva asignatura para un usuario."""

    nueva_asignatura = Asignatura(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        ciclo=datos.ciclo,
        docente=datos.docente,
        id_usuario=id_usuario
    )

    return asignatura_repository.crear(db, nueva_asignatura)


def obtener_asignatura_por_id(db: Session,id_asignatura: int) -> Asignatura | None:

    return asignatura_repository.obtener_por_id(db, id_asignatura)


def listar_asignaturas(db: Session,id_usuario: int) -> list[Asignatura]:

    return asignatura_repository.listar_por_usuario(db, id_usuario)


def actualizar_asignatura(db: Session,id_asignatura: int,datos: AsignaturaUpdate) -> Asignatura | None:

    asignatura = asignatura_repository.obtener_por_id(db,id_asignatura)

    if asignatura is None:
        return None

    return asignatura_repository.actualizar(db,asignatura,datos)


def eliminar_asignatura(db: Session,id_asignatura: int) -> bool:

    asignatura = asignatura_repository.obtener_por_id(db,id_asignatura)

    if asignatura is None:
        return False

    asignatura_repository.eliminar(db,asignatura)

    return True