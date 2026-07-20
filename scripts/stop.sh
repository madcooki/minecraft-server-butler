#!/usr/bin/bash
set -euo pipefail

# Read settings
source "/opt/minecraft-server-butler/settings"

MAINPID=$(systemctl show -p MainPID --value minecraft.service)
if [ "$MAINPID" -eq 0 ]; then
    echo "No running Minecraft PID."
    exit 0
fi

echo "Waiting for RCON to respond..."

for i in {1..60}; do
    if mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "list" >/dev/null 2>&1; then
        echo "RCON ready."
        break
    fi
    sleep 1
done

if mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "list" >/dev/null 2>&1; then

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 10 minutes.\"}"
    echo "The server will restart in 10 minutes."
    sleep 300

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 5 minutes.\"}"
    echo "The server will restart in 5 minutes."
    sleep 240

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 1 minute.\"}"
    echo "The server will restart in 1 minute."
    sleep 50

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 10 seconds!\"}"
    echo "The server will restart in 10 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 9 seconds!\"}"
    echo "The server will restart in 9 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 8 seconds!\"}"
    echo "The server will restart in 8 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 7 seconds!\"}"
    echo "The server will restart in 7 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 6 seconds!\"}"
    echo "The server will restart in 6 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 5 seconds!\"}"
    echo "The server will restart in 5 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 4 seconds!\"}"
    echo "The server will restart in 4 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 3 seconds!\"}"
    echo "The server will restart in 3 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 2 seconds!\"}"
    echo "The server will restart in 2 seconds!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server will restart in 1 second!\"}"
    echo "The server will restart in 1 second!"
    sleep 1

    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "tellraw @a {\"color\":\"red\",\"text\":\"[Server] The server is restarting now!\"}"
    echo "The server is restarting now!"
    sleep 1

    echo "Requesting clean shutdown through RCON..."
    mcrcon -P "${MCRCON_PORT}" -p "${MCRCON_PASSWORD}" "stop"
else
    echo "RCON did not respond in time. Sending SIGTERM..." 1>&2
    kill -SIGTERM "$MAINPID"
    exit 1
fi

while kill -0 "$MAINPID" 2>/dev/null; do
    sleep 1
done

echo "$(date +"%Y-%m-%d %H:%M:%S")" > "/opt/minecraft-server-butler/flags/timestamp_latest_save"
rm "/opt/minecraft-server-butler/flags/dirty"

echo "Clean shutdown confirmed."
