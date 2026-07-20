from sqlalchemy.orm import Session

from app.models.horario import Horario
from app.repository import horario as horario_repository
from app.schemas.horario import HorarioCreate, HorarioUpdate


def crear_horario(db: Session,datos: HorarioCreate,id_asignatura: int) -> Horario:
    """Crea un horario para una asignatura."""
    if datos.hora_fin <= datos.hora_inicio:
        raise ValueError(
            "La hora de fin debe ser posterior a la hora de inicio."
        )

    nuevo_horario = Horario(
        dia_semana=datos.dia_semana,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        aula=datos.aula,
        id_asignatura=id_asignatura
    )

    return horario_repository.crear(db,nuevo_horario)


def obtener_horario_por_id(db: Session,id_horario: int) -> Horario | None:

    return horario_repository.obtener_por_id(db,id_horario)


def listar_horarios(db: Session,id_asignatura: int) -> list[Horario]:

    return horario_repository.listar_por_asignatura(db,id_asignatura)


def actualizar_horario(db: Session,id_horario: int,datos: HorarioUpdate) -> Horario | None:

    horario = horario_repository.obtener_por_id(db,id_horario)

    if horario is None:
        return None

    return horario_repository.actualizar(db,horario,datos)


def eliminar_horario(db: Session,id_horario: int) -> bool:

    horario = horario_repository.obtener_por_id(db,id_horario)

    if horario is None:
        return False

    horario_repository.eliminar(db,horario)

    return True