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
