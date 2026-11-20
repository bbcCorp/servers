"""
Unit tests for RustFS object store operations.
Tests reading and writing objects to the RustFS S3-compatible storage.
"""

import pytest
import json
from io import BytesIO


class TestRustFSConnection:
    """Test RustFS connectivity and configuration."""

    def test_s3_client_created(self, s3_client):
        """Verify S3 client is properly configured."""
        assert s3_client is not None
        assert hasattr(s3_client, "put_object")
        assert hasattr(s3_client, "get_object")
        assert hasattr(s3_client, "delete_object")

    def test_rustfs_config_loaded(self, rustfs_config):
        """Verify RustFS configuration is loaded."""
        assert rustfs_config["endpoint_url"]
        assert rustfs_config["access_key"]
        assert rustfs_config["secret_key"]
        assert rustfs_config["bucket"]

    def test_bucket_accessible(self, test_bucket, s3_client):
        """Verify test bucket is accessible."""
        response = s3_client.head_bucket(Bucket=test_bucket)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


class TestRustFSWriteOperations:
    """Test writing objects to RustFS."""

    def test_write_text_file(self, s3_client, test_bucket, sample_data):
        """Test writing a text file to RustFS."""
        text_obj = sample_data["text_file"]

        # Write object
        response = s3_client.put_object(
            Bucket=test_bucket,
            Key=text_obj["key"],
            Body=text_obj["data"],
            ContentType=text_obj["content_type"],
        )

        # Verify write
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        assert "ETag" in response

    def test_write_json_file(self, s3_client, test_bucket, sample_data):
        """Test writing a JSON file to RustFS."""
        json_obj = sample_data["json_file"]

        # Write object
        response = s3_client.put_object(
            Bucket=test_bucket,
            Key=json_obj["key"],
            Body=json_obj["data"],
            ContentType=json_obj["content_type"],
        )

        # Verify write
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def test_write_binary_file(self, s3_client, test_bucket, sample_data):
        """Test writing a binary file to RustFS."""
        bin_obj = sample_data["binary_file"]

        # Write object
        response = s3_client.put_object(
            Bucket=test_bucket,
            Key=bin_obj["key"],
            Body=bin_obj["data"],
            ContentType=bin_obj["content_type"],
        )

        # Verify write
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def test_write_with_metadata(self, s3_client, test_bucket):
        """Test writing object with custom metadata."""
        response = s3_client.put_object(
            Bucket=test_bucket,
            Key="test/with-metadata.txt",
            Body="Test content",
            Metadata={
                "custom-key": "custom-value",
                "app-version": "1.0.0",
                "environment": "test",
            },
        )

        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


class TestRustFSReadOperations:
    """Test reading objects from RustFS."""

    def test_read_text_file(self, s3_client, test_bucket, sample_data):
        """Test reading a text file from RustFS."""
        text_obj = sample_data["text_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=text_obj["key"],
            Body=text_obj["data"],
        )

        # Read object
        response = s3_client.get_object(Bucket=test_bucket, Key=text_obj["key"])
        content = response["Body"].read().decode("utf-8")

        # Verify read
        assert content == text_obj["data"]
        assert response["ContentType"] == text_obj["content_type"]

    def test_read_json_file(self, s3_client, test_bucket, sample_data):
        """Test reading and parsing a JSON file from RustFS."""
        json_obj = sample_data["json_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=json_obj["key"],
            Body=json_obj["data"],
        )

        # Read and parse
        response = s3_client.get_object(Bucket=test_bucket, Key=json_obj["key"])
        content = response["Body"].read().decode("utf-8")
        data = json.loads(content)

        # Verify read and parse
        assert data["name"] == "RustFS"
        assert data["type"] == "object store"
        assert data["status"] == "active"

    def test_read_binary_file(self, s3_client, test_bucket, sample_data):
        """Test reading a binary file from RustFS."""
        bin_obj = sample_data["binary_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=bin_obj["key"],
            Body=bin_obj["data"],
        )

        # Read object
        response = s3_client.get_object(Bucket=test_bucket, Key=bin_obj["key"])
        content = response["Body"].read()

        # Verify read
        assert content == bin_obj["data"]

    def test_read_nonexistent_file(self, s3_client, test_bucket):
        """Test reading a non-existent file raises error."""
        with pytest.raises(Exception):  # NoSuchKey error
            s3_client.get_object(Bucket=test_bucket, Key="nonexistent.txt")

    def test_read_with_metadata(self, s3_client, test_bucket):
        """Test reading object metadata."""
        key = "test/with-metadata.txt"
        metadata = {
            "custom-key": "custom-value",
            "app-version": "1.0.0",
        }

        # Write object with metadata
        s3_client.put_object(
            Bucket=test_bucket,
            Key=key,
            Body="Test content",
            Metadata=metadata,
        )

        # Read and verify metadata
        response = s3_client.get_object(Bucket=test_bucket, Key=key)
        assert response["Metadata"]["custom-key"] == "custom-value"
        assert response["Metadata"]["app-version"] == "1.0.0"


