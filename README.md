# Development Servers Stack

A comprehensive Docker Compose setup for running multiple development services and databases locally. Perfect for development, testing, and learning environments. Includes database services, message queues, caching, graph databases, semantic stores, file storage, and agent memory systems.

**Last Updated:** 2026-11-20  
**Status:** ✅ All Core Services Operational

---

## 🚀 Quick Start

```bash
# 1. Pull required Docker images
python fetch_images.py

# 2. Start all active services
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop all services
docker-compose down
```

---

## 📋 Prerequisites

- **Python 3.7+** - For the image download script
- **Docker 20.10+** or **Podman** - With docker compose support
- **Git** - For version control
- **8GB+ RAM** - For optimal performance with all services
- **50GB+ Disk Space** - For Docker images and data persistence

---

## 🏗️ Architecture

All services run on a custom bridge network called `servers` for secure inter-service communication. The stack includes:
- **Data Layer**: PostgreSQL (multi-schema), Neo4j, GraphDB
- **Cache & Queue**: Redis, RabbitMQ
- **Storage**: RustFS (S3-compatible)
- **Automation**: N8N workflow engine
- **Monitoring**: Dozzle log viewer
- **AI/Memory**: Hindsight (with Ollama Cloud)
- **Reverse Proxy**: Nginx

---

## 🗄️ Active Services (10 Services)

| Service | Port(s) | Status | Description |
|---------|---------|--------|-------------|
| **PostgreSQL** | 5432 | ✅ Running | Relational database with multi-schema support |
| **Redis** | 6379 | ✅ Running | In-memory cache with extensions (8-alpine) |
| **RabbitMQ** | 5672, 15672 | ✅ Running | Message queue + Management UI |
| **Neo4j** | 7474, 7687 | ✅ Running | Graph database (2026-community) |
| **GraphDB** | 7200 | ✅ Running | Semantic database (11.5.1) |
| **RustFS** | 9000 | ✅ Running | S3-compatible file storage (replaces MinIO) |
| **N8N** | 5678 | ✅ Running | Workflow automation engine |
| **Hindsight** | 8080 | ✅ Ready* | Agent memory system (requires LLM_API_KEY) |
| **Dozzle** | 8888 | ✅ Running | Container log viewer |
| **Nginx** | 80, 443 | ✅ Running | Reverse proxy and load balancer |

**\* Hindsight Ready**: Fully configured, awaiting Ollama Cloud API key to activate

---

## 📊 Service Details & Connection Information

### Database Services

#### PostgreSQL (Relational)
```
Port: 5432
Default User: postgres
Default Password: devServer@1
Connection: postgresql://postgres:devServer@1@localhost:5432/postgres

Schemas:
  • public     - Standard public schema
  • n8n        - N8N workflow automation data
  • hindsight  - Hindsight agent memory data
```

**UI:** pgAdmin or similar client  
**Health Check:** `docker-compose ps | grep postgres`

#### Neo4j (Graph Database)
```
Port: 7474 (HTTP), 7687 (Bolt)
URL: http://localhost:7474
User: neo4j
Password: devServer@1
Connection: neo4j://neo4j:devServer@1@localhost:7687
```

**UI:** http://localhost:7474  
**Browser:** Graph browser interface

#### GraphDB (Semantic Database)
```
Port: 7200
URL: http://localhost:7200
Description: Ontotext GraphDB 11.5.1
```

**UI:** http://localhost:7200  
**Type:** RDF/SPARQL database

---

### Cache & Queue Services

#### Redis Stack
```
Port: 6379
Connection: redis://localhost:6379
Features: Streams, JSON, Time Series, Search
```

**CLI:** `redis-cli -p 6379`

#### RabbitMQ
```
Port: 5672 (AMQP), 15672 (Management)
Management UI: http://localhost:15672
User: rmquser
Password: SuperSecurePassw0rd
Connection: amqp://rmquser:SuperSecurePassw0rd@localhost:5672
```

**UI:** http://localhost:15672

---

### Storage & AI Services

#### RustFS (File Storage)
```
Port: 9000
URL: http://localhost:9000
Type: S3-compatible storage (replaces MinIO)
Default Bucket: dev-bucket
```

**Usage:** AWS S3 SDK compatible clients

#### Hindsight (Agent Memory)
```
Port: 8080
URL: http://localhost:8080
Type: Agent memory system with Ollama Cloud
Database: PostgreSQL (hindsight schema)
LLM Provider: Ollama Cloud
Status: Requires LLM_API_KEY configuration
```

**Configuration:** See "Activating Hindsight" section

---

### Workflow & Monitoring

#### N8N (Workflow Automation)
```
Port: 5678
URL: http://localhost:5678
Type: Workflow automation engine
Database: PostgreSQL (n8n schema)
Version: 2.28.2
```

**UI:** http://localhost:5678

#### Dozzle (Log Viewer)
```
Port: 8888
URL: http://localhost:8888
Type: Container log viewer and analyzer
```

**UI:** http://localhost:8888

#### Nginx (Reverse Proxy)
```
Ports: 80 (HTTP), 443 (HTTPS)
Type: Web server and reverse proxy
```

