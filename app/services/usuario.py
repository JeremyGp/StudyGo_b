import bcrypt
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repository import usuario as usuario_repository
from app.schemas.usuario import (UsuarioCreate,UsuarioUpdate,UsuarioOut,UsuarioLogin,Token,)
from app.core.security import (hash_contrasena,verificar_contrasena,crear_access_token,)


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    """Registra un nuevo usuario."""

    # Validar que el correo no exista
    usuario_existente = usuario_repository.obtener_por_correo(db, datos.correo)

    if usuario_existente:
        raise ValueError("El correo ya se encuentra registrado.")

    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        contrasena_hash=hash_contrasena(datos.contrasena)
    )

    return usuario_repository.crear(db, nuevo_usuario)

def autenticar_usuario(db: Session,correo: str,contrasena: str) -> Usuario | None:
    """Verifica las credenciales del usuario. Devuelve el usuario si son correctas."""

    usuario = usuario_repository.obtener_por_correo(db, correo)

    if usuario is None:
        return None

    if not verificar_contrasena(
        contrasena,
        usuario.contrasena_hash
    ):
        return None

    if not usuario.estado:
        return None

    return usuario

def login_usuario(db: Session, datos: UsuarioLogin) -> Token | None:
    """Autentica un usuario y genera un JWT."""

    usuario = autenticar_usuario(db,datos.correo,datos.contrasena)

    if usuario is None:
        return None

    access_token = crear_access_token(
        {"sub": usuario.correo}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        usuario=UsuarioOut.model_validate(usuario)
    )

# Usuario | None significa que la función puede devolver un objeto Usuario o None si no se encuentra el usuario.
def obtener_usuario_por_id(db: Session, id_usuario: int) -> Usuario | None:
    """Busca un usuario por su id. Devuelve None si no existe."""
    return usuario_repository.obtener_por_id(db, id_usuario)


def obtener_usuario_por_correo(db: Session, correo: str) -> Usuario | None:
    """Busca un usuario por su correo. Se usa mucho en el login."""
    return usuario_repository.obtener_por_correo(db, correo)


def listar_usuarios(db: Session) -> list[Usuario]:
    """Devuelve todos los usuarios registrados."""
    return usuario_repository.listar(db)


def actualizar_usuario(db: Session, id_usuario: int, datos: UsuarioUpdate) -> Usuario | None:

    usuario = usuario_repository.obtener_por_id(db, id_usuario)

    if usuario is None:
        return None
    # Validar correo duplicado
    if (datos.correo is not None and datos.correo != usuario.correo):
        existente = usuario_repository.obtener_por_correo(db, datos.correo)
        if existente:
            raise ValueError("El correo ya se encuentra registrado.")

    # Si se desea cambiar la contraseña
    if datos.contrasena is not None:
        usuario.contrasena_hash = hash_contrasena(datos.contrasena)

    return usuario_repository.actualizar(db, usuario, datos)


def eliminar_usuario(db: Session, id_usuario: int) -> bool:
    """Realiza un borrado lógico del usuario."""
    usuario = usuario_repository.obtener_por_id(db, id_usuario)

    if usuario is None:
        return False

    usuario_repository.desactivar(db, usuario)

    return True