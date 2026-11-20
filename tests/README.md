# Development Server Test Suites

Comprehensive unit test suites for all development services: RustFS, Redis, and PostgreSQL.

**Location:** `tests/`

---

## Overview

Three complete test suites covering:

### **RustFS (Object Storage)** - 18 tests
- ✅ S3-compatible API operations
- ✅ Connection and configuration
- ✅ Writing text, JSON, and binary files
- ✅ Reading and verifying objects
- ✅ Object metadata handling
- ✅ Object listing and deletion
- ✅ Large file support (1MB+)

### **Redis (Cache Store)** - 24 tests
- ✅ Connection and ping
- ✅ String operations (GET, SET, INCR, APPEND)
- ✅ List operations (PUSH, POP, RANGE)
- ✅ Hash operations (HSET, HGET, HDEL)
- ✅ Set operations (SADD, SREM, MEMBERS)
- ✅ Key management (TTL, EXPIRE, RENAME)
- ✅ JSON storage and retrieval
- ✅ Pipeline operations (batch commands)

### **PostgreSQL (Relational Database)** - 22 tests
- ✅ Connection and configuration
- ✅ Table operations and schema
- ✅ CRUD operations (Insert, Select, Update, Delete)
- ✅ Complex queries (WHERE, GROUP BY, ORDER BY, LIMIT)
- ✅ Aggregate functions (COUNT, AVG, MAX, MIN)
- ✅ Transaction handling (Commit, Rollback)
- ✅ Data types (Boolean, Numeric, String, DateTime)
- ✅ Index operations

---

## Project Structure

```
tests/
├── requirements.txt              # All dependencies (pytest, boto3, redis, sqlalchemy)
├── README.md                     # This file
├── test_rustfs/                  # RustFS S3 object storage tests
│   ├── __init__.py
│   ├── conftest.py               # Fixtures: S3 client, test bucket
│   └── test_object_store.py      # 18 test cases
├── test_redis/                   # Redis cache store tests
│   ├── __init__.py
│   ├── conftest.py               # Fixtures: Redis client, cleanup
│   └── test_cache_operations.py  # 24 test cases
└── test_postgres/                # PostgreSQL database tests
    ├── __init__.py
    ├── conftest.py               # Fixtures: Engine, session, test tables
    └── test_database_operations.py # 22 test cases
```

---

## Setup

### 1. Install Dependencies

```bash
# Navigate to tests directory
cd tests/

# Install required packages
pip install -r requirements.txt
# OR
python -m pip install -r requirements.txt
```

### 2. Ensure RustFS is Running

```bash
# From project root
docker-compose up -d rustfs

# Verify RustFS is accessible
docker-compose ps | grep rustfs
```

### 3. Configure Environment

The tests use environment variables from `.env`:

```env
RUSTFS_ENDPOINT_URL=http://localhost:9000
RUSTFS_ROOT_USER=minio
RUSTFS_ROOT_PASSWORD=minio123
RUSTFS_BUCKET=test-bucket
```

These are configured automatically from the project's `.env` file.

---

## Running Tests

### Run All Tests

```bash
# All tests across all services
pytest tests/ -v

# All tests for a specific service
pytest test_rustfs/ -v
pytest test_redis/ -v
pytest test_postgres/ -v
```

### Run Specific Test Class

```bash
# RustFS tests
pytest test_rustfs/test_object_store.py::TestRustFSConnection -v
pytest test_rustfs/test_object_store.py::TestRustFSWriteOperations -v

# Redis tests
pytest test_redis/test_cache_operations.py::TestRedisConnection -v
pytest test_redis/test_cache_operations.py::TestRedisStringOperations -v

# PostgreSQL tests
pytest test_postgres/test_database_operations.py::TestPostgresConnection -v
pytest test_postgres/test_database_operations.py::TestPostgresCRUDOperations -v
```

### Run Specific Test

