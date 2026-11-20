# RustFS Object Store Tests

Comprehensive unit test suite for RustFS S3-compatible object storage operations.

**Location:** `tests/test_rustfs/`

---

## Overview

This test suite validates RustFS read/write operations using boto3 S3 client. Tests cover:

- ✅ Connection and configuration
- ✅ Writing text, JSON, and binary files
- ✅ Reading and verifying objects
- ✅ Object metadata handling
- ✅ Object listing and deletion
- ✅ Large file handling

---

## Project Structure

```
tests/
├── requirements.txt              # Test dependencies
├── README.md                     # This file
└── test_rustfs/
    ├── __init__.py              # Package marker
    ├── conftest.py              # Pytest fixtures and configuration
    └── test_object_store.py     # Test cases
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
pytest test_rustfs/ -v
```

### Run Specific Test Class

```bash
# Test connection
pytest test_rustfs/test_object_store.py::TestRustFSConnection -v

# Test write operations
pytest test_rustfs/test_object_store.py::TestRustFSWriteOperations -v

# Test read operations
pytest test_rustfs/test_object_store.py::TestRustFSReadOperations -v
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

## Test Classes

### TestRustFSConnection
Tests basic connectivity and configuration.

```python
✓ test_s3_client_created       # Verify S3 client initialization
✓ test_rustfs_config_loaded    # Verify configuration loaded
✓ test_bucket_accessible       # Verify test bucket accessibility
```

### TestRustFSWriteOperations
Tests writing various data types.

```python
✓ test_write_text_file         # Write text file
✓ test_write_json_file         # Write JSON file
✓ test_write_binary_file       # Write binary file
✓ test_write_with_metadata     # Write with custom metadata
```

### TestRustFSReadOperations
Tests reading and retrieving objects.

```python
✓ test_read_text_file          # Read text file
✓ test_read_json_file          # Read and parse JSON
✓ test_read_binary_file        # Read binary file
✓ test_read_nonexistent_file   # Verify error on missing object
✓ test_read_with_metadata      # Read and verify metadata
```

### TestRustFSObjectManagement
Tests object lifecycle operations.

```python
✓ test_list_objects            # List bucket contents
✓ test_delete_object           # Delete object
✓ test_object_exists           # Check object existence
✓ test_get_object_size         # Get object size
```

### TestRustFSLargeFiles
Tests handling of larger files.

```python
✓ test_write_read_large_text   # Write/read 1MB file
✓ test_write_read_binary_stream # Write/read binary stream
```

---

## Configuration Details

### Fixtures

**rustfs_config** (session scope)
- Provides RustFS configuration from environment variables
- Returns dict with endpoint_url, access_key, secret_key, region_name, bucket

**s3_client** (session scope)
- Provides boto3 S3 client configured for RustFS
- Uses environment credentials

**test_bucket** (function scope)
- Creates test bucket for each test
- Cleans up after test completes
- Idempotent: creates bucket if missing

**sample_data** (function scope)
- Provides sample data for testing
- Includes text, JSON, and binary objects

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
**Test Count:** 18 test cases  
**Coverage:** Connection, Write, Read, Management, Large Files
