#!/bin/bash
# Скрипт для создания пользователя и базы данных для приложения.

set -e

echo "Waiting for PostgreSQL to start..."

# Ожидание, пока база данных не будет готова
until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  echo "Waiting for database..."
  sleep 2
done

echo "run init script"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --host "postgres" --port 5432 --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $DB_USER WITH LOGIN PASSWORD '$DB_PASSWORD';
  CREATE DATABASE $DB_NAME OWNER $DB_USER;
EOSQL

echo "run sql script"
psql -v ON_ERROR_STOP=1 --username "$DB_USER" --host "postgres" --port 5432 --dbname "$DB_NAME" -f /docker-entrypoint-initdb.d/sql/init.sql
