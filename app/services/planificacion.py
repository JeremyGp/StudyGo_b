from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.enums import DiasSemana, PrioridadTarea
from app.models.horario import Horario
from app.models.tarea import Tarea
from app.repository import asignatura as asignatura_repository
from app.repository import horario as horario_repository
from app.repository import tarea as tarea_repository


HORA_INICIO_DIA = time(7, 0)
HORA_FIN_DIA = time(22, 0)
HORAS_MAXIMAS_POR_BLOQUE = 2

DIA_SEMANA_POR_WEEKDAY = {
    0: DiasSemana.LUNES,
    1: DiasSemana.MARTES,
    2: DiasSemana.MIERCOLES,
    3: DiasSemana.JUEVES,
    4: DiasSemana.VIERNES,
    5: DiasSemana.SABADO,
}


def calcular_fecha_inicio_sugerida(
    db: Session,
    tarea: Tarea,
    fecha_referencia: datetime | None = None
) -> datetime:
    """Calcula la primera fecha libre recomendada para iniciar una tarea."""

    bloques = generar_plan_estudio(db, tarea, fecha_referencia)

    if not bloques:
        raise ValueError("No se encontraron espacios libres antes de la fecha limite.")

    return bloques[0]["inicio"]


def planificar_tarea(
    db: Session,
    id_tarea: int,
    fecha_referencia: datetime | None = None
) -> dict:
    """Genera el plan de estudio y guarda la fecha de inicio sugerida."""

    tarea = tarea_repository.obtener_por_id(db, id_tarea)

    if tarea is None:
        raise ValueError("Tarea no encontrada.")

    bloques = generar_plan_estudio(db, tarea, fecha_referencia)

    if not bloques:
        raise ValueError("No se encontraron espacios libres antes de la fecha limite.")

    tarea.fecha_inicio_sugerida = bloques[0]["inicio"]
    db.commit()
    db.refresh(tarea)

    return {
        "id_tarea": tarea.id_tarea,
        "fecha_inicio_sugerida": tarea.fecha_inicio_sugerida,
        "horas_estimadas": tarea.horas_estimadas,
        "bloques": bloques,
    }


def recalcular_planificacion(
    db: Session,
    id_tarea: int,
    fecha_referencia: datetime | None = None
) -> dict:
    """Recalcula la planificación cuando una tarea cambia."""

    return planificar_tarea(db, id_tarea, fecha_referencia)


def generar_plan_estudio(
    db: Session,
    tarea: Tarea,
    fecha_referencia: datetime | None = None
) -> list[dict]:
    """Distribuye las horas estimadas en bloques libres antes de la fecha limite."""

    validar_tarea_planificable(tarea)

    fecha_referencia = fecha_referencia or datetime.now()
    inicio_busqueda = obtener_inicio_busqueda(tarea, fecha_referencia)

    if inicio_busqueda >= tarea.fecha_limite:
        raise ValueError("La fecha de inicio debe ser anterior a la fecha limite.")

    horas_restantes = tarea.horas_estimadas
    bloques_planificados = []
    dia_actual = inicio_busqueda.date()

    while horas_restantes > 0 and dia_actual <= tarea.fecha_limite.date():
        bloques_libres = obtener_bloques_libres_del_dia(
            db,
            tarea,
            dia_actual,
            tarea.id_tarea
        )

        for inicio, fin in bloques_libres:
            inicio_bloque = max(inicio, inicio_busqueda)
            fin_bloque = min(fin, tarea.fecha_limite)

            if inicio_bloque >= fin_bloque:
                continue

            horas_disponibles = calcular_horas(inicio_bloque, fin_bloque)

            if horas_disponibles <= 0:
                continue

            horas_asignadas = min(
                horas_restantes,
                horas_disponibles,
                HORAS_MAXIMAS_POR_BLOQUE
            )

            fin_planificado = inicio_bloque + timedelta(hours=horas_asignadas)

            bloques_planificados.append(
                {
                    "inicio": inicio_bloque,
                    "fin": fin_planificado,
                    "horas": horas_asignadas,
                }
            )

            horas_restantes -= horas_asignadas

            if horas_restantes <= 0:
                break

        dia_actual += timedelta(days=1)

    return bloques_planificados


def obtener_inicio_busqueda(
    tarea: Tarea,
    fecha_referencia: datetime
) -> datetime:
    """Define desde que momento empezar a buscar espacios libres."""

    dias_disponibles = (tarea.fecha_limite.date() - fecha_referencia.date()).days

    if tarea.prioridad == PrioridadTarea.ALTA or dias_disponibles <= 3:
        return fecha_referencia

    if tarea.prioridad == PrioridadTarea.MEDIA or dias_disponibles <= 7:
        return fecha_referencia + timedelta(days=1)

    return fecha_referencia + timedelta(days=2)


def validar_tarea_planificable(tarea: Tarea) -> None:
    """Valida que la tarea tenga los datos mínimos para poder planificarse."""

    if tarea.fecha_limite is None:
        raise ValueError("La tarea debe tener una fecha limite.")

    if tarea.horas_estimadas is None or tarea.horas_estimadas <= 0:
        raise ValueError("La tarea debe tener horas estimadas mayores a cero.")

    if tarea.id_asignatura is None:
        raise ValueError("La tarea debe pertenecer a una asignatura.")


