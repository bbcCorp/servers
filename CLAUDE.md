# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

```bash
# Download required Docker images
python fetch_images.py

# Start all active services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Architecture Overview

This is a Docker Compose development server stack that provides multiple services for development and testing environments. All services run on a custom bridge network called `servers` for secure inter-service communication.

### Core Components

- **docker-compose.yml**: Service definitions with active and disabled services
- **fetch_images.py**: Python script to pull Docker images defined in .env
- **.env**: Environment variables for all service configurations including ports, credentials, and image versions
- **./dev-servers/**: Directory for persistent data storage for all services

### Active Services
- Neo4j (Graph Database) - ports 7474, 7687
- PostgreSQL (Relational Database) - port 5432
- PgVector (PostgreSQL with Vector Extension) - port 5433
- Redis Stack (Cache + UI) - ports 6379, 8001
- RabbitMQ (Message Queue + Management) - ports 5672, 15672
- MongoDB (NoSQL Document Database) - port 27017

### Disabled Services (commented out)
- N8N (Workflow Automation) - port 5678
- MinIO (S3-compatible Storage) - ports 9000, 9001
- Ollama (AI/ML Model Server) - port 11434

## Common Development Tasks

### Service Management
```bash
# Check service status
docker-compose ps

# View specific service logs
docker-compose logs [service-name]

# Follow logs in real-time
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart [service-name]

# Execute commands in containers
docker-compose exec postgres psql -U postgres
docker-compose exec mongo mongosh
```

### Selective Service Start
```bash
# Start only specific services
docker-compose up -d postgres redis
```

### Environment Configuration
Service configurations are managed through .env file variables. Key patterns:
- Port variables: `{SERVICE}_PORT`
- Image variables: `{SERVICE}_DOCKER_IMAGE` or `{SERVICE}_IMAGE`
- Credentials: `{SERVICE}_USER`, `{SERVICE}_PASSWORD`

### Data Persistence
All service data is persisted in `./dev-servers/` directory with subdirectories for each service.

## Security Notes
- Default passwords are provided for development convenience
- Services are exposed to localhost only by default
- Environment contains both development credentials (in .env) and docker-compose defaults (hardcoded)