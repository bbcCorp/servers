"""
Unit tests for PostgreSQL database operations.
Tests CRUD operations and database interactions.
"""

import pytest
from sqlalchemy import text, func
from datetime import datetime


class TestPostgresConnection:
    """Test PostgreSQL connectivity and configuration."""

    def test_database_connection(self, engine):
        """Verify database connection is working."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            assert row[0] == 1

    def test_postgres_version(self, engine):
        """Verify PostgreSQL version can be retrieved."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            assert "PostgreSQL" in version

    def test_postgres_config_loaded(self, postgres_config):
        """Verify PostgreSQL configuration is loaded."""
        assert postgres_config["host"]
        assert postgres_config["user"]
        assert postgres_config["database"]
        assert postgres_config["port"] > 0


class TestPostgresTableOperations:
    """Test table creation and management."""

    def test_create_table(self, engine, raw_connection):
        """Test creating a table."""
        cursor = raw_connection

        # Create table
        cursor.execute("""
            CREATE TABLE test_products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2),
                in_stock BOOLEAN DEFAULT TRUE
            )
        """)

        # Verify table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_name = 'test_products'
            )
        """)

        exists = cursor.fetchone()[0]
        assert exists is True

        # Cleanup
        cursor.execute("DROP TABLE test_products")

    def test_table_columns(self, engine, test_table):
        """Test verifying table columns."""
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'test_users'
                ORDER BY ordinal_position
            """))

            columns = {row[0]: row[1] for row in result}

            assert "id" in columns
            assert "username" in columns
            assert "email" in columns
            assert "age" in columns
            assert columns["id"] == "integer"
            assert "character" in columns["username"]


class TestPostgresCRUDOperations:
    """Test CRUD (Create, Read, Update, Delete) operations."""

    def test_insert_single_record(self, engine, test_table, db_session):
        """Test inserting a single record."""
        from sqlalchemy.orm import Session

        # Execute insert via raw SQL
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, age, active, score)
                VALUES ('alice', 'alice@example.com', 25, true, 92.5)
            """))
            conn.commit()

        # Verify insert
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT * FROM test_users WHERE username = 'alice'"
            ))
            row = result.fetchone()
            assert row is not None
            assert row[1] == "alice"

    def test_insert_multiple_records(self, engine, test_table, sample_users):
        """Test inserting multiple records."""
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Verify count
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM test_users"))
            count = result.scalar()
            assert count == len(sample_users)

    def test_select_all_records(self, engine, test_table, sample_users):
        """Test selecting all records."""
        # Insert test data
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Select all
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM test_users"))
            rows = result.fetchall()
            assert len(rows) == len(sample_users)

    def test_select_with_where_clause(self, engine, test_table, sample_users):
        """Test selecting with WHERE clause."""
        # Insert test data
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Select with WHERE
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT * FROM test_users WHERE age > 30"
            ))
            rows = result.fetchall()
            assert len(rows) == 1  # bob_wilson is 35

    def test_update_record(self, engine, test_table):
        """Test updating a record."""
        # Insert record
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, age, active, score)
                VALUES ('testuser', 'test@example.com', 25, true, 80.0)
            """))
            conn.commit()

        # Update record
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE test_users
                SET score = 95.0, age = 26
                WHERE username = 'testuser'
            """))
            conn.commit()

        # Verify update
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT score, age FROM test_users WHERE username = 'testuser'"
            ))
            row = result.fetchone()
            assert row[0] == 95.0
            assert row[1] == 26

    def test_delete_record(self, engine, test_table):
        """Test deleting a record."""
        # Insert record
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, age, active, score)
                VALUES ('todelete', 'delete@example.com', 30, true, 70.0)
            """))
            conn.commit()

        # Verify exists
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT COUNT(*) FROM test_users WHERE username = 'todelete'"
            ))
            assert result.scalar() == 1

        # Delete record
        with engine.connect() as conn:
            conn.execute(text(
                "DELETE FROM test_users WHERE username = 'todelete'"
            ))
            conn.commit()

        # Verify deleted
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT COUNT(*) FROM test_users WHERE username = 'todelete'"
            ))
            assert result.scalar() == 0


