-- Supabase Analytics Database Connection
-- This creates the connection to your Supabase database (PostgreSQL)
-- Replace the parameters with your actual Supabase credentials

CREATE DATABASE supabase_analytics
WITH ENGINE = "postgres",
PARAMETERS = { 
  "user": "${SUPABASE_USER}",
  "password": "${SUPABASE_PASSWORD}",
  "host": "${SUPABASE_HOST}",
  "port": "${SUPABASE_PORT}",
  "database": "${SUPABASE_DATABASE}"
};