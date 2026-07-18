# Development Servers Stack

A comprehensive Docker Compose setup for running multiple development and services locally. Perfect for development, testing, and learning environments.

## 🚀 Quick Start

```bash
# Download required Docker images
$ python fetch_images.py

# Start all active services
$ docker-compose up -d

# View logs
$ docker-compose logs -f

# Stop all services
$ docker-compose down
```

## 📋 Prerequisites

- **Python 3** - For the image download script
- **Docker** or **Podman** - With docker compose support
- **Git** - For version control

## 🏗️ Architecture

All services run on a custom bridge network called `servers` for secure inter-service communication.

## 🗄️ Active Services

| Service | Port(s) | Description | Web UI |
|---------|---------|-------------|--------|
| **Dozzle** | 8888 | Local Container log viewer | [http://localhost:8888/](http://localhost:8888/) | 
| **Elasticsearch** | 9200, 9300 | Search and Analytics Engine | - |
| **Kibana** | 5601 | Visualization Tool for Elasticsearch | [http://localhost:5601](http://localhost:5601) |
| **Nginx** | 80, 443 | Reverse Proxy and Load Balancer | [http://localhost](http://localhost) |
| **Grafana** | 3000 | Metrics Visualization and Monitoring | [http://localhost:3000](http://localhost:3000) |
| **Neo4j** | 7474, 7687 | Graph Database | [http://localhost:7474](http://localhost:7474) |
| **PostgreSQL** | 5432 | Relational Database | - |
| **PgVector** | 5433 | PostgreSQL with Vector Extension | - |
| **Redis Stack Server** | 6379, 8001 | In-memory Cache + UI | [http://localhost:8001](http://localhost:8001) |
| **RabbitMQ** | 5672, 15672 | Message Queue + Management | [http://localhost:15672](http://localhost:15672) |
| **MongoDB** | 27017 | NoSQL Document Database | - |

## 🔧 Additional Services

The following services are also available and can be activated as needed:

| Service | Port(s) | Description | Web UI |
|---------|---------|-------------|--------|
| **N8N** | 5678 | Workflow Automation | [http://localhost:5678](http://localhost:5678) |
| **MinIO** | 9000, 9001 | S3-compatible Storage | [http://localhost:9001](http://localhost:9001) |
| **Ollama** | 11435 | AI/ML Model Server | - |

## 🌐 Service URLs & Endpoints

### Search & Analytics
- **Elasticsearch**: http://localhost:9200
  - Health check: `curl http://localhost:9200/_cluster/health`
- **Kibana Dashboard**: http://localhost:5601
  - Elasticsearch data visualization and management

### Monitoring & Proxy
- **Nginx**: http://localhost
  - Serves as reverse proxy for all services
- **Grafana**: http://localhost:3000
  - Default credentials: `admin` / `admin`

### Databases
- **Neo4j Browser**: http://localhost:7474
  - Default credentials: `neo4j` / `devServer@1`
- **PostgreSQL**: `postgresql://postgres:devServer@1@localhost:5432/postgres`
- **PgVector**: `postgresql://postgres:devServer@1@localhost:5433/postgres`
- **MongoDB**: `mongodb://mongoadmin:SuperSecurePassw0rd@localhost:27017`

### Message Queue
- **RabbitMQ Management UI**: http://localhost:15672
  - Default credentials: `rmquser` / `SuperSecurePassw0rd`
- **RabbitMQ Server**: `amqp://rmquser:SuperSecurePassw0rd@localhost:5672`

### Cache & Search
- **Redis CLI**: `redis-cli -p 6379`
- **Redis Stack UI**: http://localhost:8001

## ⚙️ Configuration

All services can be configured through environment variables in the `.env` file:

```bash
# Example: Change Neo4j port
NEO4J_PORT=7475

# Example: Change PostgreSQL password
POSTGRES_PASSWORD=YourSecurePassword
```

### Key Configuration Files
- `docker-compose.yml` - Service definitions and orchestration
- `.env` - Environment variables and configuration
- `fetch_images.py` - Docker image download script

## 📁 Data Persistence

All service data is persisted in the `./dev-servers/` directory:

```
dev-servers/
├── elasticsearch/  # Elasticsearch data and config
├── kibana/         # Kibana data
├── nginx/          # Nginx config, html, and logs
├── grafana/        # Grafana data and provisioning
├── neo4j/          # Neo4j data, logs, config
├── postgres/       # PostgreSQL data
├── pgvector/       # PgVector data
├── redis-stack-server/  # Redis Stack Server data
├── rabbitmq/       # RabbitMQ data
├── mongo/          # MongoDB data
├── n8n/            # N8N workflow data
├── minio/          # MinIO object storage data
└── ollama/         # Ollama model data
```

## 🔍 Monitoring & Management

### Health Checks
```bash
# Check service status
$ docker-compose ps

# View service logs
$ docker-compose logs [service-name]

# Follow logs in real-time
$ docker-compose logs -f [service-name]
```

### Common Commands
```bash
# Restart specific service
$ docker-compose restart postgres

# Scale services (if supported)
$ docker-compose up -d --scale postgres=2

# Execute commands in containers
$ docker-compose exec postgres psql -U postgres
```

## 🔒 Security Notes

- Default passwords are provided for development convenience
- **Always change passwords in production environments**
- Services are exposed to localhost only by default
- Consider using Docker secrets for sensitive data in production

## 🐛 Troubleshooting

### Port Conflicts
If ports are already in use, modify them in `.env`:
```bash
POSTGRES_PORT=5433
REDIS_PORT=6380
```

### Permission Issues
```bash
# Fix volume permissions on Linux
sudo chown -R $USER:$USER ./dev-servers/
```

### Memory Issues
For systems with limited RAM, start services selectively:
```bash
# Start only specific services
$ docker-compose up -d postgres redis
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add or modify services in `docker-compose.yml`
4. Update documentation
5. Submit a pull request

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🚀 Happy Developing!**
