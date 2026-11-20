-- Hindsight PostgreSQL Initialization Script
-- Creates schema and user for Hindsight service

-- Create hindsight database user if it doesn't exist
DO $$
BEGIN
  CREATE USER hindsight_user WITH PASSWORD 'hindsight@1';
EXCEPTION WHEN duplicate_object THEN
  NULL;
END
$$;

-- Create hindsight schema in existing postgres database
DO $$
BEGIN
  CREATE SCHEMA hindsight AUTHORIZATION hindsight_user;
EXCEPTION WHEN duplicate_schema THEN
  NULL;
END
$$;

-- Grant schema privileges to hindsight user
GRANT USAGE ON SCHEMA hindsight TO hindsight_user;
GRANT CREATE ON SCHEMA hindsight TO hindsight_user;

-- Set default privileges for hindsight user in hindsight schema
ALTER DEFAULT PRIVILEGES IN SCHEMA hindsight GRANT ALL PRIVILEGES ON TABLES TO hindsight_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hindsight GRANT ALL PRIVILEGES ON SEQUENCES TO hindsight_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hindsight GRANT ALL PRIVILEGES ON FUNCTIONS TO hindsight_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hindsight GRANT ALL PRIVILEGES ON TYPES TO hindsight_user;

-- Set application defaults
ALTER ROLE hindsight_user SET search_path = hindsight;
