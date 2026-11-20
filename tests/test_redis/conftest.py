"""
Pytest fixtures for Redis testing.
Provides Redis client and configuration.
"""

import os
import pytest
import redis
from dotenv import load_dotenv

# Load environment variables from parent .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


@pytest.fixture(scope="session")
def redis_config():
    """
    Provides Redis configuration from environment variables.

    Returns:
        dict: Redis connection configuration
    """
    return {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "db": int(os.getenv("REDIS_DB", "0")),
        "decode_responses": True,
    }


@pytest.fixture(scope="session")
def redis_client(redis_config):
    """
    Provides Redis client.

    Args:
        redis_config: Redis configuration

    Returns:
        redis.Redis: Redis client instance
    """
    client = redis.Redis(
        host=redis_config["host"],
        port=redis_config["port"],
        db=redis_config["db"],
        decode_responses=redis_config["decode_responses"],
    )

    # Test connection
    client.ping()

    return client


@pytest.fixture(autouse=True)
def cleanup_redis(redis_client):
    """
    Cleans up Redis after each test.
    Removes all keys used in tests.
    """
    yield

    # Cleanup: Remove all keys matching test pattern
    keys = redis_client.keys("test:*")
    if keys:
        redis_client.delete(*keys)


@pytest.fixture(scope="function")
def sample_data():
    """
    Provides sample data for testing.

    Returns:
        dict: Sample data objects
    """
    return {
        "string": {
            "key": "test:string",
            "value": "Hello, Redis!",
        },
        "counter": {
            "key": "test:counter",
            "value": 42,
        },
        "json": {
            "key": "test:json",
            "value": '{"name": "Redis", "type": "cache", "status": "active"}',
        },
        "list": {
            "key": "test:list",
            "values": ["item1", "item2", "item3"],
        },
        "hash": {
            "key": "test:hash",
            "data": {
                "name": "Test User",
                "email": "test@example.com",
                "age": "30",
            },
        },
        "set": {
            "key": "test:set",
            "values": {"tag1", "tag2", "tag3"},
        },
    }
