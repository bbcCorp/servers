"""
Pytest fixtures for PostgreSQL testing.
Provides database connection and configuration.
"""

import os
import pytest
from sqlalchemy import create_engine, text, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from parent .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

Base = declarative_base()


@pytest.fixture(scope="session")
def postgres_config():
    """
    Provides PostgreSQL configuration from environment variables.

    Returns:
        dict: PostgreSQL connection configuration
    """
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "devServer@1"),
        "database": os.getenv("POSTGRES_DB", "postgres"),
    }


@pytest.fixture(scope="session")
def engine(postgres_config):
    """
    Provides SQLAlchemy engine for PostgreSQL.

    Args:
        postgres_config: PostgreSQL configuration

    Returns:
        Engine: SQLAlchemy engine instance
    """
    connection_string = (
        f"postgresql://{postgres_config['user']}:{postgres_config['password']}"
        f"@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}"
    )

    engine = create_engine(connection_string, echo=False)

    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return engine


@pytest.fixture(scope="session")
def session_factory(engine):
    """
    Provides SQLAlchemy session factory.

    Args:
        engine: SQLAlchemy engine

    Returns:
        sessionmaker: Session factory
    """
    return sessionmaker(bind=engine)


@pytest.fixture
def db_session(session_factory):
    """
    Provides a database session for testing.
    Rolls back after each test.

    Args:
        session_factory: Session factory

    Yields:
        Session: Database session
    """
    session = session_factory()

    yield session

    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def test_table(engine):
    """
    Creates and cleans up a test table.

    Args:
        engine: SQLAlchemy engine

    Yields:
        str: Table name
    """
    # Define test table model
    class User(Base):
        __tablename__ = "test_users"

        id = Column(Integer, primary_key=True)
        username = Column(String(50), unique=True, nullable=False)
        email = Column(String(100), nullable=False)
        age = Column(Integer)
        active = Column(Boolean, default=True)
        score = Column(Float, default=0.0)
        created_at = Column(DateTime, default=datetime.utcnow)

    # Create table
    Base.metadata.create_all(engine)

    yield "test_users"

    # Cleanup: Drop table
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def raw_connection(engine):
    """
    Provides raw database connection for direct SQL execution.

    Args:
        engine: SQLAlchemy engine

    Yields:
        Connection: Raw database connection
    """
    connection = engine.raw_connection()
    cursor = connection.cursor()

    yield cursor

    # Cleanup
    cursor.close()
    connection.rollback()
    connection.close()


@pytest.fixture(scope="function")
def sample_users():
    """
    Provides sample user data for testing.

    Returns:
        list: Sample user dictionaries
    """
    return [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "age": 30,
            "active": True,
            "score": 95.5,
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "age": 28,
            "active": True,
            "score": 88.0,
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "age": 35,
            "active": False,
            "score": 76.5,
        },
    ]
