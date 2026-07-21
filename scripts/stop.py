#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import time

from butler.constants import (
    CONFIG,
    PATH_FLAG_DIRTY,
    PATH_FLAG_TIMESTAMP,
    TIMESTAMP,
)


def main() -> None:
    minecraft_pid = int(subprocess.run(
        [
            "systemctl",
            "show",
            "-p",
            "MainPID",
            "--value",
            "minecraft.service",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip())

    if minecraft_pid == 0:
        print(
            "Systemd minecraft.service process is not running.",
            flush=True,
        )
        sys.exit()

    print(
        "Waiting for RCON to respond...",
        flush=True,
    )

    for _ in range(60):
        if subprocess.run(
            [
                "mcrcon",
                "-P", str(CONFIG.mcrcon.port),
                "-p", CONFIG.mcrcon.password,
                "list",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0:
            print(
                "RCON ready.",
                flush=True,
            )
            break
        time.sleep(1)
    else:
        print(
            "RCON did not respond in time. Sending SIGTERM...",
            flush=True,
            file=sys.stderr,
        )
        os.kill(minecraft_pid, signal.SIGTERM)
        sys.exit(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 10 minutes.\"}",
    ])
    print(
        "The server will restart in 10 minutes.",
        flush=True,
    )
    time.sleep(300)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 5 minutes.\"}",
    ])
    print(
        "The server will restart in 5 minutes.",
        flush=True,
    )
    time.sleep(240)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 1 minute.\"}",
    ])
    print(
        "The server will restart in 1 minute.",
        flush=True,
    )
    time.sleep(50)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 10 seconds!\"}",
    ])
    print(
        "The server will restart in 10 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 9 seconds!\"}",
    ])
    print(
        "The server will restart in 9 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 8 seconds!\"}",
    ])
    print(
        "The server will restart in 8 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 7 seconds!\"}",
    ])
    print(
        "The server will restart in 7 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 6 seconds!\"}",
    ])
    print(
        "The server will restart in 6 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 5 seconds!\"}",
    ])
    print(
        "The server will restart in 5 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 4 seconds!\"}",
    ])
    print(
        "The server will restart in 4 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 3 seconds!\"}",
    ])
    print(
        "The server will restart in 3 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 2 seconds!\"}",
    ])
    print(
        "The server will restart in 2 seconds!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server will restart in 1 second!\"}",
    ])
    print(
        "The server will restart in 1 second!",
        flush=True,
    )
    time.sleep(1)

    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "tellraw @a {\"color\":\"red\",\"text\":"
        "\"[Server] The server is restarting now!\"}",
    ])
    print(
        "The server is restarting now!",
        flush=True,
    )
    time.sleep(1)

    print(
        "Requesting clean shutdown through RCON...",
        flush=True,
    )
    subprocess.run([
        "mcrcon",
        "-P", str(CONFIG.mcrcon.port),
        "-p", CONFIG.mcrcon.password,
        "stop",
    ])

    while True:
        try:
            os.kill(minecraft_pid, 0)
        except ProcessLookupError:
            break
        time.sleep(1)

    PATH_FLAG_TIMESTAMP.write_text(
        TIMESTAMP.strftime("%Y-%m-%d %H:%M:%S"),
        encoding="utf-8",
    )
    PATH_FLAG_DIRTY.unlink()
    print(
        "Clean shutdown confirmed.",
        flush=True,
    )


if __name__ == "__main__":
    main()
