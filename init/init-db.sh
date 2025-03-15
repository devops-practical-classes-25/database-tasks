#!/bin/bash
# Скрипт для создания пользователя и базы данных для приложения.

set -e

echo run init script

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $DB_USER WITH LOGIN PASSWORD '$DB_PASSWORD';
	CREATE DATABASE $DB_NAME OWNER $DB_USER;
EOSQL

echo run sql script
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/sql/demo-small-en-20170815.sql