"""
Unit tests for Redis cache operations.
Tests read/write operations to the Redis cache store.
"""

import pytest
import json
import time


class TestRedisConnection:
    """Test Redis connectivity and configuration."""

    def test_redis_client_created(self, redis_client):
        """Verify Redis client is properly configured."""
        assert redis_client is not None
        assert hasattr(redis_client, "get")
        assert hasattr(redis_client, "set")
        assert hasattr(redis_client, "delete")

    def test_redis_ping(self, redis_client):
        """Verify Redis connection with ping."""
        result = redis_client.ping()
        assert result is True

    def test_redis_config_loaded(self, redis_config):
        """Verify Redis configuration is loaded."""
        assert redis_config["host"]
        assert redis_config["port"]
        assert redis_config["db"] >= 0


class TestRedisStringOperations:
    """Test Redis string operations (GET, SET, DELETE)."""

    def test_set_and_get_string(self, redis_client, sample_data):
        """Test setting and getting a string value."""
        data = sample_data["string"]

        # Set value
        redis_client.set(data["key"], data["value"])

        # Get value
        result = redis_client.get(data["key"])

        assert result == data["value"]

    def test_set_with_expiration(self, redis_client):
        """Test setting a value with expiration."""
        key = "test:expiring"
        value = "temporary"

        # Set with 1 second expiration
        redis_client.setex(key, 1, value)

        # Verify value exists
        assert redis_client.get(key) == value

        # Wait for expiration
        time.sleep(1.1)

        # Verify value is gone
        assert redis_client.get(key) is None

    def test_delete_key(self, redis_client, sample_data):
        """Test deleting a key."""
        data = sample_data["string"]

        # Set value
        redis_client.set(data["key"], data["value"])
        assert redis_client.exists(data["key"]) == 1

        # Delete key
        result = redis_client.delete(data["key"])
        assert result == 1
        assert redis_client.exists(data["key"]) == 0

    def test_get_nonexistent_key(self, redis_client):
        """Test getting a non-existent key returns None."""
        result = redis_client.get("test:nonexistent")
        assert result is None

    def test_increment_counter(self, redis_client):
        """Test incrementing a counter value."""
        key = "test:counter"

        # Initialize counter
        redis_client.set(key, 0)

        # Increment multiple times
        redis_client.incr(key)
        redis_client.incr(key)
        redis_client.incr(key)

        # Verify count
        assert redis_client.get(key) == "3"

    def test_append_to_string(self, redis_client):
        """Test appending to a string value."""
        key = "test:append"

        # Set initial value
        redis_client.set(key, "Hello")

        # Append to value
        redis_client.append(key, " World")

        # Verify result
        assert redis_client.get(key) == "Hello World"

    def test_mset_mget_multiple_keys(self, redis_client):
        """Test setting and getting multiple keys at once."""
        keys_values = {
            "test:key1": "value1",
            "test:key2": "value2",
            "test:key3": "value3",
        }

        # Set multiple keys
        redis_client.mset(keys_values)

        # Get multiple keys
        keys = list(keys_values.keys())
        results = redis_client.mget(keys)

        # Verify results
        assert results == list(keys_values.values())


class TestRedisListOperations:
    """Test Redis list operations."""

    def test_push_and_pop_list(self, redis_client):
        """Test pushing and popping list items."""
        key = "test:list"

        # Push items
        redis_client.rpush(key, "item1", "item2", "item3")

        # Pop items
        item1 = redis_client.lpop(key)
        item2 = redis_client.lpop(key)

        assert item1 == "item1"
        assert item2 == "item2"

    def test_list_length(self, redis_client):
        """Test getting list length."""
        key = "test:list"

        # Push items
        redis_client.rpush(key, "a", "b", "c", "d")

        # Get length
        length = redis_client.llen(key)

        assert length == 4

    def test_get_list_range(self, redis_client):
        """Test getting a range of list items."""
        key = "test:list"

        # Push items
        redis_client.rpush(key, "a", "b", "c", "d", "e")

        # Get range
        items = redis_client.lrange(key, 1, 3)

        assert items == ["b", "c", "d"]

    def test_list_index(self, redis_client):
        """Test getting item by index."""
        key = "test:list"

        # Push items
        redis_client.rpush(key, "first", "second", "third")

        # Get by index
        item = redis_client.lindex(key, 1)

        assert item == "second"


class TestRedisHashOperations:
    """Test Redis hash operations."""

    def test_set_and_get_hash_field(self, redis_client):
        """Test setting and getting hash fields."""
        key = "test:hash"
        field = "name"
        value = "Test User"

        # Set field
        redis_client.hset(key, field, value)

        # Get field
        result = redis_client.hget(key, field)

        assert result == value

    def test_set_multiple_hash_fields(self, redis_client):
        """Test setting multiple hash fields at once."""
        key = "test:hash"
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": "30",
        }

        # Set all fields
        redis_client.hset(key, mapping=data)

        # Get all fields
        result = redis_client.hgetall(key)

        assert result == data

    def test_hash_field_exists(self, redis_client):
        """Test checking if hash field exists."""
        key = "test:hash"
        field = "status"

        # Set field
        redis_client.hset(key, field, "active")

        # Check existence
        exists = redis_client.hexists(key, field)

        assert exists == 1

    def test_delete_hash_field(self, redis_client):
        """Test deleting a hash field."""
        key = "test:hash"
        field = "temporary"

        # Set field
        redis_client.hset(key, field, "value")

        # Delete field
        result = redis_client.hdel(key, field)

        assert result == 1
        assert redis_client.hexists(key, field) == 0

    def test_get_all_hash_fields(self, redis_client):
        """Test getting all hash fields and values."""
        key = "test:hash"
        data = {"field1": "value1", "field2": "value2", "field3": "value3"}

        # Set fields
        redis_client.hset(key, mapping=data)

        # Get all
        result = redis_client.hgetall(key)

        assert result == data

    def test_hash_length(self, redis_client):
        """Test getting hash length."""
        key = "test:hash"

        # Set fields
        redis_client.hset(key, mapping={"a": "1", "b": "2", "c": "3"})

        # Get length
        length = redis_client.hlen(key)

        assert length == 3


