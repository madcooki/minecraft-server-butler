from dataclasses import dataclass
from configparser import ConfigParser
from pathlib import Path


@dataclass(frozen=True)
class ServerConfig:
    auto_update: bool
    launch_options: str


@dataclass(frozen=True)
class McrconConfig:
    password: str
    port: int


@dataclass(frozen=True)
class BackupConfig:
    path: Path
    retention_short: int
    retention_long: int


@dataclass(frozen=True)
class ButlerConfig:
    server: ServerConfig
    mcrcon: McrconConfig
    backup: BackupConfig


def load_butler_config(ini: Path) -> ButlerConfig:
    parser: ConfigParser = ConfigParser()
    parser.read(ini)

    return ButlerConfig(
        server=ServerConfig(
            auto_update=bool(parser["server"]["auto_update"]),
            launch_options=str(parser["server"]["launch_options"]),
        ),
        mcrcon=McrconConfig(
            password=str(parser["mcrcon"]["password"]),
            port=int(parser["mcrcon"]["port"]),
        ),
        backup=BackupConfig(
            path=Path(parser["backup"]["path"]),
            retention_short=int(parser["backup"]["retention_short"]),
            retention_long=int(parser["backup"]["retention_long"]),
        ),
    )
