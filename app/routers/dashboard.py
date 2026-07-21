from typing import cast

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from app.services import asignatura as asignatura_service
from app.services import tarea as tarea_service
from app.services import horario as horario_service
from app.services import notificacion as notificacion_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", status_code=status.HTTP_200_OK)
def obtener_dashboard(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    usuario_id = cast(int, usuario_actual.id_usuario)

    asignaturas = asignatura_service.listar_asignaturas(db, usuario_id)
    tareas = []
    for asignatura in asignaturas:
        tareas.extend(tarea_service.listar_tareas(db, cast(int, asignatura.id_asignatura)))

    horarios = []
    for asignatura in asignaturas:
        horarios.extend(horario_service.listar_horarios(db, cast(int, asignatura.id_asignatura)))

    notificaciones = notificacion_service.listar_notificaciones(db, usuario_id)

    tareas_completadas = sum(1 for tarea in tareas if getattr(tarea, "estado", None) == "Completada")
    tareas_pendientes = sum(1 for tarea in tareas if getattr(tarea, "estado", None) == "Pendiente")

    return {
        "usuario": {
            "id_usuario": usuario_actual.id_usuario,
            "nombre": usuario_actual.nombre,
            "correo": usuario_actual.correo,
        },
        "resumen": {
            "total_asignaturas": len(asignaturas),
            "total_tareas": len(tareas),
            "tareas_completadas": tareas_completadas,
            "tareas_pendientes": tareas_pendientes,
            "total_horarios": len(horarios),
            "total_notificaciones": len(notificaciones),
        },
    }
