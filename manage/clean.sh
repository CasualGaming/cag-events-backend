#!/bin/bash

# Remove local run data, virtualenv, Python caches, etc.

FULL_DB_VOLUME="ceb-full-database-data"

echo "Cleaning Docker ..."
docker-compose -f setup/simple/docker-compose.yml down
docker-compose -f setup/full/docker-compose.yml down
docker volume ls -q --filter "name=$FULL_DB_VOLUME" | grep -q . \
&& docker volume rm $FULL_DB_VOLUME

echo "Cleaning local data ..."
rm -rf .local

echo "Cleaning virtualenv ..."
rm -rf .venv

echo "Cleaning Python cache ..."
find src -name "__pycache__" -exec rm -rf {} \; -prune

echo "Cleaning other stuff ..."
rm -f requirements/*.old.txt
