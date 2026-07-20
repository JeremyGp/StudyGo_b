from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.notificacion import (NotificacionCreate,NotificacionUpdate,NotificacionOut)
from app.services import notificacion as notificacion_service

router = APIRouter(prefix="/notificaciones",tags=["Notificaciones"])

@router.post("/",response_model=NotificacionOut,status_code=status.HTTP_201_CREATED)
def crear_notificacion(datos: NotificacionCreate,id_usuario: int,id_tarea: int | None = None,db: Session = Depends(get_db)):
    return notificacion_service.crear_notificacion(db,datos,id_usuario,id_tarea)

@router.get("/",response_model=list[NotificacionOut])
def listar_notificaciones(id_usuario: int,db: Session = Depends(get_db)):
    return notificacion_service.listar_notificaciones(db,id_usuario)

@router.get("/{id_notificacion}",response_model=NotificacionOut)
def obtener_notificacion(id_notificacion: int,db: Session = Depends(get_db)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    return notificacion

@router.put("/{id_notificacion}",response_model=NotificacionOut)
def actualizar_notificacion(id_notificacion: int,datos: NotificacionUpdate,db: Session = Depends(get_db)):
    notificacion = notificacion_service.actualizar_notificacion(db,id_notificacion,datos)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    return notificacion

@router.delete("/{id_notificacion}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_notificacion(id_notificacion: int,db: Session = Depends(get_db)):
    eliminado = notificacion_service.eliminar_notificacion(db,id_notificacion)

    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")