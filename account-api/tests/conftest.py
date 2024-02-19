from flask import Flask
from flask import jsonify
import pytest
from flask_sqlalchemy import SQLAlchemy
from init import app, db, migrate, Account

@pytest.fixture(scope="session")
def test_app():
    app.config.from_object("init.config.Config")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def new_account_isolated():
    account = Account({
        "email": "tester@gmail.com",
        "first_name": "Diana",
        "last_name": "Tester",
        "password": "Password4"
    })
    return account

@pytest.fixture(scope="module")
def new_account(test_app):
    with test_app.app_context():
        account = Account(
            email="tester@gmail.com",
            first_name="Diana",
            last_name="Tester",
            password="Password4"
        )
        db.session.add(account)
        db.session.commit()
        return account
