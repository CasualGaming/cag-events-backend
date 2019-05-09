#!/bin/bash

# Note: Do not use "set -u" before sourcing this script, virtualenv's activate may trigger it.

SYSTEM_PACKAGES="virtualenv setuptools wheel"
VENV_PACKAGES="pip-tools"
VENV_DIR=".venv"

if ! [[ -e $VENV_DIR ]]; then
    echo "Virtualenv not found, creating it ..."

    # The essentials
    # Make sure the user bin dir is added to PATH
    pip3 install --quiet $SYSTEM_PACKAGES

    # Windows uses Python 3 as "python", and has no "python3" or "python2"
    # Linux uses Python 2 as "python", but has "python3" and "python2"
    case "$(uname -s)" in
        MINGW*) PYTHON_PATH="$(which python)" ;;
        *) PYTHON_PATH="$(which python3)" ;;
    esac

    # Create venv
    if [[ ! -d .venv ]]; then
        echo "Creating venv ..."
        # Don't use symlinks if in VirtualBox shared folder
        if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
            echo "VirtualBox shared folder detected"
            virtualenv -p $PYTHON_PATH --always-copy $VENV_DIR
        else
            virtualenv -p $PYTHON_PATH $VENV_DIR
        fi
    fi

    # Enter venv
    case "$(uname -s)" in
        MINGW*) source $VENV_DIR/Scripts/activate ;;
        *) source $VENV_DIR/bin/activate ;;
    esac

    # Install extra packages inside venv
    pip install --quiet $VENV_PACKAGES
else
    # Enter existing venv directly
    case "$(uname -s)" in
        MINGW*) source $VENV_DIR/Scripts/activate ;;
        *) source $VENV_DIR/bin/activate ;;
    esac
fi
