# Servers in a Bottle
Running servers locally using Docker containers

## Prerequisites
- `Python 3`
- `Docker` or `Podman` along with `docker compose` command


## Running local servers using Docker
```bash
# Download the images
$ python fetch_images.py

# Bring up the servers
$ docker-compose -f ./docker-compose.yml up 
```

## Server urls

| Server | Endpoint |
| --- | --- |
| n8n | http://localhost:5678 | 
| RMQ Management UI | http://localhost:15672/ | 
| RMQ Server | amqp://localhost:5672/ |
| MinIO Console | http://localhost:9001/ |