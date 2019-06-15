#!/bin/bash

LOCAL_DIR=".local/full"
CONFIG_TEMPLATE_FILE="setup/full/config.template.env"
CONFIG_FILE="$LOCAL_DIR/config.env"
DB_CONTAINER="ceb-full-database"
DB_VOLUME="$DB_CONTAINER-data"
# Double slash prevents MSYS/MinGW path translation
#DB_PGDATA="//var/lib/postgresql/data/pgdata"
DB_SUPERUSER="postgres"
DB_SUPERPASSWORD="dev_postgres_password"
DB_USER="dev_user"
DB_PASSWORD="dev_password"
DB_NAME="dev_db"
DC_FILE="setup/full/docker-compose.yml"
DC="docker-compose -f $DC_FILE"
MANAGE="$DC run app python3 src/manage.py"

set -eu # Exit on error and undefined var is error

mkdir -p $LOCAL_DIR

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Creating new config file ..."
    cp $CONFIG_TEMPLATE_FILE $CONFIG_FILE

    echo
    echo "ATTENTION!"
    echo "A new config file has been created: $CONFIG_FILE"
    echo "Please configure it and then re-run this script."
    exit 0
fi

echo
echo "Removing any previous Docker Compose setups ..."
$DC down

echo
echo "Building image ..."
$DC build app

echo
echo "Creating database data volume ..."
docker volume create $DB_VOLUME

echo
echo "Creating containers ..."
$DC up --no-start

echo
echo "Setting up database ..."
# Fix wrong owner bitching from postgres
echo "(No further output means it failed.)"
$DC up -d database
# Wait for the service to get ready
sleep 5s
docker exec -i -e PGPASSWORD=$DB_SUPERPASSWORD $DB_CONTAINER \
psql --username=$DB_SUPERUSER > /dev/null << END
CREATE DATABASE $DB_NAME;
CREATE ROLE $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'Europe/Oslo';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
END

echo
echo "If you see this, maybe it succeeded."

echo
echo "Stopping ..."
$DC down