```bash
pytest test_rustfs/test_object_store.py::TestRustFSWriteOperations::test_write_text_file -v
```

### Run with Coverage

```bash
pytest test_rustfs/ --cov=test_rustfs --cov-report=html
```

### Run with Detailed Output

```bash
pytest test_rustfs/ -vv -s
```

---

## Test Classes by Service

### RustFS Object Storage (18 tests)

**TestRustFSConnection** - Connection validation
```
✓ test_s3_client_created       # S3 client initialization
✓ test_rustfs_config_loaded    # Configuration loading
✓ test_bucket_accessible       # Bucket accessibility
```

**TestRustFSWriteOperations** - Writing operations
```
✓ test_write_text_file         # Write text file
✓ test_write_json_file         # Write JSON file
✓ test_write_binary_file       # Write binary file
✓ test_write_with_metadata     # Write with metadata
```

**TestRustFSReadOperations** - Reading operations
```
✓ test_read_text_file          # Read text file
✓ test_read_json_file          # Read and parse JSON
✓ test_read_binary_file        # Read binary file
✓ test_read_nonexistent_file   # Error handling
✓ test_read_with_metadata      # Read and verify metadata
```

**TestRustFSObjectManagement** - Object lifecycle
```
✓ test_list_objects            # List bucket contents
✓ test_delete_object           # Delete object
✓ test_object_exists           # Check existence
✓ test_get_object_size         # Get object size
```

**TestRustFSLargeFiles** - Large file support
```
✓ test_write_read_large_text   # 1MB file handling
✓ test_write_read_binary_stream # Binary stream handling
```

---

### Redis Cache Store (24 tests)

**TestRedisConnection** - Connection validation
```
✓ test_redis_client_created    # Client initialization
✓ test_redis_ping              # Ping test
✓ test_redis_config_loaded     # Configuration loading
```

**TestRedisStringOperations** - String data type
```
✓ test_set_and_get_string      # SET/GET operations
✓ test_set_with_expiration     # SETEX with TTL
✓ test_delete_key              # DEL operation
✓ test_get_nonexistent_key     # Non-existent key handling
✓ test_increment_counter       # INCR operation
✓ test_append_to_string        # APPEND operation
✓ test_mset_mget_multiple      # MSET/MGET operations
```

**TestRedisListOperations** - List data type
```
✓ test_push_and_pop_list       # PUSH/POP operations
✓ test_list_length             # LLEN operation
✓ test_get_list_range          # LRANGE operation
✓ test_list_index              # LINDEX operation
```

**TestRedisHashOperations** - Hash data type
```
✓ test_set_and_get_hash_field  # HSET/HGET operations
✓ test_set_multiple_fields     # Multiple field operations
✓ test_hash_field_exists       # HEXISTS operation
✓ test_delete_hash_field       # HDEL operation
✓ test_get_all_hash_fields     # HGETALL operation
✓ test_hash_length             # HLEN operation
```

**TestRedisSetOperations** - Set data type
```
✓ test_add_and_members_set     # SADD/SMEMBERS operations
✓ test_check_set_membership    # SISMEMBER operation
✓ test_remove_from_set         # SREM operation
✓ test_set_cardinality         # SCARD operation
```

**TestRedisKeyManagement** - Key management
```
✓ test_key_exists              # EXISTS operation
✓ test_get_keys_pattern        # KEYS pattern matching
✓ test_key_ttl                 # TTL operation
✓ test_set_key_ttl             # EXPIRE operation
✓ test_rename_key              # RENAME operation
```

**TestRedisJSONStorage** - JSON operations
```
✓ test_store_and_retrieve_json # JSON storage
✓ test_store_nested_json       # Nested JSON handling
```

**TestRedisPipelineOperations** - Batch operations
```
✓ test_pipeline_multiple_commands # Pipeline execution
✓ test_pipeline_atomic_operations # Atomic batch operations
```

---

### PostgreSQL Database (22 tests)

