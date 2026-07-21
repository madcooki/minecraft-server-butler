#!/usr/bin/env python3

import os

from butler.constants import (
    CONFIG,
    PATH_FLAG_DIRTY,
    PATH_SERVER_JAR,
)


def main() -> None:
    PATH_FLAG_DIRTY.touch()
    args = [
        "java",
        *CONFIG.server.launch_options.split(),
        "-jar",
        str(PATH_SERVER_JAR),
        "nogui",
    ]

    os.execvp(args[0], args)


if __name__ == "__main__":
    main()
