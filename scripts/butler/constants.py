from datetime import datetime
from pathlib import Path
from typing import Final

from butler.config import (
    ButlerConfig,
    load_butler_config,
)


PATH_BUTLER_ROOT: Final[Path] = Path("/opt/minecraft-server-butler")
PATH_INI: Final[Path] = PATH_BUTLER_ROOT / "butler.ini"

CONFIG: Final[ButlerConfig] = load_butler_config(PATH_INI)

PATH_FLAGS: Final[Path] = PATH_BUTLER_ROOT / "flags"
PATH_FLAG_DIRTY: Final[Path] = PATH_FLAGS / "dirty"
PATH_FLAG_VERSION: Final[Path] = PATH_FLAGS / "auto_update_version"

PATH_SCRIPTS: Final[Path] = PATH_BUTLER_ROOT / "scripts"

PATH_SERVER: Final[Path] = PATH_BUTLER_ROOT / "server"
PATH_SERVER_JAR: Final[Path] = PATH_SERVER / "server.jar"
PATH_SERVER_JAR_NEW: Final[Path] = PATH_SERVER / "server.jar.new"

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

PATH_BACKUP_ROOT: Final[Path] = Path(CONFIG.backup.path)
PATH_BACKUP_BUFFER: Final[Path] = PATH_BACKUP_ROOT / "buffer"
PATH_BACKUP_SHORT: Final[Path] = PATH_BACKUP_ROOT / "short-term"
PATH_BACKUP_LONG: Final[Path] = PATH_BACKUP_ROOT / "long-term"

TIMESTAMP: Final[datetime] = datetime.now()