class TestRustFSObjectManagement:
    """Test object management operations."""

    def test_list_objects(self, s3_client, test_bucket, sample_data):
        """Test listing objects in bucket."""
        # Write multiple objects
        for obj in sample_data.values():
            s3_client.put_object(
                Bucket=test_bucket,
                Key=obj["key"],
                Body=obj["data"],
            )

        # List objects
        response = s3_client.list_objects_v2(Bucket=test_bucket)

        # Verify list
        assert "Contents" in response
        assert len(response["Contents"]) == 3
        keys = [obj["Key"] for obj in response["Contents"]]
        assert "test/sample.txt" in keys
        assert "test/sample.json" in keys
        assert "test/sample.bin" in keys

    def test_delete_object(self, s3_client, test_bucket, sample_data):
        """Test deleting an object."""
        text_obj = sample_data["text_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=text_obj["key"],
            Body=text_obj["data"],
        )

        # Verify object exists
        response = s3_client.list_objects_v2(Bucket=test_bucket)
        assert len(response["Contents"]) == 1

        # Delete object
        delete_response = s3_client.delete_object(
            Bucket=test_bucket, Key=text_obj["key"]
        )
        assert delete_response["ResponseMetadata"]["HTTPStatusCode"] == 204

        # Verify object deleted
        response = s3_client.list_objects_v2(Bucket=test_bucket)
        assert "Contents" not in response

    def test_object_exists(self, s3_client, test_bucket, sample_data):
        """Test checking if object exists."""
        text_obj = sample_data["text_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=text_obj["key"],
            Body=text_obj["data"],
        )

        # Check existence
        try:
            s3_client.head_object(Bucket=test_bucket, Key=text_obj["key"])
            exists = True
        except Exception:
            exists = False

        assert exists is True

    def test_get_object_size(self, s3_client, test_bucket, sample_data):
        """Test getting object size."""
        text_obj = sample_data["text_file"]

        # Write object
        s3_client.put_object(
            Bucket=test_bucket,
            Key=text_obj["key"],
            Body=text_obj["data"],
        )

        # Get object size
        response = s3_client.head_object(Bucket=test_bucket, Key=text_obj["key"])
        size = response["ContentLength"]

        # Verify size
        expected_size = len(text_obj["data"].encode("utf-8"))
        assert size == expected_size


class TestRustFSLargeFiles:
    """Test handling larger files."""

    def test_write_read_large_text(self, s3_client, test_bucket):
        """Test writing and reading a larger text file."""
        # Create 1MB of data
        large_content = "x" * (1024 * 1024)

        # Write
        s3_client.put_object(
            Bucket=test_bucket,
            Key="test/large.txt",
            Body=large_content,
        )

        # Read and verify
        response = s3_client.get_object(Bucket=test_bucket, Key="test/large.txt")
        content = response["Body"].read().decode("utf-8")

        assert len(content) == 1024 * 1024
        assert content == large_content

    def test_write_read_binary_stream(self, s3_client, test_bucket):
        """Test writing and reading binary data as stream."""
        # Create binary data
        binary_data = bytes(range(256)) * 100  # 25.6 KB

        # Write as stream
        s3_client.put_object(
            Bucket=test_bucket,
            Key="test/binary-stream.bin",
            Body=BytesIO(binary_data),
        )

        # Read and verify
        response = s3_client.get_object(Bucket=test_bucket, Key="test/binary-stream.bin")
        content = response["Body"].read()

        assert content == binary_data
