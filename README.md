# tls

System for managing Customers and their TLS Certificates.

## Design

Microservices based architecture using RESTful API and JSON serialization. Each services with its own database for persistance.

Account service: Manage customer accounts

- Database: postgreSQL DB
- Endpoint: Create and Delete customers

Certificate service: Manages certificates

- Database?
  - NoSQL for scalability
  - SQL with indexing and sharding
- Endpoint:
  - Create, Update, and Delete certificates
  - Get all certificates by customerID
- Generate private key
- Support millions of certificates
- Publish message for event changes to Certificate Status

Other:

- frontend
- kafka: Message broker for inter-service communication
  - Listen to event changes to Certificate Status
- redis: Caching layer between services and DB

Consider:

- Nginx proxy to route services
- Service registry
- DB replicas (read, write)
- Metrics
- Kubernetes for orchestration, load balancing, and API Gateway.

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
