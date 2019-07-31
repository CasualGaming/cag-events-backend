#!/bin/bash

# Note: Do not use "set -u" before sourcing this script, virtualenv's activate script may trigger it.

SYSTEM_PACKAGES="virtualenv setuptools wheel"
VENV_DIR=".venv"

if [[ ! -e $VENV_DIR ]]; then
    echo "Virtualenv not found, creating it ..."

    # The essentials
    # Make sure the user bin dir is added to PATH
    # Users need "--user", while CI doesn't allow it
    if [[ $CI == "true" ]]; then
        pip3 install $SYSTEM_PACKAGES
    else
        pip3 install --user $SYSTEM_PACKAGES
    fi

    # Windows uses Python 3 as "python", and has no "python3" or "python2"
    # Linux uses Python 2 as "python", but has "python3" and "python2"
    case "$(uname -s)" in
        MINGW*) PYTHON_PATH="$(which python)" ;;
        *) PYTHON_PATH="$(which python3)" ;;
    esac

    # Create venv
    virtualenv -p "$PYTHON_PATH" $VENV_DIR
fi

# Enter venv
case "$(uname -s)" in
    MINGW*) source $VENV_DIR/Scripts/activate ;;
    *) source $VENV_DIR/bin/activate ;;
esac
