from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.enums import EstadoTarea
from app.models.tarea import Tarea
from app.repository import asignatura as asignatura_repository


DIAS_PROXIMAS_ENTREGAS = 7


def obtener_dashboard(
    db: Session,
    id_usuario: int
) -> dict:
    """Calcula el resumen principal del dashboard de un usuario."""

    tareas = obtener_tareas_del_usuario(db, id_usuario)
    ahora = datetime.now()
    limite_proximas = ahora + timedelta(days=DIAS_PROXIMAS_ENTREGAS)

    total_tareas = len(tareas)
    tareas_pendientes = filtrar_por_estado(tareas, EstadoTarea.PENDIENTE)
    tareas_en_proceso = filtrar_por_estado(tareas, EstadoTarea.EN_PROCESO)
    tareas_completadas = filtrar_por_estado(tareas, EstadoTarea.COMPLETADA)
    tareas_vencidas = obtener_tareas_vencidas(tareas, ahora)
    proximas_entregas = obtener_proximas_entregas(
        tareas,
        ahora,
        limite_proximas
    )

    return {
        "total_tareas": total_tareas,
        "tareas_pendientes": len(tareas_pendientes),
        "tareas_en_proceso": len(tareas_en_proceso),
        "tareas_completadas": len(tareas_completadas),
        "tareas_vencidas": len(tareas_vencidas),
        "proximas_entregas": [
            serializar_tarea(tarea)
            for tarea in proximas_entregas
        ],
    }


def obtener_tareas_del_usuario(
    db: Session,
    id_usuario: int
) -> list[Tarea]:
    """Obtiene todas las tareas asociadas a las asignaturas de un usuario."""

    asignaturas = asignatura_repository.listar_por_usuario(db, id_usuario)
    tareas = []

    for asignatura in asignaturas:
        tareas.extend(asignatura.tareas)

    return tareas


def filtrar_por_estado(
    tareas: list[Tarea],
    estado: EstadoTarea
) -> list[Tarea]:
    """Filtra tareas por estado."""

    return [
        tarea
        for tarea in tareas
        if tarea.estado == estado
    ]


def obtener_tareas_vencidas(
    tareas: list[Tarea],
    ahora: datetime
) -> list[Tarea]:
    """Obtiene tareas vencidas que aun no estan completadas."""

    return [
        tarea
        for tarea in tareas
        if tarea.fecha_limite is not None
        and tarea.fecha_limite < ahora
        and tarea.estado != EstadoTarea.COMPLETADA
    ]


def obtener_proximas_entregas(
    tareas: list[Tarea],
    ahora: datetime,
    limite: datetime
) -> list[Tarea]:
    """Obtiene tareas no completadas que vencen en los proximos dias."""

    proximas = [
        tarea
        for tarea in tareas
        if tarea.fecha_limite is not None
        and ahora <= tarea.fecha_limite <= limite
        and tarea.estado != EstadoTarea.COMPLETADA
    ]

    return sorted(
        proximas,
        key=lambda tarea: tarea.fecha_limite
    )


def serializar_tarea(tarea: Tarea) -> dict:
    """Convierte una tarea en un diccionario simple para el dashboard."""

    return {
        "id_tarea": tarea.id_tarea,
        "titulo": tarea.titulo,
        "fecha_limite": tarea.fecha_limite,
        "estado": tarea.estado,
        "prioridad": tarea.prioridad,
        "id_asignatura": tarea.id_asignatura,
        "asignatura": tarea.asignatura.nombre if tarea.asignatura else None,
    }
