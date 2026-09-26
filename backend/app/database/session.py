"""Database engine, session factory, and initialization."""

from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database.base import Base

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    future=True,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def _seed_demo_farmer() -> None:
    """Create a documented demo farmer if none exists."""
    from sqlalchemy import select

    from app.services.auth_service import hash_password

    db = SessionLocal()
    try:
        exists = db.scalar(select(User).where(User.mobile == "9876543210"))
        if exists:
            return
        demo = User(
            full_name="Demo Farmer",
            mobile="9876543210",
            email="farmer@bovimed.demo",
            password_hash=hash_password("Demo@1234"),
            farm_name="Green Pasture Dairy",
            state="Karnataka",
            district="Bengaluru Rural",
            preferred_language="en",
            is_active=True,
        )
        db.add(demo)
        db.commit()
    except Exception:  # noqa: BLE001
        db.rollback()
    finally:
        db.close()


def init_db() -> None:
    """Create all tables if they do not exist."""
    import app.models  # noqa: F401
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.results_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    _seed_demo_farmer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
