from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.usuario import (UsuarioCreate,UsuarioUpdate,UsuarioOut,UsuarioLogin)
from app.services import usuario as usuario_service

router = APIRouter(prefix="/usuarios",tags=["Usuarios"])

@router.post("/",response_model=UsuarioOut,status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate,db: Session = Depends(get_db)):
    try:
        return usuario_service.crear_usuario(db, datos)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@router.post("/login")
def login(datos: UsuarioLogin,db: Session = Depends(get_db)):
    usuario = usuario_service.autenticar_usuario(db,datos.correo,datos.contrasena)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Correo o contraseña incorrectos.")

    return {
        "mensaje": "Inicio de sesión exitoso.",
        "usuario": UsuarioOut.model_validate(usuario)
}


@router.get("/",response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)

@router.get("/{id_usuario}",response_model=UsuarioOut)
def obtener_usuario(id_usuario: int,db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario_por_id(db,id_usuario)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")

    return usuario


@router.put("/{id_usuario}",response_model=UsuarioOut)
def actualizar_usuario(id_usuario: int,datos: UsuarioUpdate,db: Session = Depends(get_db)):
    try:
        usuario = usuario_service.actualizar_usuario(db,id_usuario,datos)

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.delete("/{id_usuario}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int,db: Session = Depends(get_db)):
    eliminado = usuario_service.eliminar_usuario(db,id_usuario)

    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")