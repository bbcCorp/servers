"""
Pytest fixtures for RustFS testing.
Provides S3 client configured for RustFS object store.
"""

import os
import pytest
import boto3
from dotenv import load_dotenv

# Load environment variables from parent .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


@pytest.fixture(scope="session")
def rustfs_config():
    """
    Provides RustFS configuration from environment variables.

    Returns:
        dict: RustFS connection configuration
    """
    return {
        "endpoint_url": os.getenv("RUSTFS_ENDPOINT_URL", "http://localhost:9000"),
        "access_key": os.getenv("RUSTFS_ROOT_USER", "minio"),
        "secret_key": os.getenv("RUSTFS_ROOT_PASSWORD", "minio123"),
        "region_name": os.getenv("RUSTFS_REGION", "us-east-1"),
        "bucket": os.getenv("RUSTFS_BUCKET", "test-bucket"),
    }


@pytest.fixture(scope="session")
def s3_client(rustfs_config):
    """
    Provides boto3 S3 client configured for RustFS.

    Args:
        rustfs_config: RustFS configuration

    Returns:
        boto3.client: S3 client connected to RustFS
    """
    client = boto3.client(
        "s3",
        endpoint_url=rustfs_config["endpoint_url"],
        aws_access_key_id=rustfs_config["access_key"],
        aws_secret_access_key=rustfs_config["secret_key"],
        region_name=rustfs_config["region_name"],
    )
    return client


@pytest.fixture(scope="function")
def test_bucket(s3_client, rustfs_config):
    """
    Creates a test bucket for each test and cleans up after.

    Args:
        s3_client: S3 client
        rustfs_config: RustFS configuration

    Yields:
        str: Bucket name
    """
    bucket_name = rustfs_config["bucket"]

    # Create bucket if it doesn't exist
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)

    yield bucket_name

    # Cleanup: Empty the bucket
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
    except Exception:
        pass


@pytest.fixture(scope="function")
def sample_data():
    """
    Provides sample data for testing.

    Returns:
        dict: Sample objects for testing
    """
    return {
        "text_file": {
            "key": "test/sample.txt",
            "data": "Hello, RustFS! This is a test file.",
            "content_type": "text/plain",
        },
        "json_file": {
            "key": "test/sample.json",
            "data": '{"name": "RustFS", "type": "object store", "status": "active"}',
            "content_type": "application/json",
        },
        "binary_file": {
            "key": "test/sample.bin",
            "data": b"Binary content \x00\x01\x02\x03",
            "content_type": "application/octet-stream",
        },
    }
