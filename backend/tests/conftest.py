import os
import sys
import tempfile
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure backend/ is on sys.path so `import app.*` works when running pytest from repo root.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# ---- Environment (must be set before importing app modules) ----
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("AWS_REGION", "ap-southeast-1")
os.environ.setdefault("AWS_S3_BUCKET", "test-bucket")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-access-key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-secret-access-key")

_TEST_DB_FILE = Path(tempfile.gettempdir()) / f"restaurant_order_mgmt_test_{uuid.uuid4().hex}.sqlite"
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{_TEST_DB_FILE}")

from app.main import app  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    # Fresh schema per test for isolation.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db_file():
    yield
    try:
        _TEST_DB_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_owner(client: TestClient, *, username: str, password: str, restaurant_name: str) -> str:
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
            "restaurant_name": restaurant_name,
        },
    )
    assert response.status_code == 201, response.text
    payload = response.json()
    assert "access_token" in payload
    return payload["access_token"]
