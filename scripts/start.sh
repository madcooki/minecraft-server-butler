#!/usr/bin/bash
set -euo pipefail

# Read settings
source "/opt/minecraft-server-butler/settings"

# Set dirty flag and start minecraft server
touch "/opt/minecraft-server-butler/flags/dirty"
exec java ${LAUNCH_OPTIONS} -jar "/opt/minecraft-server-butler/server/server.jar" nogui
