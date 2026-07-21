#!/usr/bin/env python3

from contextlib import suppress
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen

from butler.constants import (
    CONFIG,
    PATH_BACKUP_BUFFER,
    PATH_BACKUP_SHORT,
    PATH_BACKUP_LONG,
    PATH_BUTLER_ROOT,
    PATH_FLAG_DIRTY,
    PATH_FLAG_VERSION,
    PATH_SCRIPTS,
    PATH_SERVER_JAR,
    PATH_SERVER_JAR_NEW,
    PATH_SYSTEMD_UNITS,
    TIMESTAMP,
)


def clear_backup_buffer() -> None:
    with suppress(FileNotFoundError):
        shutil.rmtree(PATH_BACKUP_BUFFER)
    PATH_BACKUP_BUFFER.mkdir(parents=True, exist_ok=True)
    PATH_BACKUP_SHORT.mkdir(parents=True, exist_ok=True)
    PATH_BACKUP_LONG.mkdir(parents=True, exist_ok=True)


def get_latest_backup(path: Path) -> Path | None:
    return backups[0] if (
        backups := sorted(path.glob("*.tar.zst"), reverse=True)
    ) else None


def verify_zstd(path: Path) -> None:
    if (result := subprocess.run(
        ["zstd", "-t", str(path)],
        capture_output=True,
        text=True,
    )).returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)


def sha1_file(path: Path) -> str:
    digest = hashlib.sha1()
    with open(path, "rb") as file:
        while chunk := file.read(65536):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_json(url: str) -> Any:
    with urlopen(url) as response:
        return json.load(response)


def prune_backups(path: Path, retention: int) -> None:
    for backup in sorted(
        path.glob("*.tar.zst"),
        reverse=True,
    )[retention:]:
        backup.unlink()


def get_restore_path() -> Path | None:
    clear_backup_buffer()
    restore_path = None

    if len(sys.argv) > 1:
        print(
            (
                "Manual restoration requested. "
                "Attempting to locate specified backup: "
                f"{sys.argv[1]}..."
            ),
            flush=True,
        )

        shortterm_candidate = PATH_BACKUP_SHORT / sys.argv[1]
        longterm_candidate = PATH_BACKUP_LONG / sys.argv[1]

        if shortterm_candidate.exists():
            restore_path = shortterm_candidate
        elif longterm_candidate.exists():
            restore_path = longterm_candidate
        else:
            print(
                "Specified backup not found.",
                flush=True,
                file=sys.stderr,
            )
            sys.exit(1)

    elif PATH_FLAG_DIRTY.exists():
        print(
            (
                "Dirty state detected. "
                "Automatically restoring from latest backup..."
            ),
            flush=True,
        )

        restore_path = (
            get_latest_backup(PATH_BACKUP_SHORT)
            or get_latest_backup(PATH_BACKUP_LONG)
        )

        if restore_path is None:
            print(
                "No backups found.",
                flush=True,
                file=sys.stderr,
            )
            sys.exit(1)

    return restore_path


def restore(path: Path) -> None:
    print(
        f"Attempting to restore from backup: {path}...",
        flush=True,
    )

    subprocess.run(
        [
            "tar",
            "--zstd",
            "-xf",
            path,
            "-C",
            PATH_BACKUP_BUFFER,
        ],
        check=True,
    )

    subprocess.run(
        [
            "rsync",
            "--archive",
            "--delete",
            "--checksum",
            f"--exclude={PATH_SCRIPTS.relative_to(PATH_BUTLER_ROOT)}",
            f"--exclude={PATH_SYSTEMD_UNITS.relative_to(PATH_BUTLER_ROOT)}",
            f"--exclude={PATH_FLAG_DIRTY.relative_to(PATH_BUTLER_ROOT)}",
            f"{PATH_BACKUP_BUFFER}/",
            f"{PATH_BUTLER_ROOT}/",
        ],
        check=True,
    )

    clear_backup_buffer()

    print(
        "Restoration complete.",
        flush=True,
    )


