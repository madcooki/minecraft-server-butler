#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import sys

from butler.constants import (
    PATH_SYSTEMD_MAINTENANCE_SERVICE,
    PATH_SYSTEMD_MAINTENANCE_TIMER,
    PATH_SYSTEMD_MINECRAFT_SERVICE,
)


def run_command(command: list[str | Path]) -> None:
    subprocess.run(command, check=True)


def systemctl_link(unit: Path) -> None:
    run_command(["systemctl", "link", unit])


def systemctl_reload() -> None:
    run_command(["systemctl", "daemon-reload"])


def systemctl_enable(unit: Path) -> None:
    run_command(["systemctl", "enable", unit.name])


def systemctl_disable(unit: Path) -> None:
    run_command(["systemctl", "disable", unit.name])


def systemctl_start(unit: Path) -> None:
    run_command(["systemctl", "start", unit.name])


def systemctl_stop(unit: Path) -> None:
    run_command(["systemctl", "stop", unit.name])


def main() -> None:
    arg_install = "install"
    arg_uninstall = "uninstall"

    example_base = f"sudo {Path(__file__).resolve()}"
    example_install = f"{example_base} {arg_install}"
    example_uninstall = f"{example_base} {arg_uninstall}"

    if os.getuid() != 0:
        print(
            f"This script must be run as root. Example: {example_install}",
            flush=True,
        )
        exit(1)

    if len(sys.argv) < 2 or sys.argv[1] not in [arg_install, arg_uninstall]:
        print(
            (
                f"You must specify \"{arg_install}\" or \"{arg_uninstall}\". "
                f"Example: {example_install}"
            ),
            flush=True,
        )
        exit(1)
    elif sys.argv[1] == arg_install:
        systemctl_link(PATH_SYSTEMD_MINECRAFT_SERVICE)
        systemctl_link(PATH_SYSTEMD_MAINTENANCE_SERVICE)
        systemctl_link(PATH_SYSTEMD_MAINTENANCE_TIMER)

        systemctl_reload()

        systemctl_enable(PATH_SYSTEMD_MINECRAFT_SERVICE)
        systemctl_enable(PATH_SYSTEMD_MAINTENANCE_TIMER)

        systemctl_start(PATH_SYSTEMD_MINECRAFT_SERVICE)
        systemctl_start(PATH_SYSTEMD_MAINTENANCE_TIMER)

        print(
            (
                "Systemd units successfully installed. "
                f"To uninstall, run: {example_uninstall}"
            ),
            flush=True,
        )
    elif sys.argv[1] == arg_uninstall:
        systemctl_stop(PATH_SYSTEMD_MAINTENANCE_TIMER)
        systemctl_stop(PATH_SYSTEMD_MINECRAFT_SERVICE)

        systemctl_disable(PATH_SYSTEMD_MAINTENANCE_TIMER)
        systemctl_disable(PATH_SYSTEMD_MAINTENANCE_SERVICE)
        systemctl_disable(PATH_SYSTEMD_MINECRAFT_SERVICE)

        systemctl_reload()

        print(
            (
                "Systemd units successfully uninstalled. "
                f"To reinstall, run: {example_install}"
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