---

## ⚙️ Configuration

### Environment Variables (.env)

Key configurable variables:

```env
# Database Configuration
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=devServer@1
POSTGRES_DB=postgres

# Redis Configuration
REDIS_PORT=6379

# RabbitMQ Configuration
RABBITMQ_PORT=5672
RABBITMQ_MGMT_PORT=15672
RMQ_USERNAME=rmquser
RMQ_PASSWORD=SuperSecurePassw0rd

# Neo4j Configuration
NEO4J_PORT=7474
NEO4J_USER=neo4j
NEO4J_PASSWORD=devServer@1

# GraphDB Configuration
GRAPHDB_PORT=7200

# RustFS Configuration
RUSTFS_PORT=9000

# N8N Configuration
N8N_PORT=5678

# Hindsight Configuration
HINDSIGHT_PORT=8080
LLM_API="https://ollama.com/api"
LLM_API_KEY="your-ollama-cloud-api-key"

# Nginx Configuration
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
```

### Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service definitions and orchestration |
| `.env` | Environment variables and credentials |
| `fetch_images.py` | Docker image download script |
| `dev-servers/postgres/init/01-hindsight-init.sql` | PostgreSQL schema initialization |

---

## 📁 Data Persistence

All service data persists in `./dev-servers/` directory:

```
dev-servers/
├── postgres/
│   ├── data/              # PostgreSQL databases
│   └── init/
│       └── 01-hindsight-init.sql  # Initialization script
├── redis/data/            # Redis cache data
├── rabbitmq/data/         # RabbitMQ queue data
├── neo4j/                 # Neo4j graph store
├── graphdb/               # GraphDB semantic store
├── rustfs/data/           # File storage
├── n8n/data/              # N8N workflows and data
├── hindsight/data/        # Hindsight application data
├── nginx/                 # Nginx configuration
└── dozzle/                # Dozzle data
```

**Backup Recommendation:** Regularly backup the entire `dev-servers/` directory for data preservation.

---

## 🚀 Getting Started with Key Services

### 1. First Time Setup

```bash
# Download all Docker images
python fetch_images.py

# Start all services
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check specific service logs
docker-compose logs postgres
```

### 2. Accessing Services

```bash
# PostgreSQL
psql -h localhost -U postgres -d postgres

# Redis
redis-cli -p 6379

# RabbitMQ Management
# Open: http://localhost:15672 (rmquser / SuperSecurePassw0rd)

# Neo4j Browser
# Open: http://localhost:7474 (neo4j / devServer@1)

# N8N
# Open: http://localhost:5678
```

### 3. Activating Hindsight

Hindsight requires an Ollama Cloud API key to run:

```bash
# 1. Get API key from: https://ollama.com/api
# 2. Update .env file
LLM_API_KEY="your-actual-ollama-api-key"

# 3. Restart Hindsight
docker-compose restart hindsight

# 4. Verify it's running
docker-compose logs hindsight
docker-compose ps | grep hindsight

# 5. Access at: http://localhost:8080
```

---

## 🔍 Common Operations

### Service Management

```bash
# Check service status
docker-compose ps

# View service logs (last 50 lines)
docker-compose logs --tail=50 [service-name]

# Follow logs in real-time
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart [service-name]

# Stop specific service
docker-compose stop [service-name]

# Start specific service
docker-compose start [service-name]

# Restart all services
docker-compose restart

# Stop all services
docker-compose stop

# Remove all containers (preserves data)
docker-compose down
```

### Database Operations

```bash
# PostgreSQL console
docker-compose exec postgres psql -U postgres

# List PostgreSQL schemas
docker-compose exec postgres psql -U postgres -c "\dn"

# Redis CLI
docker-compose exec redis redis-cli

# RabbitMQ management
# GUI: http://localhost:15672

# Neo4j browser
# GUI: http://localhost:7474
```

### Health Checks

```bash
# Check PostgreSQL health
docker-compose exec postgres pg_isready -U postgres

# Check Redis health
docker-compose exec redis redis-cli ping

# Check RabbitMQ health
docker-compose exec rabbitmq rabbitmq-diagnostics ping
```

---

## 🔄 Service Startup Order

Services start in this order based on dependencies:

1. **PostgreSQL** - Core database (required by most)
2. **Redis** - Cache layer
3. **RabbitMQ** - Message queue
4. **Neo4j** - Graph database (independent)
5. **GraphDB** - Semantic database (independent)
6. **RustFS** - File storage (independent)
7. **N8N** - Waits for PostgreSQL health check
8. **Hindsight** - Waits for PostgreSQL health check
9. **Nginx** - Web server (independent)
10. **Dozzle** - Log viewer (independent)

---

## 🔐 Security Notes

### Development Environment

Current configuration is suitable for **development only**. For production:

#### 1. Change Default Credentials
```env
POSTGRES_PASSWORD=YourStrongPassword123!
POSTGRES_USER=customuser
RMQ_PASSWORD=StrongRabbitMQPassword!
NEO4J_PASSWORD=StrongNeo4jPassword!
```

