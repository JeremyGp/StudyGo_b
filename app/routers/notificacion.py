from typing import cast

# Se usa cast para convertir los identificadores del modelo SQLAlchemy a valores simples
# y evitar errores de tipado al compararlos con el usuario autenticado.

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

        # Se valida que la tarea pertenezca al mismo usuario autenticado antes de
        # asociarle una notificación.
        if cast(int, tarea.asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para asociar esta notificación a esa tarea.")

    # El identificador del usuario autenticado se convierte a un entero simple para
    # que la capa de servicio reciba un valor compatible con la lógica de negocio.
    usuario_id = cast(int, usuario_actual.id_usuario)
    return notificacion_service.crear_notificacion(db,datos,usuario_id,id_tarea)

@router.get("/",response_model=list[NotificacionOut])
def listar_notificaciones(db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    # Se extrae el id del usuario autenticado como entero simple para listar
    # únicamente sus notificaciones y no las de otros usuarios.
    usuario_id = cast(int, usuario_actual.id_usuario)
    return notificacion_service.listar_notificaciones(db,usuario_id)

@router.get("/{id_notificacion}",response_model=NotificacionOut)
def obtener_notificacion(id_notificacion: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    # Se comprueba la propiedad de la notificación para evitar que un usuario
    # acceda a información que no le pertenece.
    if cast(int, notificacion.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a esta notificación.")

    return notificacion

@router.put("/{id_notificacion}",response_model=NotificacionOut)
def actualizar_notificacion(id_notificacion: int,datos: NotificacionUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    # Se limita la modificación a la notificación del usuario autenticado.
    if cast(int, notificacion.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta notificación.")

    return notificacion_service.actualizar_notificacion(db,id_notificacion,datos)


@router.patch("/{id_notificacion}/leer",response_model=NotificacionOut)
def marcar_notificacion_como_leida(id_notificacion: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    if notificacion.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta notificación.")

    return notificacion_service.marcar_como_leida(db,id_notificacion)

@router.delete("/{id_notificacion}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_notificacion(id_notificacion: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    notificacion = notificacion_service.obtener_notificacion_por_id(db,id_notificacion)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notificación no encontrada.")

    # Se impide borrar una notificación que pertenezca a otro usuario.
    if cast(int, notificacion.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar esta notificación.")

    notificacion_service.eliminar_notificacion(db,id_notificacion)
