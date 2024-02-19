import pytest
import os
import psycopg2
from tests.conftest import test_client as client

API_BASE_URL = os.getenv("APP_URL")

def test_api_health(client):
    response = client.get(f"{API_BASE_URL}/health")

    assert response.status_code == 200

def test_postgres_health():
    try:
        connection = psycopg2.connect(
            host="account_db_primary_test",
            port=5432,
            user="user",
            password="password",
            database="account_db_primary_test",
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

def test_get_accounts(client):
    response = client.get(f"{API_BASE_URL}/api/accounts")

    assert response.status_code == 200

def test_create_account(client):
    data = {"email": "test5@example.com",
            "password": "testpassword2",
            "first_name": "First",
            "last_name": "Last"}
    response = client.post(f"{API_BASE_URL}/api/accounts", json=data)
    assert response.status_code == 200 or 201

# def test_get_account_by_id(client):
#     response = client.get(f"{API_BASE_URL}/api/accounts/17da0ce6-6bc4-4856-bac3-be56263a3aaa")

#     assert response.status_code == 200

# def test_delete_account(client):
#     response = client.delete(f"{API_BASE_URL}/api/accounts/17da0ce6-6bc4-4856-bac3-be56263a3aaa")

#     assert response.status_code == 200
