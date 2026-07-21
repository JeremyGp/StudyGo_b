from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.horario import (HorarioCreate,HorarioUpdate,HorarioOut)
from app.services import asignatura as asignatura_service
from app.services import horario as horario_service

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"],
)

@router.post("/",response_model=HorarioOut,status_code=status.HTTP_201_CREATED)
def crear_horario(datos: HorarioCreate,id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if cast(int, asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para crear horarios en esta asignatura.")

    try:
        return horario_service.crear_horario(db,datos,id_asignatura)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.get("/{id_horario}",response_model=HorarioOut)
def obtener_horario(id_horario: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    horario = horario_service.obtener_horario_por_id(db,id_horario)

    if horario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Horario no encontrado.")

    if cast(int, horario.asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a este horario.")

    return horario

@router.get("/",response_model=list[HorarioOut])
def listar_horarios(id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if cast(int, asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para listar horarios de esta asignatura.")

    return horario_service.listar_horarios(db,id_asignatura)

@router.put("/{id_horario}",response_model=HorarioOut)
def actualizar_horario(id_horario: int,datos: HorarioUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    horario = horario_service.obtener_horario_por_id(db,id_horario)

    if horario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Horario no encontrado.")

    if cast(int, horario.asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar este horario.")

    return horario_service.actualizar_horario(db,id_horario,datos)

@router.delete("/{id_horario}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_horario(id_horario: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    horario = horario_service.obtener_horario_por_id(db,id_horario)

    if horario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Horario no encontrado.")

    if cast(int, horario.asignatura.id_usuario) != cast(int, usuario_actual.id_usuario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar este horario.")

    horario_service.eliminar_horario(db,id_horario)
