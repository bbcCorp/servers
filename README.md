# Servers in a Bottle
Running servers locally using Docker containers

## Prerequisites

1. Setup the `SERVER_HOME` variable to the path of the `server` project
2. Have Docker installed.


## Running local servers using Docker
```bash
# Download the images
$ sh fetch_images.sh

# Bring up the servers
$ docker-compose -f ./docker-compose.yml up 
```
