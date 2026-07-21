from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.asignatura import (AsignaturaCreate,AsignaturaUpdate,AsignaturaOut)
from app.services import asignatura as asignatura_service

router = APIRouter(
    prefix="/asignaturas",
    tags=["Asignaturas"],
)

@router.post("/", response_model=AsignaturaOut, status_code=status.HTTP_201_CREATED)
def crear_asignatura(datos: AsignaturaCreate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    return asignatura_service.crear_asignatura(db,datos,usuario_actual.id_usuario)

@router.get("/{id_asignatura}",response_model=AsignaturaOut)
def obtener_asignatura(id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):

    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para acceder a esta asignatura.")

    return asignatura

@router.get("/", response_model=list[AsignaturaOut])
def listar_asignaturas(db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    return asignatura_service.listar_asignaturas(db,usuario_actual.id_usuario)

@router.put("/{id_asignatura}",response_model=AsignaturaOut)
def actualizar_asignatura(id_asignatura: int,datos: AsignaturaUpdate,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para modificar esta asignatura.")

    return asignatura_service.actualizar_asignatura(db,id_asignatura,datos)

@router.delete("/{id_asignatura}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asignatura(id_asignatura: int,db: Session = Depends(get_db),usuario_actual: Usuario = Depends(get_current_user)):
    asignatura = asignatura_service.obtener_asignatura_por_id(db,id_asignatura)

    if asignatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Asignatura no encontrada.")

    if asignatura.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar esta asignatura.")

    asignatura_service.eliminar_asignatura(db,id_asignatura)