**TestPostgresConnection** - Connection validation
```
✓ test_database_connection     # Connection test
✓ test_postgres_version        # Version retrieval
✓ test_postgres_config_loaded  # Configuration loading
```

**TestPostgresTableOperations** - Schema operations
```
✓ test_create_table            # CREATE TABLE
✓ test_table_columns           # Column verification
```

**TestPostgresCRUDOperations** - CRUD operations
```
✓ test_insert_single_record    # INSERT single
✓ test_insert_multiple_records # INSERT multiple
✓ test_select_all_records      # SELECT all
✓ test_select_with_where       # SELECT with WHERE
✓ test_update_record           # UPDATE operation
✓ test_delete_record           # DELETE operation
```

**TestPostgresQueryOperations** - Query operations
```
✓ test_aggregate_functions     # COUNT, AVG, MAX, MIN
✓ test_group_by                # GROUP BY clause
✓ test_order_by                # ORDER BY clause
✓ test_limit_offset            # LIMIT/OFFSET clauses
```

**TestPostgresTransactions** - Transaction handling
```
✓ test_transaction_commit      # COMMIT operation
✓ test_transaction_rollback    # ROLLBACK operation
```

**TestPostgresDataTypes** - Data type support
```
✓ test_boolean_type            # BOOLEAN support
✓ test_numeric_types           # INT, FLOAT support
✓ test_string_type             # VARCHAR support
✓ test_datetime_type           # TIMESTAMP support
```

**TestPostgresIndexes** - Index operations
```
✓ test_create_index            # CREATE INDEX
```

---

## Configuration Details

### Environment Variables Required

**RustFS:**
```env
RUSTFS_ENDPOINT_URL=http://localhost:9000
RUSTFS_ROOT_USER=minio
RUSTFS_ROOT_PASSWORD=minio123
RUSTFS_BUCKET=test-bucket
```

**Redis:**
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**PostgreSQL:**
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=devServer@1
POSTGRES_DB=postgres
```

### RustFS Fixtures

**rustfs_config** (session scope)
- Configuration from environment variables
- Returns: endpoint_url, access_key, secret_key, region_name, bucket

**s3_client** (session scope)
- boto3 S3 client configured for RustFS

**test_bucket** (function scope)
- Auto-creates/cleans test bucket per test
- Idempotent: creates if missing

**sample_data** (function scope)
- Provides text, JSON, and binary test objects

### Redis Fixtures

**redis_config** (session scope)
- Configuration from environment variables
- Returns: host, port, db, decode_responses

**redis_client** (session scope)
- Redis client instance with connection validation

**cleanup_redis** (autouse)
- Auto-cleanup after each test
- Removes all keys matching test pattern

**sample_data** (function scope)
- Provides test data for strings, lists, hashes, sets

### PostgreSQL Fixtures

**postgres_config** (session scope)
- Configuration from environment variables
- Returns: host, port, user, password, database

**engine** (session scope)
- SQLAlchemy engine for PostgreSQL
- Connection validation on creation

**session_factory** (session scope)
- SQLAlchemy session factory for ORM operations

**db_session** (function scope)
- Database session per test with rollback

**test_table** (function scope)
- Auto-creates/drops test table schema
- Provides Users table with CRUD operations

**raw_connection** (function scope)
- Raw database connection for direct SQL

**sample_users** (function scope)
- Provides sample user data for testing

---

## Test Data

### Sample Objects

| Name | Type | Size | Content |
|------|------|------|---------|
| sample.txt | Text | ~38 bytes | "Hello, RustFS! This is a test file." |
| sample.json | JSON | ~63 bytes | {name, type, status} |
| sample.bin | Binary | 4 bytes | Binary content with null bytes |

---

## Example Test Output

```
tests/test_rustfs/test_object_store.py::TestRustFSConnection::test_s3_client_created PASSED
tests/test_rustfs/test_object_store.py::TestRustFSConnection::test_rustfs_config_loaded PASSED
tests/test_rustfs/test_object_store.py::TestRustFSConnection::test_bucket_accessible PASSED
tests/test_rustfs/test_object_store.py::TestRustFSWriteOperations::test_write_text_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSWriteOperations::test_write_json_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSWriteOperations::test_write_binary_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSWriteOperations::test_write_with_metadata PASSED
tests/test_rustfs/test_object_store.py::TestRustFSReadOperations::test_read_text_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSReadOperations::test_read_json_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSReadOperations::test_read_binary_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSReadOperations::test_read_nonexistent_file PASSED
tests/test_rustfs/test_object_store.py::TestRustFSReadOperations::test_read_with_metadata PASSED
tests/test_rustfs/test_object_store.py::TestRustFSObjectManagement::test_list_objects PASSED
tests/test_rustfs/test_object_store.py::TestRustFSObjectManagement::test_delete_object PASSED
tests/test_rustfs/test_object_store.py::TestRustFSObjectManagement::test_object_exists PASSED
tests/test_rustfs/test_object_store.py::TestRustFSObjectManagement::test_get_object_size PASSED
tests/test_rustfs/test_object_store.py::TestRustFSLargeFiles::test_write_read_large_text PASSED
tests/test_rustfs/test_object_store.py::TestRustFSLargeFiles::test_write_read_binary_stream PASSED

