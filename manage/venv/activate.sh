#!/bin/bash

# Note: Do not use "set -u" before sourcing this script, virtualenv's activate may trigger it.

SYSTEM_PACKAGES="virtualenv setuptools wheel"
EXTRA_PACKAGES=""
VENV_DIR=".venv"

if [[ ! -e $VENV_DIR ]]; then
    echo "Virtualenv not found, creating it ..."

    # The essentials
    # Make sure the user bin dir is added to PATH
    # Users need "--user", while CI doesn't allow it
    if [[ $CI == "true" ]]; then
        pip3 install --quiet $SYSTEM_PACKAGES
    else
        pip3 install --user --quiet $SYSTEM_PACKAGES
    fi

    # Windows uses Python 3 as "python", and has no "python3" or "python2"
    # Linux uses Python 2 as "python", but has "python3" and "python2"
    case "$(uname -s)" in
        MINGW*) PYTHON_PATH="$(which python)" ;;
        *) PYTHON_PATH="$(which python3)" ;;
    esac

    # Create venv
    if [[ ! -d .venv ]]; then
        echo
        echo "Creating virtualenv ..."
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
    if [[ ! -z $EXTRA_PACKAGES ]]; then
        pip install --quiet $EXTRA_PACKAGES
    fi
else
    # Enter existing venv directly
    case "$(uname -s)" in
        MINGW*) source $VENV_DIR/Scripts/activate ;;
        *) source $VENV_DIR/bin/activate ;;
    esac
fi
