from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_contrasena(contrasena: str) -> str:
    """Convierte una contraseña en texto plano en un hash seguro."""
    contrasena_bytes = contrasena.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(contrasena_bytes, salt)
    return hash_bytes.decode("utf-8")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    """Compara una contraseña en texto plano con el hash almacenado."""
    return bcrypt.checkpw(contrasena.encode("utf-8"),hash_guardado.encode("utf-8"))


def crear_access_token(data: dict) -> str:
    """Crea un JWT firmado."""

    datos = data.copy()

    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos.update({"exp": expiracion})

    token = jwt.encode(datos,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return token


def verificar_access_token(token: str):
    """Decodifica y valida un JWT. Devuelve el payload si es válido."""

    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload

    except JWTError:
        return None