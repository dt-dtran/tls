import pytest
import psycopg2
import requests
import os
import uuid

API_BASE_URL = os.getenv("APP_URL")

def test_api_health():
    response = requests.get(f"{API_BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_postgres_health():
    try:
        connection = psycopg2.connect(
            host="certificate_db_primary_test",
            port=5432,
            user="user",
            password="password",
            database="certificate_db_primary_test",
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        assert result[0] == 1
        # Expecting a result of 1

    except Exception as e:
        pytest.fail(f"PostgreSQL health check failed: {str(e)}")

    finally:
        if connection:
            connection.close()

def test_get_all_certificates():
    response = requests.get(f"{API_BASE_URL}/api/certificates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_certificate_by_id():
    response = requests.get(f"{API_BASE_URL}/api/certificates/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_certificate_by_accountid():
    response = requests.get(f"{API_BASE_URL}/api/certificates/account/6268a212-f4e5-4b44-994c-973fd4b4daa0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_patch_deactivate_certificate():
    response = requests.patch(f"{API_BASE_URL}/api/certificates/1/deactivate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_patch_deactivate_certificate():
    response = requests.patch(f"{API_BASE_URL}/api/certificates/1/activate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

# def test_create_certificate():
#     data = {"account_id": str(uuid.uuid4())}
#     response = requests.post(f"{API_BASE_URL}/api/certificates", json=data)
#     assert response.status_code == 200

#     update = response.json()
#     assert isinstance(update, dict)
