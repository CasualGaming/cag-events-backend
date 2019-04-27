#!/bin/bash

DEV_SETTINGS_FILE="dev-setup/docker-full/env.original"
SETTINGS_FILE="dev-setup/docker-full/env"
DB_CONTAINER_ID="cag-events-backend-full-db"
DB_SUPERUSER="postgres"
DB_USER="dev_user"
DB_PASSWORD="dev_password"
DB_NAME="dev_db"
DC_FILE="dev-setup/docker-full/docker-compose.yml"
DC="docker-compose -f $DC_FILE"
DC_MANAGE="$DC run app python3 manage.py"

set -eu # Exit on error and undefined var is error

# Add settings file
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "Adding sample settings file ..."
    mkdir -p $(dirname $SETTINGS_FILE)
    cp $DEV_SETTINGS_FILE $SETTINGS_FILE
fi

echo
echo "Removing previous instances ..."
$DC down

echo
echo "Building ..."
$DC build app

echo
echo "Creating containers ..."
$DC up --no-start

echo
echo "Setting up DB user ..."
$DC up -d db
# Wait for the service to get ready
sleep 10s
docker exec -i $DB_CONTAINER_ID psql --username=$DB_SUPERUSER 1>/dev/null << END
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'Europe/Oslo';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
END
$DC_MANAGE check

echo
echo "Stopping ..."
$DC stop
