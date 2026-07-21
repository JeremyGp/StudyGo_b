from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioUpdate


def obtener_por_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter(
        Usuario.id_usuario == id_usuario
    ).first()


def obtener_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(
        Usuario.correo == correo
    ).first()


def listar(db: Session):
    return db.query(Usuario).all()


def crear(db: Session, usuario: Usuario):
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def actualizar(db: Session, usuario: Usuario, datos: UsuarioUpdate):
    # Se aplican solo los campos enviados en la solicitud, usando setattr para
    # mantener compatibilidad con los atributos del modelo SQLAlchemy.
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario

def desactivar(db: Session, usuario: Usuario):
    # Se desactiva el usuario de forma lógica mediante un cambio de estado.
    setattr(usuario, "estado", False)
    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar(db: Session, usuario: Usuario):
    db.delete(usuario)
    db.commit()