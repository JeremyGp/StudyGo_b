from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import verificar_access_token
from app.database.database import get_db
from app.repository import usuario as usuario_repository
from app.models.usuario import Usuario

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)) -> Usuario:
    token = credentials.credentials
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

    if not usuario.estado:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario inactivo.")

    return usuario