#!/usr/bin/env python3
"""Run the complete dependency-free project health check."""

from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    [sys.executable, "scripts/validate_data.py"],
    [sys.executable, "scripts/build_site.py"],
]


def main() -> None:
    for command in COMMANDS:
        subprocess.run(command, check=True)
    print("Project checks passed.")


if __name__ == "__main__":
    main()

