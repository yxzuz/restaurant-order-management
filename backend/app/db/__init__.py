import secrets

from sqlalchemy import inspect, text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


is_sqlite = settings.DATABASE_URL.startswith("sqlite")

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if is_sqlite else {},
)

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
    _migrate_sqlite_schema()
    _seed_tables()


def _migrate_sqlite_schema():
    if not is_sqlite:
        return

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        if "users" in existing_tables:
            user_columns = {column["name"] for column in inspector.get_columns("users")}
            if "hashed_password" not in user_columns:
                connection.execute(
                    text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT ''")
                )

        if "orders" in existing_tables:
            order_columns = {column["name"] for column in inspector.get_columns("orders")}
            if "table_id" not in order_columns:
                connection.execute(text("ALTER TABLE orders ADD COLUMN table_id INTEGER"))
            if "payment_status" not in order_columns:
                connection.execute(text("ALTER TABLE orders ADD COLUMN payment_status VARCHAR(6) NOT NULL DEFAULT 'unpaid'"))
            if "closed_at" not in order_columns:
                connection.execute(text("ALTER TABLE orders ADD COLUMN closed_at DATETIME"))

        if "tables" in existing_tables:
            table_columns = {column["name"] for column in inspector.get_columns("tables")}
            if "status" not in table_columns:
                connection.execute(text("ALTER TABLE tables ADD COLUMN status VARCHAR(9) NOT NULL DEFAULT 'available'"))
            if "qr_token" not in table_columns:
                connection.execute(text("ALTER TABLE tables ADD COLUMN qr_token VARCHAR(64)"))

    _backfill_table_tokens()


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
                    for number in range(1, 21)
                ]
            )
            db.commit()
    finally:
        db.close()


def _backfill_table_tokens():
    from app.models.table import Table

    db = SessionLocal()
    try:
        tables = db.query(Table).filter((Table.qr_token.is_(None)) | (Table.qr_token == "")).all()
        if not tables:
            return

        for table in tables:
            table.qr_token = _generate_qr_token()
        db.commit()
    finally:
        db.close()


def _generate_qr_token() -> str:
    return secrets.token_urlsafe(16)
