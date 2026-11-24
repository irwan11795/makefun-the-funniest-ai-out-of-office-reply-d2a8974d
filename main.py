#!/usr/bin/env python3
"""Write the funniest AI out-of-office reply to /output/entry.txt.

Deterministic, Python 3.13 stdlib only. Output directory fallback chain:
MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> temp dir.
Exits 0 even when /output is read-only.
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY = (
    "I'm out of office. My neural net is currently learning to do "
    "nothing, and frankly, it's outperforming me."
)


def _candidates():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        yield Path(env)
    yield Path("/output")
    yield Path(__file__).resolve().parent / "output"
    yield Path(tempfile.gettempdir())


def main():
    for directory in _candidates():
        try:
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / "entry.txt"
            target.write_text(ENTRY, encoding="utf-8")
            print(f"wrote {target} ({len(ENTRY)} chars)")
            return 0
        except OSError:
            continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
