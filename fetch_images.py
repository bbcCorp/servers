import os
import subprocess
from dotenv import load_dotenv

def pull_docker_image(image_name: str) -> None:
    """Pull a Docker image using subprocess."""
    print(f"Pulling image: {image_name}")
    try:
        subprocess.run(['docker', 'pull', image_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling image {image_name}: {e}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Using docker to pull images")
    
    # Get all environment variables
    env_vars = os.environ
    
    # Filter and pull Docker images. Match any *_IMAGE or *_DOCKER_IMAGE
    # env var so services using either naming convention are covered
    # (e.g. NEO4J_IMAGE, NGINX_IMAGE alongside POSTGRES_DOCKER_IMAGE).
    for key, value in env_vars.items():
        if key.endswith('_IMAGE') or key.endswith('_DOCKER_IMAGE'):
            pull_docker_image(value)

if __name__ == "__main__":
    main()