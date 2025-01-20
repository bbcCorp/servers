echo "Using docker to pull images"

# Pull server images
docker pull docker.io/neo4j:5.25-community
docker pull docker.io/elasticsearch:8.16.0
docker pull docker.io/postgres:17-bullseye
docker pull docker.io/redis:7.4-alpine
docker pull docker.io/rabbitmq:4-alpine

# Pull app layer images
docker pull docker.io/python:3.13-bullseye
docker pull mcr.microsoft.com/dotnet/sdk:8.0
docker pull mcr.microsoft.com/dotnet/sdk:9.0
docker pull mcr.microsoft.com/dotnet/aspnet:8.0
docker pull mcr.microsoft.com/dotnet/aspnet:9.0