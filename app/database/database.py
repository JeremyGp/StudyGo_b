from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logging import configure_logging

logger = configure_logging()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        # Mantiene viva la sesión de base de datos durante el ciclo de vida de la petición.
        yield db
    except SQLAlchemyError:
        # Si falla la base de datos, se realiza un rollback para dejar la sesión en estado limpio
        # y se registra el problema para facilitar la depuración.
        db.rollback()
        logger.exception("Error de base de datos durante la sesión")
        raise
    finally:
        # Siempre se cierra la sesión al terminar, evitando fugas de recursos.
        db.close()