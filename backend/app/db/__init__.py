import secrets

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import menu_item, order, order_item, table, user

    Base.metadata.create_all(bind=engine)
    _seed_tables()


def _seed_tables():
    from app.models.table import Table, TableStatus

    db = SessionLocal()
    try:
        if db.query(Table).count() == 0:
            db.add_all(
                [
                    Table(
                        number=number,
                        qr_token=_generate_qr_token(),
                        status=TableStatus.AVAILABLE,
                    )
                    for number in range(1, 11)
                ]
            )
            db.commit()
    finally:
        db.close()


def _backfill_table_tokens():
    from app.models.table import Table

    db = SessionLocal()
    try:
        tables = db.query(Table).filter(
            (Table.qr_token.is_(None)) | (Table.qr_token == "")).all()
        if not tables:
            return

        for table in tables:
            table.qr_token = _generate_qr_token()
        db.commit()
    finally:
        db.close()


def _generate_qr_token() -> str:
    return secrets.token_urlsafe(16)
