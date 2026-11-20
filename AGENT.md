# AGENT.md - Comprehensive Project Guide for AI Agents

**Last Updated:** 2026-11-20  
**Project:** Development Servers Stack with Docker Compose  
**Current Status:** ✅ All Core Services Operational

This file provides comprehensive guidance for AI agents (Claude, automated tools, etc.) working with this Docker-based development server stack. Follow these instructions to maintain consistency, avoid issues, and work effectively with the project.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Critical Information](#critical-information)
3. [Project Structure](#project-structure)
4. [Key Files & Their Purposes](#key-files--their-purposes)
5. [Agent Notes Folder](#agent-notes-folder) ⭐ START HERE
6. [Current Architecture](#current-architecture)
7. [Important Recent Changes](#important-recent-changes)
8. [Common Tasks](#common-tasks)
9. [Best Practices](#best-practices)
10. [Gotchas & Warnings](#gotchas--warnings)
11. [Testing & Verification](#testing--verification)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## 📖 Project Overview

This is a **Docker Compose-based development environment** that provides:

- **10 containerized services** running on a custom bridge network
- **Multi-schema PostgreSQL** database (public, hindsight, n8n schemas)
- **Graph & semantic databases** (Neo4j, GraphDB)
- **Message queuing & caching** (RabbitMQ, Redis)
- **File storage** (RustFS - S3-compatible)
- **Workflow automation** (N8N)
- **Agent memory system** (Hindsight with Ollama Cloud)
- **Log visualization** (Dozzle)
- **Web reverse proxy** (Nginx)

**Purpose:** Enable developers to quickly spin up all backend service dependencies for local development without installing them directly on their machines.

---

## 🔴 Critical Information - READ FIRST

### DO NOT IGNORE

1. **LLM Configuration for Hindsight**
   - Hindsight requires `LLM_API_KEY` from Ollama Cloud to run
   - Without it, the service will fail to start
   - Get key at: https://ollama.com/api
   - Set in `.env`: `LLM_API_KEY="your-actual-api-key"`

2. **PostgreSQL Multi-Schema Design**
   - `postgres` database contains 3 schemas: `public`, `n8n`, `hindsight`
   - Each service uses its own schema for isolation
   - Initialization happens automatically via `01-hindsight-init.sql`
   - DO NOT create separate databases - use schemas instead

3. **RustFS Replaced MinIO**
   - MinIO service has been removed
   - RustFS now handles S3-compatible file storage on port 9000
   - Any code expecting MinIO needs updating

4. **Variable Naming Convention**
   - Use `LLM_API` and `LLM_API_KEY` (not OLLAMA_API, etc.)
   - This allows easy provider switching (Ollama → OpenAI → etc.)
   - All environment variables use this generic naming

5. **Network Name: `servers`**
   - All services communicate via custom bridge network `servers`
   - Use service name (not localhost) for internal connections
   - Example: `postgres:5432` not `localhost:5432` from other containers

---

## 🗂️ Project Structure

```
D:\progs\servers/
├── docker-compose.yml              ← Service orchestration (DO NOT edit lightly)
├── .env                             ← Configuration variables (UPDATE with real values)
├── CLAUDE.md                        ← Original project docs
├── README.md                        ← User-facing documentation (KEEP UPDATED)
├── AGENT.md                         ← This file - agent instructions
│
├── CHANGES_SUMMARY.md               ← Changelog of recent updates
├── TEST_REPORT.md                   ← Test results from latest deployment
├── DEPLOYMENT_STATUS.md             ← Current status & troubleshooting
├── FINAL_DEPLOYMENT_SUMMARY.md      ← Comprehensive deployment guide
├── VARIABLE_NAMING_UPDATE.md        ← LLM variable naming update
│
├── fetch_images.py                  ← Script to pull all Docker images
├── dev-servers/
│   ├── postgres/
│   │   ├── data/                    ← PostgreSQL database files
│   │   └── init/
│   │       └── 01-hindsight-init.sql ← PostgreSQL initialization (DO NOT modify)
│   ├── redis/data/                  ← Redis persistence
│   ├── rabbitmq/data/               ← RabbitMQ data
│   ├── neo4j/                       ← Neo4j data, logs, config
│   ├── graphdb/                     ← GraphDB data
│   ├── rustfs/data/                 ← RustFS file storage
│   ├── n8n/data/                    ← N8N workflows
│   ├── hindsight/
│   │   ├── data/                    ← Hindsight app data
│   │   └── hindsight.env            ← Hindsight-specific config (reference only)
│   ├── nginx/                       ← Nginx configuration
│   └── dozzle/                      ← Dozzle data
│
└── [Git files]
    ├── .gitignore
    ├── LICENSE
    └── [other git files]
```

---

## 🔑 Key Files & Their Purposes

### Configuration Files

| File | Purpose | Modify? | Notes |
|------|---------|---------|-------|
| `.env` | All environment variables | ✅ YES | Update with real credentials & API keys |
| `docker-compose.yml` | Service definitions | ⚠️ CAREFUL | Only for adding/removing services |
| `fetch_images.py` | Download Docker images | ❌ NO | Only if adding new services |

### Documentation Files

| File | Purpose | Keep Updated? | Notes |
|------|---------|---------------|-------|
| `README.md` | User documentation | ✅ YES | Update when services change |
| `AGENT.md` | Agent instructions | ✅ YES | Update with new learnings |
| `CLAUDE.md` | Original architecture | ⚠️ IF CHANGED | Keep for reference |
| `CHANGES_SUMMARY.md` | Changelog | ✅ YES | Document all modifications |
| `TEST_REPORT.md` | Test results | ✅ YES | Update after testing |

### Initialization Files

| File | Purpose | Modify? | Notes |
|------|---------|---------|-------|
| `01-hindsight-init.sql` | PostgreSQL setup | ❌ NO | Only if schema design changes |
| `hindsight.env` | Hindsight config | ⚠️ REFERENCE | Use docker-compose environment instead |

---

## 📂 Agent Notes Folder

**Location:** `agent_notes/` directory  
**Purpose:** Working logs and historical documentation  
**When to Use:** Reference previous work, understand project evolution

### What's in agent_notes/

| File | Purpose | Use When |
|------|---------|----------|
| `CHANGES_SUMMARY.md` | Detailed changelog of modifications | Need to know what changed |
| `VARIABLE_NAMING_UPDATE.md` | LLM variable naming update | Configuring LLM settings |
| `FINAL_DEPLOYMENT_SUMMARY.md` | Complete deployment overview | Need full context |
| `DEPLOYMENT_STATUS.md` | Current status & troubleshooting | Debugging issues |
| `TEST_REPORT.md` | Test procedures & results | Verifying services |
| `AGENT_MD_SUMMARY.md` | Overview of this AGENT.md file | Understanding structure |
| `README.md` | Index of all notes | Navigating the folder |
| `WARP.md` | Original archived documentation | Historical reference |

### How to Use agent_notes/

**For New Agents:**
1. Read `agent_notes/README.md` to understand folder contents
2. Check `CHANGES_SUMMARY.md` to see what's been done
3. Reference specific files as needed

**For Understanding History:**
1. `WARP.md` - Original project setup
2. `CHANGES_SUMMARY.md` - Evolution of the project
3. `DEPLOYMENT_STATUS.md` - Current state

**For Specific Information:**
- **Configuration questions** → `VARIABLE_NAMING_UPDATE.md`
- **Service verification** → `TEST_REPORT.md`
- **Troubleshooting** → `DEPLOYMENT_STATUS.md`
- **Full deployment context** → `FINAL_DEPLOYMENT_SUMMARY.md`

### Important: These Are NOT Official Documentation

**These are working logs** - useful for understanding evolution but not authoritative.

**For official guidance, use:**
- ✅ **AGENT.md** (this file - main guide)
- ✅ **README.md** (user documentation in root)
- ✅ **docker-compose.yml** (service definitions)
- ✅ **.env** (configuration)

---

## 🏗️ Current Architecture

### Services Overview

```
┌─────────────────────────────────────────────────────────┐
│          Docker Bridge Network: "servers"               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  PostgreSQL  │  │  Neo4j Graph │  │  GraphDB       ││
│  │  17-alpine   │  │  2026        │  │  11.5.1        ││
│  │  5432        │  │  7474/7687   │  │  7200          ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  Redis       │  │  RabbitMQ    │  │  RustFS        ││
│  │  8-alpine    │  │  4.4-mgmt    │  │  latest        ││
│  │  6379        │  │  5672/15672  │  │  9000          ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  N8N         │  │  Hindsight   │  │  Dozzle        ││
│  │  2.28.2      │  │  latest*     │  │  latest        ││
│  │  5678        │  │  8080        │  │  8888          ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
│                                                          │
│  ┌──────────────────────────────────────────────────────┤
│  │  Nginx (Reverse Proxy)                   80/443      ││
│  └──────────────────────────────────────────────────────┤
│                                                          │
└─────────────────────────────────────────────────────────┘

* Hindsight requires LLM_API_KEY to be functional
```

### Data Flow

```
Application Requests
    ↓
Nginx (Reverse Proxy)
    ↓
N8N (Workflow Automation) ←→ PostgreSQL (n8n schema)
    ↓
Message Queue (RabbitMQ)
    ↓
Services:
  - Graph Queries → Neo4j
  - Semantic Search → GraphDB
  - Cache Lookups → Redis
  - File Storage → RustFS
  - Memory/Context → Hindsight + PostgreSQL (hindsight schema)
```

---

## 📌 Important Recent Changes

### Latest Changes (2026-11-20)

1. **PostgreSQL 18 → 17-alpine**
   - More stable LTS release
   - Better compatibility with Alpine Linux

2. **MinIO Removed → RustFS Added**
   - RustFS provides S3-compatible file storage
   - Port 9000 maintained for compatibility
   - No console UI (use API or S3 clients)

3. **Hindsight Integrated**
   - New agent memory service on port 8080
   - Uses PostgreSQL `hindsight` schema
   - Requires Ollama Cloud API key to function
   - Connected to external LLM provider

4. **Variable Naming Standardized**
   - Changed from `OLLAMA_API` → `LLM_API`
   - Changed from `OLLAMA_API_KEY` → `LLM_API_KEY`
   - Allows easy provider switching in future

5. **Multi-Schema PostgreSQL**
   - Single PostgreSQL instance with 3 schemas:
     - `public` - standard schema
     - `n8n` - N8N data
     - `hindsight` - Hindsight data
   - Reduces resource overhead
   - Easier backup/restore

6. **RabbitMQ 4.4**
   - Latest stable release
   - Full management UI

7. **GraphDB 11.5.1**
   - Latest stable semantic database

### Breaking Changes to Know

- ❌ **MinIO is gone** - Code expecting MinIO S3 endpoints must update to RustFS
- ❌ **Elasticsearch/Kibana commented out** - No ELK stack by default
- ⚠️ **Hindsight needs API key** - Won't start without `LLM_API_KEY`

---

## 🛠️ Common Tasks

### Task: Add a New Service

**Steps:**
1. Add service definition to `docker-compose.yml`
2. Add configuration variables to `.env`
3. Create volume directory: `mkdir -p dev-servers/service-name/data`
4. Update `README.md` service table
5. Update `AGENT.md` if significant
6. Document in `CHANGES_SUMMARY.md`

**Example:**
```yaml
# docker-compose.yml
  my-service:
    image: ${MY_SERVICE_IMAGE:-myimage:latest}
    container_name: my-service
    ports:
      - "${MY_SERVICE_PORT:-9999}:9999"
    environment:
      CONFIG: ${MY_SERVICE_CONFIG}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./dev-servers/my-service/data:/data
    restart: always
    networks:
      - servers
```

```env
# .env
MY_SERVICE_IMAGE="myimage:1.0.0"
MY_SERVICE_PORT=9999
MY_SERVICE_CONFIG="value"
```

### Task: Update Service Version

**Steps:**
1. Update version in `.env`: `SERVICE_IMAGE="image:newversion"`
2. Pull new image: `docker pull image:newversion`
3. Restart service: `docker-compose restart service-name`
4. Test the service
5. Document in `CHANGES_SUMMARY.md`

### Task: Change Service Configuration

**Steps:**
1. Edit `.env` file (don't edit docker-compose.yml)
2. Restart affected service: `docker-compose restart service-name`
3. For major changes: `docker-compose up -d --force-recreate service-name`
4. Verify with logs: `docker-compose logs service-name`

### Task: Enable/Disable Service

**To Disable:**
```yaml
# Comment out in docker-compose.yml
#  my-service:
#    image: ...
```

**To Enable:**
```yaml
# Uncomment in docker-compose.yml
  my-service:
    image: ...
```

Then: `docker-compose up -d`

### Task: Reset Service Data

**Steps:**
1. Stop service: `docker-compose stop service-name`
2. Remove data: `rm -rf dev-servers/service-name/data`
3. Create fresh directory: `mkdir -p dev-servers/service-name/data`
4. Restart: `docker-compose up -d service-name`

### Task: Activate Hindsight

**Steps:**
1. Get API key from https://ollama.com/api
2. Update `.env`: `LLM_API_KEY="actual-key-here"`
3. Restart: `docker-compose restart hindsight`
4. Verify: `docker-compose logs hindsight`
5. Access: http://localhost:8080

---

## ✅ Best Practices

### DO ✅

1. **Always use environment variables** - Never hardcode values in docker-compose.yml
2. **Use service names** - Reference containers by name, not IP addresses
3. **Document changes** - Update relevant markdown files after modifications
4. **Test after changes** - Verify services start and are accessible
5. **Keep .env clean** - Remove unused variables periodically
6. **Back up data** - Regularly backup `dev-servers/` directory
7. **Use schema-based design** - Add new data to PostgreSQL schemas, not new databases
8. **Keep README updated** - Any service change should be reflected in README.md
9. **Version your images** - Pin to specific versions, not `latest`
10. **Use logical port numbers** - Follow existing pattern (database ports 5000+, etc.)

### DON'T ❌

1. **Don't hardcode credentials** - Always use environment variables
2. **Don't modify initialization scripts** - `01-hindsight-init.sql` should remain unchanged
3. **Don't create multiple docker-compose files** - Single source of truth
4. **Don't use localhost inside containers** - Use service names
5. **Don't delete data directories** - Back up first, then delete
6. **Don't skip health checks** - Always wait for service_healthy condition
7. **Don't modify schemas directly** - Changes go in init script
8. **Don't commit .env with real values** - Use placeholders
9. **Don't use image:latest** - Pin to specific versions for reproducibility
10. **Don't skip testing** - Always verify changes work

---

## ⚠️ Gotchas & Warnings

### Network Issues

**Problem:** Service A can't reach Service B  
**Solution:**
- Use service name (not localhost) in connection strings
- Inside container: `postgres:5432` not `localhost:5432`
- Verify both services on `servers` network: `docker network inspect servers`

### PostgreSQL Connection Issues

**Problem:** Can't connect to PostgreSQL  
**Solutions:**
- Check health: `docker-compose ps | grep postgres`
- Wait for healthy status (shows "Up X minutes (healthy)")
- Verify password matches `.env`
- Check port: `netstat -an | grep 5432`

### Hindsight Not Starting

**Problem:** Hindsight exits immediately  
**Solutions:**
- Check if `LLM_API_KEY` is set in `.env`
- Verify key format is valid
- Check logs: `docker-compose logs hindsight`
- Restart with fresh key: `docker-compose restart hindsight`

### Disk Space Issues

**Problem:** Docker out of disk space  
**Solutions:**
- Remove unused images: `docker image prune`
- Remove old data: `rm -rf dev-servers/*/data`
- Check disk: `df -h`

### Port Already in Use

**Problem:** Port XXXX is already allocated  
**Solutions:**
- Change port in `.env`
- Or stop conflicting service on host
- Or use different host port in docker-compose

### Volume Permission Issues (Linux only)

**Problem:** Permission denied when accessing volumes  
**Solutions:**
```bash
sudo chown -R $USER:$USER ./dev-servers/
chmod -R u+w ./dev-servers/
```

---

## 🧪 Testing & Verification

### After Starting Services

**Run these checks:**

```bash
# 1. Check all services are running
docker-compose ps
# All services should show "Up" status

# 2. Check health status
docker-compose ps | grep postgres
# Should show "(healthy)" for postgres

# 3. Test PostgreSQL
docker-compose exec postgres psql -U postgres -c "SELECT 1"
# Should return 1

# 4. Test Redis
docker-compose exec redis redis-cli ping
# Should return PONG

# 5. Test RabbitMQ
docker-compose exec rabbitmq rabbitmq-diagnostics ping
# Should return Ping successful

# 6. Access Neo4j browser
# Open http://localhost:7474 in browser
# Should show Neo4j interface

# 7. Access N8N
# Open http://localhost:5678 in browser
# Should show N8N interface

# 8. Check PostgreSQL schemas
docker-compose exec postgres psql -U postgres -c "\dn"
# Should show: public, n8n, hindsight schemas

# 9. Check hindsight user
docker-compose exec postgres psql -U postgres -c "SELECT usename FROM pg_user WHERE usename='hindsight_user';"
# Should return: hindsight_user
```

### After Modifying Configuration

```bash
# 1. Restart affected service
docker-compose restart service-name

# 2. Wait for service to be ready
sleep 5

# 3. Check status
docker-compose ps | grep service-name

# 4. Check for errors
docker-compose logs service-name | tail -20

# 5. Verify connectivity from another service
docker-compose exec postgres psql -h service-name -U user -c "SELECT 1"
```

---

## 🔧 Troubleshooting Guide

### Quick Diagnosis

**Step 1: Check service status**
```bash
docker-compose ps
```

**Step 2: Check logs**
```bash
docker-compose logs service-name | tail -50
```

**Step 3: Check Docker resources**
```bash
docker stats
docker system df
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "No such image" | Image not downloaded | Run `python fetch_images.py` |
| "Port already allocated" | Port in use | Change port in `.env` |
| "Connection refused" | Service not ready | Wait longer, check status |
| "Authentication failed" | Wrong credentials | Check `.env` values |
| "Out of disk space" | Docker images too large | Prune unused images |
| "Service unhealthy" | Service crashed | Check logs, restart |

### Recovery Procedures

**Nuclear Option (if everything broken):**
```bash
# Stop all services
docker-compose down

# Remove all data (WARNING: data loss!)
rm -rf dev-servers/*/data

# Remove all containers/networks
docker system prune -a

# Start fresh
docker-compose up -d
```

---

## 📚 Reference Information

### Service Connection Strings

```
PostgreSQL:   postgresql://postgres:devServer@1@postgres:5432/postgres
PostgreSQL n8n schema:    ?search_path=n8n
PostgreSQL hindsight schema: ?search_path=hindsight
Redis:        redis://redis:6379
RabbitMQ:     amqp://rmquser:SuperSecurePassw0rd@rabbitmq:5672
Neo4j:        neo4j://neo4j:devServer@1@neo4j:7687
```

### Important Ports

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache |
| RabbitMQ AMQP | 5672 | Message queue |
| RabbitMQ Management | 15672 | Web UI |
| Neo4j HTTP | 7474 | Web interface |
| Neo4j Bolt | 7687 | Protocol |
| GraphDB | 7200 | Semantic database |
| RustFS | 9000 | File storage |
| N8N | 5678 | Workflow automation |
| Hindsight | 8080 | Agent memory |
| Dozzle | 8888 | Log viewer |
| Nginx | 80, 443 | Web proxy |

### Key Files to Remember

- **docker-compose.yml** - Service definitions (read-only except for adding services)
- **.env** - Configuration (edit this for settings)
- **README.md** - User documentation (keep updated)
- **AGENT.md** - This file (update with learnings)
- **01-hindsight-init.sql** - PostgreSQL setup (read-only)

---

## 🎓 Learning Resources for Agents

### Understanding the Project

1. Read `README.md` for user perspective
2. Review `docker-compose.yml` to understand service definitions
3. Check `.env` for all configuration options
4. Study `01-hindsight-init.sql` for PostgreSQL schema setup
5. Review recent documentation files for context

### For Specific Tasks

- **Adding services**: Check `CHANGES_SUMMARY.md` for how MinIO was removed and RustFS added
- **Configuration changes**: See `VARIABLE_NAMING_UPDATE.md` for how variables were renamed
- **Testing changes**: Review `TEST_REPORT.md` to see how testing was done
- **Troubleshooting**: Check `DEPLOYMENT_STATUS.md` for known issues

### Environment Variables Pattern

```env
# Always follow this pattern:
SERVICE_IMAGE="registry/image:version"
SERVICE_PORT=5000
SERVICE_USER=username
SERVICE_PASSWORD=password
SERVICE_CONFIG="config_value"
```

---

## 🚀 Final Reminders

1. **This is development-only** - Change all credentials for production
2. **Always test changes** - Don't deploy modifications untested
3. **Document everything** - Future agents (including yourself) will thank you
4. **Keep backups** - The `dev-servers/` directory contains all persistent data
5. **LLM_API_KEY is critical** - Hindsight won't work without it
6. **Services communicate via network name** - Not localhost or IP addresses
7. **PostgreSQL is multi-schema** - Use schemas for data isolation, not separate databases
8. **RustFS replaced MinIO** - Update any S3 endpoint code
9. **Use environment variables** - Never hardcode configuration
10. **Read the docs** - This file, README.md, and CLAUDE.md contain important info

---

## 📞 Questions or Issues?

Refer to:
1. This file (AGENT.md)
2. README.md (for user-facing info)
3. DEPLOYMENT_STATUS.md (for troubleshooting)
4. TEST_REPORT.md (for verification procedures)
5. `docker-compose logs service-name` (for specific service issues)

---

**Last Updated:** 2026-11-20  
**Status:** ✅ Comprehensive & Current  
**Next Review Date:** When major changes occur

---

🤖 **This guide is for AI agents and automated tools working with this project.**  
👤 **For user documentation, see README.md**  
📚 **For project history, see CHANGES_SUMMARY.md**
