# Docker Configuration Update Summary

## Changes Made

### 1. Updated Docker Image Versions

#### PostgreSQL
- **Before**: `postgres:18-alpine`
- **After**: `postgres:17-alpine`
- **Added**: `POSTGRES_INITDB_ARGS` configuration for prepared transactions
- **Changed**: Added initialization directory mount for custom SQL scripts

#### Redis Stack Server
- **Before**: `redis/redis-stack-server:latest`
- **After**: `redis/redis-stack-server:8-alpine`
- Pinned to specific stable version

#### RabbitMQ
- **Before**: `rabbitmq:4.3.2-management-alpine` 
- **After**: `rabbitmq:4.4-management-alpine`
- Removed duplicate `RABBITMQ_PORT` environment variable in .env
- Updated to latest 4.4 release

#### Ontotext GraphDB
- **Before**: `graphdb:11.4.2`
- **After**: `graphdb:11.5.1`
- Updated to latest stable release

### 2. Replaced MinIO with RustFS

**MinIO Service Removed:**
- Removed entire MinIO service definition
- Removed all MinIO-related environment variables from .env
- Removed MinIO ports (9000, 9001) and console configuration

**RustFS Service Added:**
- New service: `rustfs`
- Image: `rustfs/rustfs:latest`
- Port: `9000` (matches MinIO's primary port)
- Storage path: `./dev-servers/rustfs/data`
- Configuration in .env:
  - `RUSTFS_DOCKER_IMAGE`: Container image reference
  - `RUSTFS_PORT`: Service port

### 3. Added Hindsight Service

**New Service: `hindsight`**
- Image: `vectorize/hindsight:latest`
- Port: `8080`
- Depends on: PostgreSQL (waits for healthy status)
- Storage: `./dev-servers/hindsight/data`

**Environment Variables:**
```env
HINDSIGHT_DOCKER_IMAGE="vectorize/hindsight:latest"
HINDSIGHT_PORT=8080
HINDSIGHT_POSTGRES_DB=postgres
HINDSIGHT_POSTGRES_SCHEMA=hindsight
HINDSIGHT_POSTGRES_USER=hindsight_user
HINDSIGHT_POSTGRES_PASSWORD="hindsight@1"
```

**PostgreSQL Initialization:**

Created: `./dev-servers/postgres/init/01-hindsight-init.sql`

This script:
- Creates `hindsight_user` PostgreSQL user
- Creates `hindsight` schema within the existing `postgres` database
- Grants schema privileges to the user
- Sets up default privileges for all objects created in the schema
- Configures the user's search path to use the hindsight schema by default

**Benefits of Schema Approach:**
- Lighter resource usage (single database connection pool)
- Simpler setup (no separate database management)
- Easier to manage alongside N8N (which also uses postgres database with its own schema)
- Better for development environments

## Service Startup Order

1. PostgreSQL starts first (required by both N8N and Hindsight)
2. RabbitMQ starts (required by N8N)
3. Hindsight waits for PostgreSQL health check before starting
4. N8N starts after PostgreSQL is healthy and RabbitMQ is running
5. RustFS starts independently
6. Other services start as configured

## Directory Structure

```
./dev-servers/
├── postgres/
│   ├── data/           (database files, including hindsight schema)
│   └── init/           (initialization scripts)
│       └── 01-hindsight-init.sql
├── rustfs/
│   └── data/           (RustFS storage)
├── hindsight/
│   └── data/           (Hindsight application data - non-database files)
└── [other services...]
```

**Note:** Hindsight database tables are stored within the `postgres` database in the `hindsight` schema, not in a separate database.

## Configuration Notes

- PostgreSQL now has prepared transactions enabled (`max_prepared_transactions=100`) for Hindsight
- Hindsight uses a dedicated schema (`hindsight`) within the main `postgres` database
- Hindsight connects to PostgreSQL via URL: `postgresql://hindsight_user:hindsight@1@postgres:5432/postgres?search_path=hindsight`
- N8N uses its own schema (`n8n`) in the same PostgreSQL instance
- Both services share the same PostgreSQL instance and database, using separate schemas for isolation
- RustFS uses port 9000 (previously used by MinIO)
- Hindsight uses port 8080 (note: may conflict with OLLAMA_WEBUI_PORT if both are enabled)

## Next Steps

1. Run `docker-compose down` to stop existing services
2. Run `python fetch_images.py` to download new images
3. Run `docker-compose up -d` to start services with new configuration
4. Verify PostgreSQL initialization by checking logs: `docker-compose logs postgres`
5. Verify Hindsight connects properly: `docker-compose logs hindsight`

## Breaking Changes

- MinIO is no longer available; use RustFS instead
- Ensure any applications using MinIO's S3 interface are updated to use RustFS API
