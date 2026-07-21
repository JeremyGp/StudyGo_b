from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.notificacion import (NotificacionCreate,NotificacionUpdate,NotificacionOut)
from app.services import notificacion as notificacion_service
from app.services import tarea as tarea_service

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"],
)

@router.post("/",response_model=NotificacionOut,status_code=status.HTTP_201_CREATED)
def crear_notificacion(datos: NotificacionCreate,id_tarea: int | None = None,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    if id_tarea is not None:
        tarea = tarea_service.obtener_tarea_por_id(db,id_tarea)

        if tarea is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada.")

        if tarea.asignatura.id_usuario != usuario_actual.id_usuario:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para asociar esta notificación a esa tarea.")

    return notificacion_service.crear_notificacion(db,datos,usuario_actual.id_usuario,id_tarea)

@router.get("/",response_model=list[NotificacionOut])
def listar_notificaciones(db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    return notificacion_service.listar_notificaciones(db,usuario_actual.id_usuario)

@router.get("/{id_notificacion}",response_model=NotificacionOut)
def obtener_notificacion(id_notificacion: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    if notificacion.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a esta notificación.")

    return notificacion

@router.put("/{id_notificacion}",response_model=NotificacionOut)
def actualizar_notificacion(id_notificacion: int,datos: NotificacionUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    if notificacion.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta notificación.")

    return notificacion_service.actualizar_notificacion(db,id_notificacion,datos)

@router.delete("/{id_notificacion}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_notificacion(id_notificacion: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    if notificacion.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar esta notificación.")

    notificacion_service.eliminar_notificacion(db,id_notificacion)
