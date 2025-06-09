# Servers in a Bottle
Running servers locally using Docker containers

## Prerequisites
- `Docker` or `Podman` along with `docker compose` command


## Running local servers using Docker
```bash
# Download the images
$ sh fetch_images.sh

# Bring up the servers
$ docker-compose -f ./docker-compose.yml up 
```

## Server urls

| Server | Endpoint |
| --- | --- |
| N8N | http://localhost:5678 | 
