from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verificar_access_token
from app.database.database import get_db
from app.repository import usuario as usuario_repository
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> Usuario:
    """Obtiene el usuario autenticado a partir del JWT."""

    payload = verificar_access_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token inválido o expirado.")

    correo = payload.get("sub")

    if correo is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token inválido.")

    usuario = usuario_repository.obtener_por_correo(db,correo)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario no encontrado.")

    if usuario.estado is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario inactivo.")

    return usuario