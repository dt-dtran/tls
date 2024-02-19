import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy.orm import Session
from main import app, get_db
from schemas import *
from utils import *
from db.models import *
import datetime
from uuid import uuid4
import logging

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"
logger = logging.getLogger(__name__)

client = TestClient(app)

def generate_mock_data(n):
    id = n + 1
    account_id = str(uuid4())
    privateKey = generate_private_key()
    private_key = serialize_private_key(privateKey)
    certificate_body = generate_certificate_from_private_key(privateKey, account_id)
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    mock_model = {
        "is_active": False,
        "private_key": private_key,
        "certificate_body": certificate_body,
        "created_at": created_at,
        "updated_at": created_at,
        "id": id,
        "account_id": account_id,
    }

    return mock_model

def first_data():
    account_id = "6268a212-f4e5-4b44-994c-973fd4b4daa0"
    privateKey = generate_private_key()
    private_key = serialize_private_key(privateKey)
    certificate_body = generate_certificate_from_private_key(privateKey, account_id)
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    mock_model = {
        "is_active": False,
        "private_key": private_key,
        "certificate_body": certificate_body,
        "created_at": created_at,
        "updated_at": created_at,
        "id": 1,
        "account_id": account_id,
    }

    return mock_model

mock_certs = [first_data(), generate_mock_data(1)]

@pytest.fixture
def mock_db():
    mock_session = Mock(session=Session)
    mock_query = Mock()
    mock_query.return_value.all.return_value = mock_certs
    mock_query.return_value.get.return_value = mock_certs[1]
    mock_query.return_value.filter.return_value.all.return_value = [mock_certs[0]]

    mock_session.query = mock_query
    return mock_session

@pytest.fixture
def mock_db_request(mock_db):
    mock_request = Mock(name="mock_request", spec=Request)
    mock_request.state.db = mock_db
    return mock_request

def test_db_middleware_connection(mock_db_request):
    db = get_db(mock_db_request)
    assert db is mock_db_request.state.db

def test_app_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

def test_get_certs(mock_db_request):
    logger.info("Starting test_get_certs")
    app.dependency_overrides[get_db] = lambda: mock_db_request.state.db

    # get certs from mock_db
    query = mock_db_request.state.db.query.return_value.all.return_value
    serialized = remove_non_serializable_attributes(query)
    response = client.get("/api/certificates/")

    assert response.status_code == 200
    assert response.json() == serialized

def test_create_cert(mock_db_request):
    logger.info("Starting test_create_cert")

    app.dependency_overrides[get_db] = lambda: mock_db_request.state.db
    account_id = uuid4()
    mock_data = {
        "account_id": account_id
    }

    response = client.post("/api/certificates/", data=mock_data)
    data = response.json()

    assert response.status_code == 200
    assert data["certificate_body"] is not None
    assert data["private_key"] is not None
    assert data["account_id"] is not None

# additional test
def test_get_certificate_id(mock_db_request):
    logger.info("Starting test_get_cert[id]")
    app.dependency_overrides[get_db] = lambda: mock_db_request.state.db

    query = mock_db_request.state.db.query.return_value.get.return_value
    serialized = remove_non_serializable_attributes(query)

    response = client.get("/api/certificates/2/")
    print("response", response.json())

    assert response.status_code == 200
    assert response.json() == serialized

def test_get_certificate_account_id(mock_db_request):
    logger.info("Starting test_get_cert[account_id]")
    app.dependency_overrides[get_db] = lambda: mock_db_request.state.db
    account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

    query = mock_db_request.state.db.query.return_value.filter.return_value.all.return_value
    serialized = remove_non_serializable_attributes(query)
    response = client.get(f"/api/certificates/account/{account_id}/")

    assert response.status_code == 200
    assert response.json() == serialized

# patch
# def test_deactivate(mock_db_request):
#     logger.info("Starting test_patch_cert[deactivate]")
#     app.dependency_overrides[get_db] = lambda: mock_db_request.state.db

#     response = client.patch("/api/certificates/2/deactivate/")

#     assert response.status_code == 200

# def test_activate(mock_db_request):
#     logger.info("Starting test_patch_cert[activate]")
#     app.dependency_overrides[get_db] = lambda: mock_db_request.state.db

#     response = client.patch("/api/certificates/2/activate/")

#     assert response.status_code == 200

# model
def test_create_certs_from_model():
    logger.info("Starting test_create_from_model")
    account_id = str(uuid4())
    privateKey = generate_private_key()
    private_key = serialize_private_key(privateKey)
    certificate_body = generate_certificate_from_private_key(privateKey, account_id)
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    update = CertificateModel(
        id=1,
        account_id=account_id,
        is_active=False,
        private_key=private_key,
        certificate_body=certificate_body,
        created_at=created_at,
        updated_at=created_at
    )

    mock_model = CertificateOut(
        id=1,
        account_id=account_id,
        is_active=False,
        private_key=private_key,
        certificate_body=certificate_body,
        created_at=created_at,
        updated_at=created_at
    )
    assert update
