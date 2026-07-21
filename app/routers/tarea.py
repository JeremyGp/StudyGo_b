from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario

from app.schemas.tarea import (TareaCreate,TareaUpdate,TareaOut)
from app.schemas.subtarea import (SubtareaCreate,SubtareaUpdate,SubtareaOut)
from app.services import asignatura as asignatura_service
from app.services import generador_subtarea as generador_subtarea_service
from app.services import notificacion as notificacion_service
from app.services import planificacion as planificacion_service
from app.services import tarea as tarea_service
from app.services import subtarea as subtarea_service

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)

# TAREAS

@router.post("/",response_model=TareaOut,status_code=status.HTTP_201_CREATED)
def crear_tarea(datos: TareaCreate,id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para crear tareas en esta asignatura.")

    try:
        return tarea_service.crear_tarea(db,datos,id_asignatura)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.get("/",response_model=list[TareaOut])
def listar_tareas(id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para listar tareas de esta asignatura.")

    return tarea_service.listar_tareas(db,id_asignatura)


@router.get("/{id_tarea}",response_model=TareaOut)
def obtener_tarea(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a esta tarea.")

    return tarea


@router.put("/{id_tarea}",response_model=TareaOut)
def actualizar_tarea(id_tarea: int,datos: TareaUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta tarea.")

    return tarea_service.actualizar_tarea(db,id_tarea,datos)


@router.delete("/{id_tarea}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar esta tarea.")

    tarea_service.eliminar_tarea(db,id_tarea)

# SUBTAREAS

@router.post("/{id_tarea}/planificar")
def planificar_tarea(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para planificar esta tarea.")

    try:
        return planificacion_service.planificar_tarea(db,id_tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.post("/{id_tarea}/recalcular-planificacion")
def recalcular_planificacion(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para recalcular esta tarea.")

    try:
        return planificacion_service.recalcular_planificacion(db,id_tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.get("/{id_tarea}/plan-estudio")
def obtener_plan_estudio(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para consultar el plan de esta tarea.")

    try:
        bloques = planificacion_service.generar_plan_estudio(db,tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    return {
        "id_tarea": tarea.id_tarea,
        "fecha_inicio_sugerida": bloques[0]["inicio"] if bloques else None,
        "horas_estimadas": tarea.horas_estimadas,
        "bloques": bloques,
    }


@router.post("/{id_tarea}/generar-subtareas",response_model=list[SubtareaOut])
def generar_subtareas(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para generar subtareas en esta tarea.")

    try:
        return generador_subtarea_service.generar_subtareas(db,id_tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.post("/{id_tarea}/regenerar-subtareas",response_model=list[SubtareaOut])
def regenerar_subtareas(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para regenerar subtareas en esta tarea.")

    try:
        return generador_subtarea_service.regenerar_subtareas(db,id_tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.post("/{id_tarea}/generar-recordatorios")
def generar_recordatorios(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para generar recordatorios en esta tarea.")

    try:
        return notificacion_service.generar_recordatorios_tarea(db,id_tarea)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@router.post("/{id_tarea}/subtareas",response_model=SubtareaOut,status_code=status.HTTP_201_CREATED)
def crear_subtarea(id_tarea: int,datos: SubtareaCreate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para crear subtareas en esta tarea.")

    return subtarea_service.crear_subtarea(db,datos,id_tarea)

@router.get("/{id_tarea}/subtareas",response_model=list[SubtareaOut])
def listar_subtareas(id_tarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

    if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para listar subtareas de esta tarea.")

    return subtarea_service.listar_subtareas(db,id_tarea)


@router.get("/{id_tarea}/subtareas/{id_subtarea}",response_model=SubtareaOut)
def obtener_subtarea(id_tarea: int,id_subtarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    subtarea = subtarea_service.obtener_subtarea_por_id(db,id_subtarea)

    if subtarea is None or subtarea.id_tarea != id_tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subtarea no encontrada.")

    if subtarea.tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a esta subtarea.")

    return subtarea


@router.put("/{id_tarea}/subtareas/{id_subtarea}",response_model=SubtareaOut)
def actualizar_subtarea(id_tarea: int,id_subtarea: int,datos: SubtareaUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    subtarea = subtarea_service.obtener_subtarea_por_id(db,id_subtarea)

    if subtarea is None or subtarea.id_tarea != id_tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subtarea no encontrada.")

    if subtarea.tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta subtarea.")

    return subtarea_service.actualizar_subtarea(db,id_subtarea,datos)


@router.delete("/{id_tarea}/subtareas/{id_subtarea}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_subtarea(id_tarea: int,id_subtarea: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    subtarea = subtarea_service.obtener_subtarea_por_id(db,id_subtarea)

    if subtarea is None or subtarea.id_tarea != id_tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subtarea no encontrada.")

    if subtarea.tarea.asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar esta subtarea.")

    subtarea_service.eliminar_subtarea(db,id_subtarea)