========================= 18 passed in 2.34s ==========================
```

---

## Troubleshooting

### RustFS Connection Failed

**Error:** `Connection refused` or `Failed to establish connection`

**Solution:**
1. Verify RustFS is running: `docker-compose ps | grep rustfs`
2. Check endpoint URL: `http://localhost:9000`
3. Restart RustFS: `docker-compose restart rustfs`

### Authentication Failed

**Error:** `InvalidAccessKeyId` or `SignatureDoesNotMatch`

**Solution:**
1. Verify credentials in `.env`:
   - `RUSTFS_ROOT_USER=minio`
   - `RUSTFS_ROOT_PASSWORD=minio123`
2. Ensure `.env` file exists and is loaded
3. Check RustFS credentials haven't changed

### Bucket Not Found

**Error:** `NoSuchBucket`

**Solution:**
1. Test bucket is created automatically via fixture
2. Verify bucket name in `.env`: `RUSTFS_BUCKET=test-bucket`
3. Check RustFS bucket creation permissions

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: RustFS Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      rustfs:
        image: rustfs/rustfs:latest
        options: >-
          --health-cmd "curl -f http://localhost:9000 || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 9000:9000

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r tests/requirements.txt
      - run: cd tests && pytest test_rustfs/ -v
```

---

## Adding New Tests

### Template for New Test

```python
class TestNewFeature:
    """Test description."""

    def test_new_operation(self, s3_client, test_bucket, sample_data):
        """Test description."""
        # Arrange
        key = "test/new-object.txt"
        data = "test data"
        
        # Act
        s3_client.put_object(Bucket=test_bucket, Key=key, Body=data)
        response = s3_client.get_object(Bucket=test_bucket, Key=key)
        
        # Assert
        assert response["Body"].read().decode() == data
```

---

## References

- **boto3 S3 Documentation:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
- **pytest Documentation:** https://docs.pytest.org/
- **RustFS GitHub:** https://github.com/vectorize-io/rustfs
- **S3 API Reference:** https://docs.aws.amazon.com/AmazonS3/latest/API/

---

## License

Same as parent project.

---

**Last Updated:** 2026-11-20  
**Total Test Count:** 64 test cases
- **RustFS:** 18 tests (S3 object storage)
- **Redis:** 24 tests (cache operations)
- **PostgreSQL:** 22 tests (database operations)

**Coverage:**
- Connection & configuration validation
- Read/Write/Delete operations
- Data type support (strings, lists, hashes, sets, etc.)
- Advanced features (transactions, indexes, pipelines)
- Large file support
- Error handling
