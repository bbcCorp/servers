# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This repository provides a Docker-based local development environment for running multiple backend services (databases, message queues, storage, and workflow automation) in containers. The primary purpose is to enable developers to quickly spin up server dependencies without installing them directly on their host machine.

## Architecture

### Docker Compose Stack
The repository uses a single `docker-compose.yml` file that orchestrates 9 services in a shared bridge network:
- **Neo4j** (graph database) - ports 7474 (HTTP), 7687 (Bolt)
- **Postgres** (relational database) - port 5432
- **PgVector** (Postgres with vector extension) - port 5433
- **Redis** (cache/key-value store) - port 6379
- **RabbitMQ** (message broker) - ports 5672 (AMQP), 15672 (management UI)
- **MongoDB** (document database via Percona) - port 27017
- **n8n** (workflow automation) - port 5678
- **MinIO** (S3-compatible object storage) - ports 9000 (API), 9001 (console)
- **Ollama** (LLM runtime) - port 11435 (remapped from 11434)

All services are configured with:
- Persistent volumes mounted to `./dev-servers/<service>/data` (or `/config`, `/logs`, `/plugins` for Neo4j)
- Environment variables from `.env` file with defaults
- Automatic restart policy
- Shared `servers` network for inter-container communication

### Configuration Management
- `.env` file at repository root contains all service configurations (ports, credentials, image versions)
- All passwords default to `SuperSecurePassw0rd` or similar development-safe values
- Image versions are pinned via environment variables with fallback defaults in docker-compose.yml

### Client Test Directory
The `client-test/` subdirectory contains a Python testing client that:
- Uses `uv` for dependency management (modern Python package manager)
- Tests connectivity to services (e.g., RabbitMQ client in `rmq.py`)
- Loads configuration from the parent `.env` file

## Common Commands

### Service Management
```bash
# Download/update all Docker images
sh fetch_images.sh

# Start all services in detached mode
docker-compose up -d

# Start specific services only
docker-compose up -d neo4j postgres redis

# Stop all services
docker-compose down

# Stop and remove volumes (wipes data)
docker-compose down -v

# View service logs
docker-compose logs -f <service-name>

# Restart a specific service
docker-compose restart <service-name>

# Check service status
docker-compose ps
```

### Client Testing
```bash
# Navigate to client-test directory
cd client-test

# Install dependencies and create virtual environment
uv sync

# Run the test client
uv run python main.py

# Activate virtual environment manually
source .venv/bin/activate
```

### Service Access URLs
- **n8n**: http://localhost:5678
- **RabbitMQ Management**: http://localhost:15672 (user: rmquser, pass: SuperSecurePassw0rd)
- **RabbitMQ AMQP**: amqp://localhost:5672
- **MinIO Console**: http://localhost:9001 (user: minioadmin, pass: minioadmin)
- **Neo4j Browser**: http://localhost:7474 (user: neo4j, pass: devServer@1)
- **Postgres**: localhost:5432 (user: postgres, pass: devServer@1)
- **PgVector**: localhost:5433 (user: postgres, pass: devServer@1)
- **MongoDB**: localhost:27017 (user: mongoadmin, pass: SuperSecurePassw0rd)
- **Redis**: localhost:6379
- **Ollama**: localhost:11435

## Development Workflow

### Adding a New Service
1. Add service definition to `docker-compose.yml` following the existing pattern
2. Add configuration variables to `.env` file
3. Create volume mount directory in `dev-servers/<service-name>/`
4. Update `fetch_images.sh` if the image should be pre-pulled
5. Update this file's "Service Access URLs" section

### Modifying Service Configuration
- Edit `.env` to change ports, credentials, or image versions
- Restart affected services: `docker-compose restart <service-name>`
- For major changes, recreate: `docker-compose up -d --force-recreate <service-name>`

### Data Persistence
- All service data persists in `dev-servers/<service>/data` directories
- These directories are Git-ignored and exist only locally
- To reset a service's data, stop the service and delete its data directory

### Python Client Development
- Use `uv` for dependency management (not pip/poetry)
- Run `uv add <package>` to add dependencies
- The client loads configuration from the parent `.env` file via relative path
- Python 3.12+ required (see `.python-version`)
