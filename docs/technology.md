# Technology Used

## Certificate API Endpoint Components

### Testing via FastAPI GUI

FastAPI provide automated documentation of endpoints. The GUI allows for testing of API endpoints:

- Prod: url/docs
- Dev: localhost:port/docs

### FastAPI Backend

FastAPI is a modern, fast, and high-performance web framework for building APIs based on Python.
[FastAPI Documentation](https://fastapi.tiangolo.com/)

- [Startlette](https://www.starlette.io/): lightweight ASGI framework/toolkit for building async web services in Python
- [Pydantic](https://docs.pydantic.dev/latest/): Define data models for data validation, serialization and documentation
- [Uvicorn](https://www.uvicorn.org/): ASGI server
- [httpbin](https://httpbin.org/): Test external notification system
  - Ideally this will only be used for testing purpose. Eventually refactor with separate event or messaging system.

### Database and Tools

- [SQLAlchemy](https://www.sqlalchemy.org/):
  - Object Relational Mapper (ORM)
- [PostgreSQL](https://www.postgresql.org/) Relational database
  - ACID compliance for reliable transaction processing
  - uses Write-Ahead Log (WAL) to recover after failures.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/): DB migrations tool
  - Initialize: alembic init
  - Migration: alembic revision -m "message"
  - Upgrade: alembic upgrade head

## Account API Endpoint Components
