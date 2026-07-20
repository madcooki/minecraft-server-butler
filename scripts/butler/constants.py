from pathlib import Path
from typing import Final

from butler.config import (
    ButlerConfig,
    load_butler_config,
)


PATH_BUTLER_ROOT: Final[Path] = Path("/opt/minecraft-server-butler")
PATH_INI: Final[Path] = PATH_BUTLER_ROOT / "butler.ini"

CONFIG: Final[ButlerConfig] = load_butler_config(PATH_INI)
