import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from schemas import *
from utils import *
from db.models import *
import uuid
import logging
import psycopg2.extras

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

logger = logging.getLogger(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2.extras

import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("PRIMARY_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

psycopg2.extras.register_uuid()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Base.metadata.drop_all(bind=engine)
    psycopg2.extras.register_uuid()
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

def test_integration_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_integration_get_certs(client):
    response = client.get("/api/certificates/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

def test_integration_get_cert_id(client):
    response = client.get("/api/certificates/1/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["id"] is not None
    assert data["account_id"] is not None
    assert data["certificate_body"] is not None
    assert data["private_key"] is not None

def test_integration_get_account_id(client):
    response = client.get(f"/api/certificates/account/6268a212-f4e5-4b44-994c-973fd4b4daa0")
    assert response.status_code == 200

    data = response.json()
    # logger.info(f"[INT data] {data}")
    assert isinstance(data, list)
    assert "account_id" in data[0]
    assert "certificate_body" in data[0]
    assert "private_key" in data[0]


def test_integration_patch_deactivate(client):
    response = client.patch(f"/api/certificates/1/deactivate/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["is_active"] is not None
    assert data["account_id"] is not None
    assert data["certificate_body"] is not None
    assert data["private_key"] is not None

def test_integration_patch_activate(client):
    response = client.patch(f"/api/certificates/1/activate/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["is_active"] is not None
    assert data["account_id"] is not None
    assert data["certificate_body"] is not None
    assert data["private_key"] is not None

# def test_integration_post_cert(client):
#     account_id = str(uuid.uuid4())
#     data = {
#         "account_id": account_id
#     }

#     response = client.post("/api/certificates/", data=data)

#     assert response.status_code == 200