class TestPostgresQueryOperations:
    """Test complex query operations."""

    def test_aggregate_functions(self, engine, test_table, sample_users):
        """Test aggregate functions (COUNT, AVG, MAX, MIN)."""
        # Insert test data
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Test aggregate functions
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) as cnt, AVG(age) as avg_age,
                       MAX(score) as max_score, MIN(score) as min_score
                FROM test_users
            """))
            row = result.fetchone()

            assert row[0] == 3  # count
            assert row[1] == 31.0  # average age (30+28+35)/3
            assert row[2] == 95.5  # max score
            assert row[3] == 76.5  # min score

    def test_group_by(self, engine, test_table):
        """Test GROUP BY clause."""
        # Insert test data with categories
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, active, score)
                VALUES ('user1', 'user1@example.com', true, 90.0)
            """))
            conn.execute(text("""
                INSERT INTO test_users (username, email, active, score)
                VALUES ('user2', 'user2@example.com', true, 85.0)
            """))
            conn.execute(text("""
                INSERT INTO test_users (username, email, active, score)
                VALUES ('user3', 'user3@example.com', false, 80.0)
            """))
            conn.commit()

        # Test GROUP BY
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT active, COUNT(*) as count, AVG(score) as avg_score
                FROM test_users
                GROUP BY active
                ORDER BY active DESC
            """))
            rows = result.fetchall()

            assert len(rows) == 2
            # First row: active=true
            assert rows[0][0] is True
            assert rows[0][1] == 2
            # Second row: active=false
            assert rows[1][0] is False
            assert rows[1][1] == 1

    def test_order_by(self, engine, test_table, sample_users):
        """Test ORDER BY clause."""
        # Insert test data
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Test ORDER BY descending
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT username, score FROM test_users ORDER BY score DESC"
            ))
            rows = result.fetchall()

            assert rows[0][1] == 95.5  # john_doe
            assert rows[1][1] == 88.0  # jane_smith
            assert rows[2][1] == 76.5  # bob_wilson

    def test_limit_offset(self, engine, test_table, sample_users):
        """Test LIMIT and OFFSET clauses."""
        # Insert test data
        with engine.connect() as conn:
            for user in sample_users:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES (:username, :email, :age, :active, :score)
                """), user)
            conn.commit()

        # Test LIMIT
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT username FROM test_users LIMIT 2"
            ))
            rows = result.fetchall()
            assert len(rows) == 2

        # Test OFFSET
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT username FROM test_users ORDER BY username LIMIT 2 OFFSET 1"
            ))
            rows = result.fetchall()
            assert len(rows) == 2


class TestPostgresTransactions:
    """Test transaction handling."""

    def test_transaction_commit(self, engine, test_table):
        """Test transaction commit."""
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, age, active, score)
                VALUES ('transaction_user', 'trans@example.com', 30, true, 85.0)
            """))

        # Verify insert
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT COUNT(*) FROM test_users WHERE username = 'transaction_user'"
            ))
            assert result.scalar() == 1

    def test_transaction_rollback(self, engine, test_table):
        """Test transaction rollback."""
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO test_users (username, email, age, active, score)
                    VALUES ('rollback_user', 'rollback@example.com', 25, true, 80.0)
                """))
                # Force error
                raise Exception("Intentional error for rollback")
        except Exception:
            pass

        # Verify rollback
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT COUNT(*) FROM test_users WHERE username = 'rollback_user'"
            ))
            assert result.scalar() == 0


class TestPostgresDataTypes:
    """Test various PostgreSQL data types."""

    def test_boolean_type(self, engine, test_table):
        """Test boolean data type."""
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, active)
                VALUES ('bool_test', 'bool@example.com', false)
            """))
            conn.commit()

        # Verify
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT active FROM test_users WHERE username = 'bool_test'"
            ))
            assert result.scalar() is False

    def test_numeric_types(self, engine, test_table):
        """Test numeric data types (INT, FLOAT)."""
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email, age, score)
                VALUES ('numeric_test', 'numeric@example.com', 42, 98.75)
            """))
            conn.commit()

        # Verify
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT age, score FROM test_users WHERE username = 'numeric_test'"
            ))
            row = result.fetchone()
            assert row[0] == 42
            assert row[1] == 98.75

    def test_string_type(self, engine, test_table):
        """Test string data type."""
        email = "string_test@example.com"

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO test_users (username, email)
                VALUES ('string_test', :email)
            """), {"email": email})
            conn.commit()

        # Verify
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT email FROM test_users WHERE username = 'string_test'"
            ))
            assert result.scalar() == email

    def test_datetime_type(self, engine, test_table):
        """Test datetime data type."""
        with engine.connect() as conn:
            # Insert record
            conn.execute(text("""
                INSERT INTO test_users (username, email)
                VALUES ('datetime_test', 'datetime@example.com')
            """))
            conn.commit()

        # Verify created_at is set
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT created_at FROM test_users WHERE username = 'datetime_test'"
            ))
            created_at = result.scalar()
            assert created_at is not None
            assert isinstance(created_at, datetime)


class TestPostgresIndexes:
    """Test index operations."""

    def test_create_index(self, engine, raw_connection):
        """Test creating an index."""
        cursor = raw_connection

        # Create test table
        cursor.execute("""
            CREATE TABLE test_indexed (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)

        # Create index
        cursor.execute(
            "CREATE INDEX idx_name ON test_indexed(name)"
        )

        # Verify index exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE indexname = 'idx_name'
            )
        """)

        exists = cursor.fetchone()[0]
        assert exists is True

        # Cleanup
        cursor.execute("DROP TABLE test_indexed")
