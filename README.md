# tls certificate management

System for managing customers and their TLS Certificates.

_This project is just for demo purposes. For environment variables, please use a more secure method._

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
  - Update certificate is_active (True: Active, False: Deactivated)
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
6. Metrics (healthy, DB load balance, resource utilization)
7. Kubernetes for orchestration, load balancing, and API Gateway.

</details>

# Setup

Clone the project

## Docker - Setup

1. Create Image and Volume

```
docker compose --parallel 2 pull
```

2. Start up containers:

```
docker-compose up -d
or docker-compose up -d --build
```

## Account Service - Setup

1. Create schema by Exec into Account Service Endpoint

```
 docker-compose exec account_api python manage.py create_db
```

2. Verify table schema was created by Exec into DB

```
1. docker-compose exec account_db_primary psql --username=user --dbname=account_db_primary
2. password: password
3. View list of databases:
    \l
4. Connect to database:
    \c account_db_primary
5. List relations (see schema):
    \dt
6. Quit:
    \q
```

### Run Migrations:

If no existing migrations folder start at step 2 else skip to step 4:

1. CD into account-api folder
2. Initialize migration file path:

   - docker-compose exec account_api flask db init

3. Initialize first migration

   - docker-compose exec account_api flask db migrate -m "initial migration"

4. Upgrade migration / Apply Existing migrations

   - docker-compose exec account_api flask upgrade

5. If another migration is needed:
   - docker-compose exec account_api flask db migrate -m "comment"
     Apply Change to DB: docker-compose exec account_api flask db upgrade

### Test

1. CD into account-api folder.
2. Create Account

```
curl -X POST -H "Content-Type: application/json" -d '{"email": "test2@example.com", "password": "testpassword2", "first_name": "First", "last_name": "Last"}' http://localhost:5001/api/accounts

```

- Response = {"message": "Account created"}

3. Get Account

```
curl http://localhost:5001/api/accounts
```

4. Copy account_id (UUID format)
   - example: "account_id": "17da0ce6-6bc4-4856-bac3-be56263a3aaa"
5. Get Account by Id:

```
curl http://localhost:5001/api/accounts/{replace_with_copied_account_id}

```

6. Delete Account

```
curl -X DELETE http://localhost:5001/api/accounts/{replace_with_copied_account_id}
```

## Certificate Service - Setup

### Testing

#### Via FastAPI built in GUI

[http://localhost:5002/docs#/](http://localhost:5002/docs#/)

- Ensure Certificate Server is running in docker

#### Via Curl

1. CD into account-api folder.
2. Create Certificate: Account_ID needed, example account_id: 6268a212-f4e5-4b44-994c-973fd4b4daa0

```
curl -X 'POST' \
  'http://localhost:5002/api/certificates/?account_id=6268a212-f4e5-4b44-994c-973fd4b4daa0' \
  -H 'accept: application/json' \
  -d ''

```

3. Get all certificates

```
curl -X 'GET' \
  'http://localhost:5002/api/certificates/' \
  -H 'accept: application/json'
```

4. Get certificate by certificate id

```
curl -X 'GET' \
  'http://localhost:5002/api/certificates/1' \
  -H 'accept: application/json'
```

5. Get certificates by account

```
curl -X 'GET' \
  'http://localhost:5002/api/certificates/6268a212-f4e5-4b44-994c-973fd4b4daa0/' \
  -H 'accept: application/json'
```

6. Patch deactivate certificate by certificate id

```
curl -X 'PATCH' \
  'http://localhost:5002/api/certificates/1/deactivate/' \
  -H 'accept: application/json'
```

7. Patch activate certificate by certificate id

```
curl -X 'PATCH' \
  'http://localhost:5002/api/certificate/1/activate/' \
  -H 'accept: application/json'
```
