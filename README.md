# tls

System for managing Customers and their TLS Certificates.

## Design

Microservices based architecture using RESTful API and JSON serialization. Each services with its own database for persistance.

Account service: Manage customer accounts

- Backend: Flask
- Database: postgreSQL DB
- Endpoint: Create and Delete accounts

Certificate service: Manages certificates

- Backend: FastAPI
- Database: postgreSQL DB
- Endpoint:
  - Create certificates
  - Update certificate is_active
  - Get all certificates by Account ID
  - Get certificates by certificate ID
- External system (httpbin) of certificate creation and updates.

Other services:

- traefik for reverse proxy and load balancing

See more detail on:

- [Technology used](./docs/technology.md)
- [Data Models](./docs/data-model.md)
- [Account API](./docs/api/account.md)
- [Account API](./docs/api/certificate.md)
- [Cryptography](./docs/cryptography.md)

<details>
<summary> Backlog</summary>

1. frontend
2. redis: Caching layer between services and DB
3. replica of DB (read, write)
4. kafka: Message broker for inter-service communication

- Listen to event changes to Certificate Status

5. Service registry
6. Metrics
7. Kubernetes for orchestration, load balancing, and API Gateway.

</details>

## Setup

### Account Service

1. Create Volume

```
docker volume create pgaccount-data-dev
docker volume create pgaccount-data-prod
```

2. Exec into Account Service Endpoint to create schema

```
 docker-compose exec account_api python manage.py create_db
```

3. Exec into DB to verify schema exist

```
docker-compose exec account_db_dev psql --username=user --dbname=account_db_dev

# See list of databases
  \l

# Connect to database
  \c account_db_dev

# List relations (see schema)
  \dt

# quit
  \q
```

If Migrations:

1. (if new): initialize migration file path

```
docker-compose exec account_api flask db init
```

2. Initialize first migration

```
docker-compose exec account_api flask db migrate -m "initial migration"
```

3. Upgrade migration

```
docker-compose exec account_api flask upgrade
```

4. If another migration is needed:

```
docker-compose exec account_api flask db migrate -m "comment"
docker-compose exec account_api flask upgrade
```
