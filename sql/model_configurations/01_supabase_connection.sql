-- Supabase Analytics Database Connection
-- This creates the connection to your Supabase database
-- Replace the parameters with your actual Supabase credentials

CREATE DATABASE supabase_analytics
WITH ENGINE = "supabase",
PARAMETERS = { 
  "user": "${SUPABASE_USER}",
  "password": "${SUPABASE_PASSWORD}",
  "host": "${SUPABASE_HOST}",
  "port": "5432",
  "database": "postgres"
};