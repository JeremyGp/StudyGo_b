import bcrypt
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


def hash_contrasena(contrasena: str) -> str:
    """Convierte una contraseña en texto plano en un hash seguro."""
    contrasena_bytes = contrasena.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(contrasena_bytes, salt)
    return hash_bytes.decode("utf-8")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    """Compara una contraseña en texto plano contra el hash guardado."""
    contrasena_bytes = contrasena.encode("utf-8")
    hash_bytes = hash_guardado.encode("utf-8")
    return bcrypt.checkpw(contrasena_bytes, hash_bytes)


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    """Crea un nuevo usuario en la base de datos."""
    hash_generado = hash_contrasena(datos.contrasena)

    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        contrasena_hash=hash_generado
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

# Usuario | None significa que la función puede devolver un objeto Usuario o None si no se encuentra el usuario.
def obtener_usuario_por_id(db: Session, id_usuario: int) -> Usuario | None:
    """Busca un usuario por su id. Devuelve None si no existe."""
    return db.query(Usuario).filter(Usuario.id == id_usuario).first()


def obtener_usuario_por_correo(db: Session, correo: str) -> Usuario | None:
    """Busca un usuario por su correo. Se usa mucho en el login."""
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def listar_usuarios(db: Session):
    """Devuelve todos los usuarios registrados."""
    return db.query(Usuario).all()


def actualizar_usuario(db: Session, id_usuario: int, datos: UsuarioUpdate) -> Usuario | None:
    """Actualiza solo los campos que vengan en 'datos'."""
    usuario = obtener_usuario_por_id(db, id_usuario)

    if usuario is None:
        return None

    if datos.nombre is not None:
        usuario.nombre = datos.nombre

    if datos.correo is not None:
        usuario.correo = datos.correo

    if datos.estado is not None:
        usuario.estado = datos.estado

    db.commit()
    db.refresh(usuario)

    return usuario


def eliminar_usuario(db: Session, id_usuario: int) -> bool:
    """Desactiva un usuario (borrado lógico, no se elimina de la BD)."""
    usuario = obtener_usuario_por_id(db, id_usuario)

    if usuario is None:
        return False
    #En vez de db.delete(): en vez de eliminar la fila, marcamos estado = False. Es una práctica común porque no pierdes el historial (tareas, comentarios, etc. que dependen de ese usuario).#
    usuario.estado = False
    db.commit()

    return True