#!/usr/bin/env sh

set -eu # Exit on error and undefined var is error

# Constants
MANAGE="python3 src/manage.py"
APP_DIR="/app"
CONFIG_FILE="$APP_DIR/config.env"
APP_USER="app"
APP_GROUP="app"

# Optional env vars
APP_UID=${APP_UID:=}
APP_GID=${APP_GID:=}

# Check if config file exists
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $CONFIG_FILE" 1>&2
    exit -1
fi

# Clear expired sessions
$MANAGE clearsessions

# Add group and user to run the app
if ! grep -q "^${APP_GROUP}:" /etc/group; then
    if [[ ! -z $APP_GID ]]; then
        groupadd -r -g $APP_GID $APP_GROUP
    else
        groupadd -r $APP_GROUP
    fi
fi
if ! grep -q "^${APP_USER}:" /etc/passwd; then
    if [[ ! -z $APP_UID ]]; then
        useradd -r -g $APP_GROUP -u $APP_UID $APP_USER
    else
        useradd -r -g $APP_GROUP $APP_USER
    fi
fi
echo "App user: $(id $APP_USER)"

# Setup permissions and stuff
# Note: Volumes from vboxsf cannot be chowned
set +e
echo "Chowning all app files ..."
chown -R $APP_USER:$APP_GROUP . 2>/dev/null
set -e

# Run server
echo
exec su $APP_USER -c "$MANAGE runserver 0.0.0.0:8000"
