#!/usr/bin/env sh

set -eu # Exit on error and undefined var is error

# Constants
MANAGE="python3 manage.py"
SETTINGS_FILE="/app/env"
LOG_DIR="/app/log"
APP_USER="app"
APP_GROUP="app"

# Optional env vars
APP_UID=${APP_UID:=}
APP_GID=${APP_GID:=}
SUPERUSER_USERNAME=${SUPERUSER_USERNAME:=}
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:=}
SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:=}
SUPERUSER_INACTIVE=${SUPERUSER_INACTIVE:=}

# Check if settings exist
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "App settings not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

# Collect static files
echo
echo "Collecting static files ..."
$MANAGE collectstatic --noinput --clear | egrep -v "^Deleting" || true

# Run migration, but skip initial if matching table names already exist
echo
echo "Migrating database ..."
$MANAGE migrate --fake-initial

# Clear expired sessions
$MANAGE clearsessions

# Optionally add superuser
echo
if [[ ! -z $SUPERUSER_USERNAME ]]; then
    echo "Adding superuser ..."
    # FIXME disable superiser
    if [[ $SUPERUSER_INACTIVE == "true" ]]; then
        SUPERUSER_ACTIVE="False"
    else
        SUPERUSER_ACTIVE="True"
    fi
    $MANAGE shell << END
# Python 3
from django.contrib.auth import get_user_model;

superuser_usernane = "${SUPERUSER_USERNAME}"
superuser_email = "${SUPERUSER_EMAIL}"
superuser_password = "${SUPERUSER_PASSWORD}"
superuser_active = ${SUPERUSER_ACTIVE}

if not superuser_usernane:
    print("Error: Username not specified")
    quit()

User = get_user_model();
if User.objects.filter(username=superuser_usernane).exists():
    print("User with specified username already exists. Not adding superuser.")
elif not superuser_email or not superuser_password:
    print("User with specified username does not exist, but all credentials were not specified. Not adding superuser.")
else:
    print("User with specified username does not exist and all credentials were provided. Adding superuser with is_active={}.".format(superuser_active))
    User.objects.create_superuser(username=superuser_usernane, email=superuser_email, password=superuser_password, is_active=superuser_active)

quit()
END
    echo "If a superuser was created, please change its password in the app"
fi

# Validate
echo
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

# Add group and user to run the app
echo
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
    echo "Added user: $(id $APP_USER)"
fi

# Setup permissions and stuff
# Note: Volumes from vboxsf cannot be chowned
set +e
echo "Trying to chown all files ..."
chown -R $APP_USER:$APP_GROUP . 2>/dev/null
set -e

# Run server
echo
echo "Starting uWSGI server ..."
exec uwsgi --ini uwsgi.ini