def backup() -> None:
    print(
        "Backing up...",
        flush=True,
    )

    new_shortterm = (
        TIMESTAMP.strftime("%Y-%m-%d_%H-%M-%S")
        + ".tar.zst"
    )

    backup_file = PATH_BACKUP_BUFFER / new_shortterm

    subprocess.run(
        [
            "tar",
            "--zstd",
            "-cf", backup_file,
            "-C", PATH_BUTLER_ROOT,
            ".",
        ],
        check=True,
    )

    try:
        verify_zstd(backup_file)
    except RuntimeError as error:
        clear_backup_buffer()
        print(
            f"New short-term backup integrity check failed.\n{error}",
            flush=True,
            file=sys.stderr,
        )
        sys.exit(1)

    destination = PATH_BACKUP_SHORT / new_shortterm
    backup_file.rename(destination)

    print(
        f"New short-term backup created: {destination}",
        flush=True,
    )

    current_month = TIMESTAMP.strftime("%Y-%m")

    if not list(PATH_BACKUP_LONG.glob(f"{current_month}*.tar.zst")):

        new_longterm = sorted(
            PATH_BACKUP_SHORT.glob(f"{current_month}*.tar.zst")
        )[0].name

        shutil.copy2(
            PATH_BACKUP_SHORT / new_longterm,
            PATH_BACKUP_BUFFER / new_longterm,
        )

        try:
            verify_zstd(PATH_BACKUP_BUFFER / new_longterm)
        except RuntimeError as error:
            clear_backup_buffer()
            print(
                f"New long-term backup integrity check failed.\n{error}",
                flush=True,
                file=sys.stderr,
            )
            sys.exit(1)

        destination = (PATH_BACKUP_LONG / new_longterm)
        (PATH_BACKUP_BUFFER / new_longterm).rename(destination)

        print(
            f"New long-term backup created: {destination}",
            flush=True,
        )

    prune_backups(PATH_BACKUP_SHORT, CONFIG.backup.retention_short)
    prune_backups(PATH_BACKUP_LONG, CONFIG.backup.retention_long)
    clear_backup_buffer()

    print(
        "Backup complete.",
        flush=True,
    )


def auto_update() -> None:
    if not CONFIG.server.auto_update:
        print(
            (
                "Automatic updates currently disabled. "
                "Skipping automatic update..."
            ),
            flush=True,
        )
        PATH_FLAG_VERSION.unlink(missing_ok=True)
        return

    print(
        "Automatic updates currently enabled. Checking for updates...",
        flush=True,
    )

    try:
        manifest = fetch_json(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        )
    except URLError:
        print(
            "Could not reach Mojang. Skipping automatic update...",
            flush=True,
        )
        return

    server_version = (
        PATH_FLAG_VERSION.read_text().strip()
        if PATH_FLAG_VERSION.exists() else "unknown"
    )

    print(
        f"Server version: {server_version}",
        flush=True,
    )

    latest_version = manifest["latest"]["release"]

    print(
        f"Latest release: {latest_version}",
        flush=True,
    )

    if server_version == latest_version:
        print(
            "Server already up to date. Skipping automatic update...",
            flush=True,
        )
        return

    print(
        f"Updating to latest release: {latest_version}...",
        flush=True,
    )

    try:
        version_json = fetch_json(next(
            version["url"]
            for version in manifest["versions"]
            if version["id"] == latest_version
        ))
    except URLError:
        print(
            "Could not reach Mojang. Skipping automatic update...",
            flush=True,
        )
        return

    with urlopen(version_json["downloads"]["server"]["url"]) as response:
        PATH_SERVER_JAR_NEW.write_bytes(response.read())

    if (
        sha1_file(PATH_SERVER_JAR_NEW)
        != version_json["downloads"]["server"]["sha1"]
    ):
        PATH_SERVER_JAR_NEW.unlink(missing_ok=True)
        print(
            "Update integrity check failed.",
            flush=True,
            file=sys.stderr,
        )
        sys.exit(1)

    PATH_SERVER_JAR_NEW.replace(PATH_SERVER_JAR)
    PATH_FLAG_VERSION.write_text(latest_version)

    print(
        f"Successfully updated to new version: {latest_version}",
        flush=True,
    )


def main() -> None:
    if (restore_path := get_restore_path()) is not None:
        restore(restore_path)
    else:
        backup()
    auto_update()


if __name__ == "__main__":
    main()
