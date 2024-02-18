from schemas import *
from uuid import uuid4
from utils import *
from db.models import *
import datetime
from fastapi import Response

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

from fastapi.testclient import TestClient
from db.engine import engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
import pytest

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

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

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200

# def test_read_main(test_db):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
