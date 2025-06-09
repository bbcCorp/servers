from dotenv import load_dotenv
import os
import sys
from rmq import test_rmq_client

# Load environment variables from .env file
env_file_path = os.path.join(os.path.dirname(__file__), "./../.env")
if not os.path.exists(env_file_path):
    print(f"Error: .env file not found at {env_file_path}")
    sys.exit(1)

load_dotenv(env_file_path)


if __name__ == "__main__":
    try:
        test_rmq_client()
        sys.exit(0)

    except Exception as e:
        exception = e
        print(f"An error occurred: {e}")
        sys.exit(1)
