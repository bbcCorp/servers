#!/bin/sh

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Using docker to pull images from .env configuration"
echo ""

# Pull database images
echo "Pulling Neo4j ${NEO4J_IMAGE}..."
docker pull "${NEO4J_IMAGE}"

echo "Pulling Postgres ${POSTGRES_IMAGE}..."
docker pull "${POSTGRES_IMAGE}"

echo "Pulling PgVector ${PGVECTOR_IMAGE}..."
docker pull "${PGVECTOR_IMAGE}"

echo "Pulling Redis ${REDIS_IMAGE}..."
docker pull "${REDIS_IMAGE}"

echo "Pulling RabbitMQ ${RABBITMQ_IMAGE}..."
docker pull "${RABBITMQ_IMAGE}"

echo "Pulling MongoDB ${MONGO_IMAGE}..."
docker pull "${MONGO_IMAGE}"

# Pull application images
echo "Pulling n8n ${N8N_IMAGE}..."
docker pull "${N8N_IMAGE}"

echo "Pulling MinIO ${MINIO_IMAGE}..."
docker pull "${MINIO_IMAGE}"

echo "Pulling Ollama..."
docker pull ollama/ollama:latest

# Pull development runtime images
echo "Pulling Python ${PYTHON_IMAGE}..."
docker pull "${PYTHON_IMAGE}"

echo "Pulling .NET SDK 8.0 ${DOTNET_SDK_8_IMAGE}..."
docker pull "${DOTNET_SDK_8_IMAGE}"

echo "Pulling .NET SDK 9.0 ${DOTNET_SDK_9_IMAGE}..."
docker pull "${DOTNET_SDK_9_IMAGE}"

echo "Pulling .NET ASP.NET 8.0 ${DOTNET_ASPNET_8_IMAGE}..."
docker pull "${DOTNET_ASPNET_8_IMAGE}"

echo "Pulling .NET ASP.NET 9.0 ${DOTNET_ASPNET_9_IMAGE}..."
docker pull "${DOTNET_ASPNET_9_IMAGE}"

echo ""
echo "All images pulled successfully!"
