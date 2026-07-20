#!/usr/bin/bash
set -euo pipefail

# Read settings
source "/opt/minecraft-server-butler/settings"

clear_backup_buffer() {
    mkdir -p "${BACKUP_PATH}/buffer"
    rm -rf "${BACKUP_PATH}/buffer/"*
}

# +----------------+
# | Backup/Restore |
# +----------------+

timestamp_now=$(date +"%Y-%m-%dT%H:%M:%S")

clear_backup_buffer
mkdir -p "${BACKUP_PATH}/short-term"
mkdir -p "${BACKUP_PATH}/long-term"

if [ ! -z "${1+x}" ]; then
    echo "Manual restoration requested. Attempting to locate specified backup: ${1}..."

    if [ ! -z "$( ls -1r "${BACKUP_PATH}/short-term/${1}" 2>/dev/null )" ]; then
        restoration_backup_path="${BACKUP_PATH}/short-term/${1}"
    elif [ ! -z "$( ls -1r "${BACKUP_PATH}/long-term/${1}" 2>/dev/null )" ]; then
        restoration_backup_path="${BACKUP_PATH}/long-term/${1}"
    else
        echo "Specified backup not found." 1>&2
        exit 1
    fi
elif [ -f "/opt/minecraft-server-butler/flags/dirty" ]; then
    echo "Dirty state detected. Automatically restoring from latest backup..."

    if [ ! -z "$( ls -1r "${BACKUP_PATH}/short-term/"*.tar.zst 2>/dev/null )" ]; then
        restoration_backup_path="$( ls -1r "${BACKUP_PATH}/short-term/"*.tar.zst | head -n 1 )"
    elif [ ! -z "$( ls -1r "${BACKUP_PATH}/long-term/"*.tar.zst 2>/dev/null )" ]; then
        restoration_backup_path="$( ls -1r "${BACKUP_PATH}/long-term/"*.tar.zst | head -n 1 )"
    else
        echo "No backups found." 1>&2
        exit 1
    fi
fi

if [ ! -z "${restoration_backup_path+x}" ]; then
    echo "Attempting to restore from backup: ${restoration_backup_path}..."

    tar --zstd -xf "${restoration_backup_path}" -C "${BACKUP_PATH}/buffer"
    rsync --archive --delete --checksum --exclude="scripts" --exclude="systemd-units" --exclude="flags/dirty" "${BACKUP_PATH}/buffer/" "/opt/minecraft-server-butler/"
    clear_backup_buffer

    echo "Restoration complete."
else
    echo "Backing up..."

    shortterm_backup_filename="$(date --date "${timestamp_now}" +"%Y-%m-%d_%H-%M-%S").tar.zst"
    tar --zstd -cf "${BACKUP_PATH}/buffer/${shortterm_backup_filename}" -C "/opt/minecraft-server-butler" .

    if ! zstd_output=$(zstd -t "${BACKUP_PATH}/buffer/${shortterm_backup_filename}" 2>&1); then
        clear_backup_buffer
        echo "New short-term backup integrity check failed." 1>&2
        echo "${zstd_output}" 1>&2
        exit 1
    else
        mv "${BACKUP_PATH}/buffer/${shortterm_backup_filename}" "${BACKUP_PATH}/short-term/${shortterm_backup_filename}"
        echo "New short-term backup created: ${BACKUP_PATH}/short-term/${shortterm_backup_filename}"
    fi

    if [ -z "$( ls -1r "${BACKUP_PATH}/long-term/$(date --date "${timestamp_now}" +"%Y-%m")"*.tar.zst 2>/dev/null )" ]; then
        longterm_backup_filename="$(basename $( ls -1r "${BACKUP_PATH}/short-term/$(date --date "${timestamp_now}" +"%Y-%m")"*.tar.zst | tail -n 1 ))"
        cp "${BACKUP_PATH}/short-term/${longterm_backup_filename}" "${BACKUP_PATH}/buffer/${longterm_backup_filename}"

        if ! zstd_output=$(zstd -t "${BACKUP_PATH}/buffer/${longterm_backup_filename}" 2>&1); then
            clear_backup_buffer
            echo "New long-term backup integrity check failed." 1>&2
            echo "${zstd_output}" 1>&2
            exit 1
        else
            mv "${BACKUP_PATH}/buffer/${longterm_backup_filename}" "${BACKUP_PATH}/long-term/${longterm_backup_filename}"
            echo "New long-term backup created: ${BACKUP_PATH}/long-term/${longterm_backup_filename}"
        fi
    fi

    ls -1r "${BACKUP_PATH}/short-term/"*.tar.zst | tail -n +$((BACKUP_KEEP_SHORT_TERM + 1)) | xargs -r rm -rf
    ls -1r "${BACKUP_PATH}/long-term/"*.tar.zst | tail -n +$((BACKUP_KEEP_LONG_TERM + 1)) | xargs -r rm -rf
    clear_backup_buffer

    echo "Backup complete."
fi

# +------------------+
# | Automatic update |
# +------------------+

if [ $AUTO_UPDATE != true ] && [ $AUTO_UPDATE != false ]; then
    echo "Invalid value for property \"AUTO_UPDATE\" in file \"/opt/minecraft-server-butler/settings\" detected. Please set property to either \"true\" or \"false\"." 1>&2
    exit 1
fi

if [ $AUTO_UPDATE = false ]; then
    echo "Automatic updates currently disabled. Skipping automatic update..."
    if [ -f "/opt/minecraft-server-butler/flags/auto_update_version" ]; then
        rm "/opt/minecraft-server-butler/flags/auto_update_version"
    fi
    exit 0
else
    echo "Automatic updates currently enabled. Checking for updates..."

    if ! manifest=$(curl -fsSL "https://launchermeta.mojang.com/mc/game/version_manifest.json"); then
        echo "Could not reach Mojang. Skipping automatic update..."
        exit 0
    else
        if [ -f "/opt/minecraft-server-butler/flags/auto_update_version" ]; then
            server_version=$(cat "/opt/minecraft-server-butler/flags/auto_update_version")
        else
            server_version="unknown"
        fi

        echo "Server version: ${server_version}"

        latest_version=$(echo "${manifest}" | jq -r '.latest.release')
        echo "Latest release: ${latest_version}"

        if [ "${server_version}" = "${latest_version}" ]; then
            echo "Server already up to date. Skipping automatic update..."
            exit 0
        fi

        echo "Updating to latest release: ${latest_version}..."

        if ! version_json=$(curl -fsSL "$(echo "${manifest}" | jq -r ".versions[] | select(.id==\"${latest_version}\") | .url")"); then
            echo "Could not reach Mojang. Skipping automatic update..."
            exit 0
        else
            download_url=$(echo "${version_json}" | jq -r '.downloads.server.url')
            download_sha1=$(echo "${version_json}" | jq -r '.downloads.server.sha1')

            curl -fL -o "/opt/minecraft-server-butler/server/server.jar.new" "${download_url}"
            if ! checksum_output=$(echo "${download_sha1} /opt/minecraft-server-butler/server/server.jar.new" | sha1sum -c - 2>&1); then
                rm -f "/opt/minecraft-server-butler/server/server.jar.new"
                echo "Update integrity check failed." 1>&2
                echo "Checksum: $checksum_output" 1>&2
                exit 1
            else
                mv "/opt/minecraft-server-butler/server/server.jar.new" "/opt/minecraft-server-butler/server/server.jar"
                echo "${latest_version}" > "/opt/minecraft-server-butler/flags/auto_update_version"
                echo "Successfully updated to new version: ${latest_version}"
            fi
        fi
    fi
fi
