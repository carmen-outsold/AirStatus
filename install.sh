#!/bin/sh

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists python3; then
    echo "Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
REQUIRED_VERSION="3.11"

compare_versions() {
    [ "$1" = "$2" ] && return 0
    local IFS=.
    set -- $1 $2
    while [ $# -gt 0 ]; do
        [ "${1:-0}" -lt "${2:-0}" ] && return 0
        [ "${1:-0}" -gt "${2:-0}" ] && return 1
        shift 2
    done
    return 0
}

if compare_versions "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
    echo "Python version is less than 3.11. Please update your Python to 3.11 or higher."
    exit 1
fi

if ! command_exists pip3; then
    echo "pip3 is not installed. Please install pip for Python 3."
    exit 1
fi

if ! python3 -c "import bleak" 2>/dev/null; then
    echo "Installing bleak..."
    pip3 install bleak~=0.22.3
fi

INSTALL_DIR="$HOME/.var/airstatus"
mkdir -p "$INSTALL_DIR"

SCRIPT_DIR=$(dirname "$(realpath "$0")")

cp "$SCRIPT_DIR/AirStatus/airstatus.py" "$INSTALL_DIR/airstatus.py"

echo "Copying airstatus.service to /etc/systemd/system. You may be prompted for your sudo password."
sudo cp "$SCRIPT_DIR/AirStatus/airstatus.service" /etc/systemd/system/airstatus.service

echo "To start the service and enable it to start on boot, run:"
echo "  sudo systemctl enable --now airstatus"
