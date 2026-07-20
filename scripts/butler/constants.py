from pathlib import Path
from typing import Final

from butler.config import (
    ButlerConfig,
    load_butler_config,
)


PATH_BUTLER_ROOT: Final[Path] = Path("/opt/minecraft-server-butler")
PATH_INI: Final[Path] = PATH_BUTLER_ROOT / "butler.ini"

CONFIG: Final[ButlerConfig] = load_butler_config(PATH_INI)

PATH_SYSTEMD_UNITS: Final[Path] = PATH_BUTLER_ROOT / "systemd-units"
PATH_SYSTEMD_MINECRAFT_SERVICE: Final[Path] = (
    PATH_SYSTEMD_UNITS / "minecraft.service"
)
PATH_SYSTEMD_MAINTENANCE_SERVICE: Final[Path] = (
    PATH_SYSTEMD_UNITS / "minecraft-maintenance.service"
)
PATH_SYSTEMD_MAINTENANCE_TIMER: Final[Path] = (
    PATH_SYSTEMD_UNITS / "minecraft-maintenance.timer"
)
