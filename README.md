# Online Order System (Microservices & DDD)

A distributed microservices-based online order processing system implementing **Domain-Driven Design (DDD)** and **CQRS (Command Query Responsibility Segregation)** patterns in Python with FastAPI.

## Architecture & Features

- **Microservices Design**:
  - `api-gateway`: Unified entry point routing requests to downstream services.
  - `order-service`: Core domain logic for order lifecycle management.
  - `user-service`: User management and customer validation.
  - `product-service`: Product inventory client and validation.
- **Domain-Driven Design (DDD)**:
  - Clean separation into `Domain`, `Application`, `Infrastructure`, and `API` layers.
  - Entities, Value Objects (`Address`), Aggregates, and Domain Repositories.
- **CQRS Pattern**:
  - Independent Command Handlers (`CreateOrderCommand`, `UpdateOrderCommand`) and Query Handlers (`GetOrderQuery`).
- **Event-Driven Architecture**:
  - Decoupled event publishing via `OrderEventPublisher`.
- **Containerization & Orchestration**:
  - Multi-service deployment via `docker-compose.yml`.

## Quick Start

### Running with Docker Compose
```bash
docker-compose up --build
```

### Running Locally
```bash
bash run_all.sh
```

### Running Tests
```bash
pytest test_system.py test_api.py test_services.py
```