class TestRedisSetOperations:
    """Test Redis set operations."""

    def test_add_and_members_set(self, redis_client):
        """Test adding items to a set and getting members."""
        key = "test:set"
        items = ["tag1", "tag2", "tag3"]

        # Add items
        redis_client.sadd(key, *items)

        # Get members
        members = redis_client.smembers(key)

        assert members == set(items)

    def test_check_set_membership(self, redis_client):
        """Test checking if item is in set."""
        key = "test:set"

        # Add items
        redis_client.sadd(key, "item1", "item2", "item3")

        # Check membership
        assert redis_client.sismember(key, "item1") == 1
        assert redis_client.sismember(key, "nonexistent") == 0

    def test_remove_from_set(self, redis_client):
        """Test removing items from set."""
        key = "test:set"

        # Add items
        redis_client.sadd(key, "a", "b", "c")

        # Remove item
        result = redis_client.srem(key, "b")

        assert result == 1
        assert redis_client.sismember(key, "b") == 0

    def test_set_cardinality(self, redis_client):
        """Test getting set size."""
        key = "test:set"

        # Add items
        redis_client.sadd(key, "x", "y", "z")

        # Get size
        size = redis_client.scard(key)

        assert size == 3


class TestRedisKeyManagement:
    """Test Redis key management operations."""

    def test_key_exists(self, redis_client):
        """Test checking if key exists."""
        key = "test:exists"

        # Set key
        redis_client.set(key, "value")

        # Check existence
        assert redis_client.exists(key) == 1
        assert redis_client.exists("nonexistent") == 0

    def test_get_keys_pattern(self, redis_client):
        """Test getting keys by pattern."""
        # Set multiple keys
        redis_client.set("test:key1", "value1")
        redis_client.set("test:key2", "value2")
        redis_client.set("test:key3", "value3")

        # Get keys by pattern
        keys = redis_client.keys("test:key*")

        assert len(keys) >= 3
        assert "test:key1" in keys
        assert "test:key2" in keys
        assert "test:key3" in keys

    def test_key_ttl(self, redis_client):
        """Test getting key TTL (time to live)."""
        key = "test:ttl"

        # Set key with expiration
        redis_client.setex(key, 100, "value")

        # Get TTL
        ttl = redis_client.ttl(key)

        # TTL should be positive and close to 100
        assert 95 <= ttl <= 100

    def test_set_key_ttl(self, redis_client):
        """Test setting TTL on existing key."""
        key = "test:set_ttl"

        # Set key
        redis_client.set(key, "value")

        # Set expiration
        redis_client.expire(key, 100)

        # Get TTL
        ttl = redis_client.ttl(key)

        assert 95 <= ttl <= 100

    def test_rename_key(self, redis_client):
        """Test renaming a key."""
        old_key = "test:old_name"
        new_key = "test:new_name"
        value = "test_value"

        # Set key
        redis_client.set(old_key, value)

        # Rename key
        redis_client.rename(old_key, new_key)

        # Verify old key gone, new key exists
        assert redis_client.exists(old_key) == 0
        assert redis_client.get(new_key) == value


class TestRedisJSONStorage:
    """Test storing and retrieving JSON in Redis."""

    def test_store_and_retrieve_json(self, redis_client):
        """Test storing and retrieving JSON objects."""
        key = "test:json"
        data = {
            "name": "Test User",
            "email": "user@example.com",
            "active": True,
            "score": 95.5,
        }

        # Store JSON
        json_str = json.dumps(data)
        redis_client.set(key, json_str)

        # Retrieve JSON
        result_str = redis_client.get(key)
        result = json.loads(result_str)

        assert result == data

    def test_store_nested_json(self, redis_client):
        """Test storing nested JSON structures."""
        key = "test:nested_json"
        data = {
            "user": {
                "name": "John",
                "details": {
                    "age": 30,
                    "city": "NYC",
                },
            },
            "metadata": ["tag1", "tag2"],
        }

        # Store JSON
        json_str = json.dumps(data)
        redis_client.set(key, json_str)

        # Retrieve JSON
        result_str = redis_client.get(key)
        result = json.loads(result_str)

        assert result == data
        assert result["user"]["details"]["city"] == "NYC"


class TestRedisPipelineOperations:
    """Test Redis pipeline operations for batch commands."""

    def test_pipeline_multiple_commands(self, redis_client):
        """Test executing multiple commands in a pipeline."""
        pipe = redis_client.pipeline()

        # Queue commands
        pipe.set("test:pipe1", "value1")
        pipe.set("test:pipe2", "value2")
        pipe.get("test:pipe1")
        pipe.get("test:pipe2")

        # Execute pipeline
        results = pipe.execute()

        # Results: [True, True, 'value1', 'value2']
        assert results[0] is True
        assert results[1] is True
        assert results[2] == "value1"
        assert results[3] == "value2"

    def test_pipeline_atomic_operations(self, redis_client):
        """Test atomic operations in pipeline."""
        key = "test:counter"

        pipe = redis_client.pipeline()

        # Queue increment operations
        for _ in range(5):
            pipe.incr(key)

        # Execute
        results = pipe.execute()

        # Verify all increments happened
        final_value = int(redis_client.get(key))
        assert final_value == 5
