from schemas import *
from uuid import uuid4
from utils import *
from db.models import *
import datetime
from fastapi import Response
from sqlalchemy.orm import Session

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

# account_id = str(uuid4())
# privateKey = generate_private_key()
# private_key = serialize_private_key(privateKey)
# certificate_body = generate_certificate_from_private_key(privateKey, account_id)
# created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

# def test_create_certs():
#     update = CertificateModel(
#             id=1,
#             account_id=account_id,
#             is_active=False,
#             private_key=private_key,
#             certificate_body=certificate_body,
#             created_at=created_at,
#             updated_at=created_at
#         )

        # mock_model = CertificateOut(
        #     id=id,
        #     account_id=account_id,
        #     is_active=False,
        #     private_key=private_key,
        #     certificate_body=certificate_body,
        #     created_at=created_at,
        #     updated_at=created_at
        # )
#     assert update

from main import app, get_db
from fastapi import Request, Depends
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi.responses import ORJSONResponse
import uuid

client = TestClient(app)

def generate_mock_data(n):
    id = n + 1
    account_id = str(uuid.uuid4())
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

mock_certs = [generate_mock_data(0),generate_mock_data(1)]

@pytest.fixture
def mock_db():
    mock_session = Mock(session=Session)
    mock_query = Mock()
    mock_query.return_value.all.return_value = mock_certs
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
    app.dependency_overrides[get_db] = lambda: mock_db_request.state.db

    try:
        response = client.get("/api/certificates/")

        print("response", response.json())
        app.dependency_overrides = {}
        # get certs from mock_db
        query = mock_db_request.state.db.query.return_value.all.return_value
        serialized = remove_non_serializable_attributes(query)

        print("serialized", serialized)
    except Exception as e:
        print(f"Error in test_create_cert: {e}")
        raise

    assert response.status_code == 200
    assert response.json() == serialized
