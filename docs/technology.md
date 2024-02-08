# Technology Used

## Account API Endpoint Components

[Account endpoint](./api/account.md) is used to create and delete customer accounts. Since authorization and authentication is not in scope for this project, Flask was used as the backend for its simplicity and lightweight.

- [SQLAlchemy](https://www.sqlalchemy.org/) was used to simplify DB interactions with PostgreSQL.
- [PostgreSQL](https://www.postgresql.org/) Relational database
  - ACID compliance for reliable transaction processing.
- [passlib](https://passlib.readthedocs.io/en/stable/) to hash password before saving into DB.
- [Gunicorn](https://flask.palletsprojects.com/en/3.0.x/deploying/gunicorn/) as WSGI server.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for migrations (uses Alembic).

## Certificate API Endpoint Components

[Certificate endpoint](./api/certificate.md) is used to create, get, and update certificates. Since this endpoint will serve over a million users, performance is a key requirement. As there are various data types and additionally complexity may be introduce as more features are developed, FastAPI was used as the backend for its high-performance, GUI documentation / testing of endpoints, and pydantic data validation.

### Testing via FastAPI GUI

FastAPI provide automated documentation of endpoints. The GUI allows for testing of API endpoints:

- Prod: url/docs
- Dev: localhost:port/docs

### FastAPI Backend

FastAPI is a modern, fast, and high-performance web framework for building APIs based on Python.
[FastAPI Documentation](https://fastapi.tiangolo.com/)

- [Startlette](https://www.starlette.io/): lightweight ASGI framework/toolkit for building async web services in Python
- [Pydantic](https://docs.pydantic.dev/latest/):
  - Define data models for data validation, serialization and documentation.
  - Enforces schema constraints on data at runtime, code ingestion, and return data as designed.
- [Uvicorn](https://www.uvicorn.org/): ASGI server
- [httpbin](https://httpbin.org/): Test external notification system.
  - Ideally this will only be used for testing purpose. Eventually refactor with separate event or messaging system.
- cryptography to generate keys, certificates, and encrypt data in PEM format. See more at [cryptography.md](cryptography.md)

### Database and Tools

- SQLAlchemy:
  - Object Relational Mapper (ORM)
- PostgreSQL: Relational database
  - ACID compliance for reliable transaction processing
  - uses Write-Ahead Log (WAL) to recover after failures.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/): DB migrations tool
  - Initialize: alembic init
  - Migration: alembic revision -m "message"
  - Upgrade: alembic upgrade head
