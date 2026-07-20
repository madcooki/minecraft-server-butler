#!/usr/bin/bash
set -euo pipefail

example="sudo /opt/minecraft-server-butler/scripts/systemd-units.sh"
example_install="${example} install"
example_uninstall="${example} uninstall"

if [ "$(id -u)" != 0 ]; then
    echo "This script must be run as root. Example: ${example_install}" 1>&2
    exit 1
fi

if [ -z "${1+x}" ] || ([ "${1}" != "install" ] && [ "${1}" != "uninstall" ]); then
    echo "You must specify \"install\" or \"uninstall\". Example: ${example_install}" 1>&2
    exit 1
elif [ "${1}" = "install" ]; then
    systemctl link "/opt/minecraft-server-butler/systemd-units/minecraft.service"
    systemctl link "/opt/minecraft-server-butler/systemd-units/minecraft-maintenance.service"
    systemctl link "/opt/minecraft-server-butler/systemd-units/minecraft-maintenance.timer"

    systemctl daemon-reload

    systemctl enable minecraft.service
    systemctl enable minecraft-maintenance.timer

    systemctl start minecraft.service
    systemctl start minecraft-maintenance.timer

    echo "Systemd units successfully installed. To uninstall, run: ${example_uninstall}"
elif [ "${1}" = "uninstall" ]; then
    systemctl stop minecraft-maintenance.timer
    systemctl stop minecraft.service

    systemctl disable minecraft-maintenance.timer
    systemctl disable minecraft-maintenance.service
    systemctl disable minecraft.service

    systemctl daemon-reload

    echo "Systemd units successfully uninstalled. To reinstall, run: ${example_install}"
fi