#### 2. Enable SSL/TLS
- Configure Nginx with valid certificates
- Update service connections to use `https://`

#### 3. Restrict Network Access
- Use firewall rules to limit port exposure
- Consider using VPN for remote access

#### 4. Manage Secrets
- Use external secret managers (Vault, AWS Secrets Manager)
- Never commit `.env` with real credentials to git

#### 5. API Key Management
- Rotate Ollama Cloud API keys regularly
- Monitor usage and access logs

---

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Change port in .env
POSTGRES_PORT=5433
REDIS_PORT=6380

# Restart service
docker-compose restart postgres redis
```

#### Service Won't Start
```bash
# Check logs
docker-compose logs [service-name]

# Try restarting
docker-compose restart [service-name]

# Clean up and restart
docker-compose down
docker-compose up -d
```

#### PostgreSQL Permission Error
```bash
# Fix permissions
sudo chown -R $USER:$USER ./dev-servers/
chmod -R u+w ./dev-servers/
```

#### Memory Issues
```bash
# Start only specific services
docker-compose up -d postgres redis

# Monitor resource usage
docker stats
```

#### Network Issues
```bash
# Verify network exists
docker network ls | grep servers

# Recreate network if needed
docker-compose down
docker-compose up -d
```

---

## 📚 Documentation

### Project Documentation

- **[CLAUDE.md](CLAUDE.md)** - Project overview and architecture
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Detailed changelog of all updates
- **[TEST_REPORT.md](TEST_REPORT.md)** - Comprehensive test results and verification
- **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** - Current status and troubleshooting
- **[FINAL_DEPLOYMENT_SUMMARY.md](FINAL_DEPLOYMENT_SUMMARY.md)** - Complete deployment guide
- **[VARIABLE_NAMING_UPDATE.md](VARIABLE_NAMING_UPDATE.md)** - LLM variable configuration

### External Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Ontotext GraphDB](https://www.ontotext.com/products/graphdb/)
- [N8N Documentation](https://docs.n8n.io/)
- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Ollama Cloud API](https://ollama.com/api)

---

## 📊 Service Versions

| Service | Version | Released | Image |
|---------|---------|----------|-------|
| PostgreSQL | 17-alpine | 2024 | `docker.io/postgres:17-alpine` |
| Redis | 8-alpine | 2024 | `docker.io/redis:8-alpine` |
| RabbitMQ | 4.4-management-alpine | 2024 | `docker.io/rabbitmq:4.4-management-alpine` |
| Neo4j | 2026-community | 2026 | `docker.io/neo4j:2026-community` |
| GraphDB | 11.5.1 | 2024 | `docker.io/ontotext/graphdb:11.5.1` |
| RustFS | latest | - | `rustfs/rustfs:latest` |
| N8N | 2.28.2 | 2024 | `n8nio/n8n:2.28.2-amd64` |
| Hindsight | latest | - | `ghcr.io/vectorize-io/hindsight:latest` |
| Dozzle | latest | - | `amir20/dozzle:latest` |
| Nginx | stable-alpine | 2024 | `nginx:stable-alpine` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add or modify services in `docker-compose.yml`
4. Update relevant documentation
5. Test your changes thoroughly
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## 📝 Git Workflow

```bash
# Clone repository
git clone <repository-url>
cd servers

# Create feature branch
git checkout -b feature/your-feature

# Make changes
# ... edit files ...

# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new service or update"

# Push to remote
git push origin feature/your-feature

# Create pull request
# (via GitHub/GitLab web interface)
```

---

## ✅ Quick Checklist

- [ ] Python 3 installed
- [ ] Docker installed and running
- [ ] `fetch_images.py` executed successfully
- [ ] All services started with `docker-compose up -d`
- [ ] Services verified with `docker-compose ps`
- [ ] PostgreSQL accessible at port 5432
- [ ] Redis accessible at port 6379
- [ ] RabbitMQ management at http://localhost:15672
- [ ] Neo4j browser at http://localhost:7474
- [ ] N8N at http://localhost:5678
- [ ] Ollama API key added for Hindsight (optional)
- [ ] Hindsight activated at http://localhost:8080 (optional)

---

## 🎯 Next Steps

### For Development
1. Set up IDE/editor connections to PostgreSQL
2. Configure N8N workflows
3. Create Neo4j graph queries
4. Build applications using Redis cache

### For Production
1. Update all default credentials
2. Set up SSL/TLS certificates
3. Configure backup procedures
4. Implement monitoring and alerting
5. Set up log aggregation

### For Learning
1. Explore PostgreSQL multi-schema design
2. Experiment with Neo4j graph queries
3. Test RabbitMQ message patterns
4. Build N8N automation workflows
5. Integrate Hindsight agent memory

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support & Feedback

For issues, questions, or suggestions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review project [documentation](#-documentation)
3. Check Docker logs: `docker-compose logs [service]`
4. Create an issue with detailed information

---

**Last Updated:** 2026-11-20  
**Status:** ✅ All Services Operational & Documented  

🚀 **Happy Developing!**