def obtener_bloques_libres_del_dia(
    db: Session,
    tarea: Tarea,
    dia: date,
    id_tarea_excluida: int | None = None
) -> list[tuple[datetime, datetime]]:
    """Obtiene los espacios libres del dia evitando clases y tareas planificadas."""

    inicio_dia = datetime.combine(dia, HORA_INICIO_DIA)
    fin_dia = datetime.combine(dia, HORA_FIN_DIA)
    bloques_ocupados = obtener_bloques_ocupados_del_dia(
        db,
        tarea,
        dia,
        id_tarea_excluida
    )

    if not bloques_ocupados:
        return [(inicio_dia, fin_dia)]

    bloques_libres = []
    cursor = inicio_dia

    for inicio_clase, fin_clase in bloques_ocupados:
        if cursor < inicio_clase:
            bloques_libres.append((cursor, inicio_clase))

        if cursor < fin_clase:
            cursor = fin_clase

    if cursor < fin_dia:
        bloques_libres.append((cursor, fin_dia))

    return bloques_libres


def obtener_bloques_ocupados_del_dia(
    db: Session,
    tarea: Tarea,
    dia: date,
    id_tarea_excluida: int | None = None
) -> list[tuple[datetime, datetime]]:
    """Une los horarios de clase y las tareas ya planificadas del usuario."""

    bloques_clase = obtener_bloques_clase_usuario_del_dia(db, tarea, dia)
    bloques_tareas = obtener_bloques_tareas_del_dia(
        db,
        tarea,
        dia,
        id_tarea_excluida
    )

    return ordenar_y_unificar_bloques(bloques_clase + bloques_tareas)


def obtener_bloques_clase_usuario_del_dia(
    db: Session,
    tarea: Tarea,
    dia: date
) -> list[tuple[datetime, datetime]]:
    """Obtiene los horarios de clase de todas las asignaturas del usuario."""

    if tarea.asignatura is None:
        return obtener_bloques_clase_del_dia(db, tarea.id_asignatura, dia)

    asignaturas = asignatura_repository.listar_por_usuario(
        db,
        tarea.asignatura.id_usuario
    )
    bloques = []

    for asignatura in asignaturas:
        bloques.extend(
            obtener_bloques_clase_del_dia(
                db,
                asignatura.id_asignatura,
                dia
            )
        )

    return ordenar_y_unificar_bloques(bloques)


def obtener_bloques_tareas_del_dia(
    db: Session,
    tarea: Tarea,
    dia: date,
    id_tarea_excluida: int | None = None
) -> list[tuple[datetime, datetime]]:
    """Obtiene bloques ocupados por tareas ya planificadas del mismo usuario."""

    if tarea.asignatura is None:
        return []

    asignaturas = asignatura_repository.listar_por_usuario(
        db,
        tarea.asignatura.id_usuario
    )
    bloques = []

    for asignatura in asignaturas:
        tareas = tarea_repository.listar_por_asignatura(
            db,
            asignatura.id_asignatura
        )

        for tarea_planificada in tareas:
            bloque = convertir_tarea_en_bloque_ocupado(
                tarea_planificada,
                dia,
                id_tarea_excluida
            )

            if bloque is not None:
                bloques.append(bloque)

    return ordenar_y_unificar_bloques(bloques)


def convertir_tarea_en_bloque_ocupado(
    tarea: Tarea,
    dia: date,
    id_tarea_excluida: int | None = None
) -> tuple[datetime, datetime] | None:
    """Convierte una tarea con fecha sugerida en un bloque ocupado."""

    if id_tarea_excluida is not None and tarea.id_tarea == id_tarea_excluida:
        return None

    if tarea.fecha_inicio_sugerida is None:
        return None

    if tarea.fecha_inicio_sugerida.date() != dia:
        return None

    if tarea.horas_estimadas is None or tarea.horas_estimadas <= 0:
        return None

    horas_ocupadas = min(
        tarea.horas_estimadas,
        HORAS_MAXIMAS_POR_BLOQUE
    )

    inicio = tarea.fecha_inicio_sugerida
    fin = inicio + timedelta(hours=horas_ocupadas)

    return inicio, fin


def obtener_bloques_clase_del_dia(
    db: Session,
    id_asignatura: int,
    dia: date
) -> list[tuple[datetime, datetime]]:
    """Convierte los horarios de clase de una asignatura en bloques ocupados."""

    dia_semana = DIA_SEMANA_POR_WEEKDAY.get(dia.weekday())

    if dia_semana is None:
        return []

    horarios = horario_repository.listar_por_asignatura(db, id_asignatura)
    horarios_del_dia = filtrar_horarios_por_dia(horarios, dia_semana)

    bloques = [
        (
            datetime.combine(dia, horario.hora_inicio),
            datetime.combine(dia, horario.hora_fin),
        )
        for horario in horarios_del_dia
    ]

    return ordenar_y_unificar_bloques(bloques)


def filtrar_horarios_por_dia(
    horarios: list[Horario],
    dia_semana: DiasSemana
) -> list[Horario]:
    """Filtra los horarios que corresponden a un dia de la semana."""

    return [
        horario
        for horario in horarios
        if horario.dia_semana == dia_semana
    ]


def ordenar_y_unificar_bloques(
    bloques: list[tuple[datetime, datetime]]
) -> list[tuple[datetime, datetime]]:
    """Ordena bloques y une aquellos que se solapan."""

    if not bloques:
        return []

    bloques_ordenados = sorted(bloques, key=lambda bloque: bloque[0])
    bloques_unificados = [bloques_ordenados[0]]

    for inicio, fin in bloques_ordenados[1:]:
        ultimo_inicio, ultimo_fin = bloques_unificados[-1]

        if inicio <= ultimo_fin:
            bloques_unificados[-1] = (ultimo_inicio, max(ultimo_fin, fin))
        else:
            bloques_unificados.append((inicio, fin))

    return bloques_unificados


def calcular_horas(inicio: datetime, fin: datetime) -> float:
    """Calcula la duración entre dos fechas en horas."""

    return (fin - inicio).total_seconds() / 3600
