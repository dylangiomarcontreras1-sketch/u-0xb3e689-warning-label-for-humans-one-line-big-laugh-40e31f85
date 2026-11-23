#!/usr/bin/env python3
"""make.fun program/v1 entry: write one warning label line to /output/entry.txt.

Standard library only, no network, no clock, no randomness: every run writes
the same bytes.
"""

from __future__ import annotations

import os
import sys
import tempfile

ENTRY = "WARNING: This unit contains small parts. Will lose them. Will blame you."
MAX_CHARS = 160
DEFAULT_OUTPUT = "/output/entry.txt"


def render() -> str:
    """Return the entry line exactly as it is judged."""
    return ENTRY


def check(text: str) -> None:
    """Fail loudly rather than submit an entry the gate would refuse."""
    if not text or not text.strip():
        raise ValueError("entry must be non-empty, non-whitespace text")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over the {MAX_CHARS} cap")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in text):
        raise ValueError("entry must be one printable line: no control characters")
    text.encode("utf-8")


def write(path: str, text: str) -> None:
    """Write UTF-8 with no newline translation, atomically where possible."""
    parent = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(parent, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=parent, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


USAGE = """usage: main.py [OUTPUT_PATH | --print | --check]

  (no argument)  write the entry line to /output/entry.txt
  OUTPUT_PATH    write it there instead, for local checks
  --print        print it to stdout, write nothing
  --check        validate it against the gate, write nothing
"""


def main(argv: list[str]) -> int:
    arg = argv[1] if len(argv) > 1 else DEFAULT_OUTPUT
    text = render()
    check(text)
    if arg in ("-h", "--help"):
        print(USAGE, end="")
        return 0
    if arg == "--check":
        print(f"ok: {len(text)} characters, valid")
        return 0
    if arg == "--print":
        print(text)
        return 0
    write(arg, text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
