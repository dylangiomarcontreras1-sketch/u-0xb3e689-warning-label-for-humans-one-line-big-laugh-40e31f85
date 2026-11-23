#!/usr/bin/env python3
"""Local stand-in for the sealed gate plus a determinism check.

The bounty has no local scorer (the server grades every entry), so this
reproduces the published gate -- /output/entry.txt is UTF-8 text of 1 to 160
characters and not only white space -- and proves the program writes the same
bytes on every run.

    python3 verify.py [--runs N]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile

MAX_CHARS = 160
MAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")


def gate(raw: bytes) -> list[str]:
    problems: list[str] = []
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("file starts with a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return problems + [f"not valid UTF-8: {exc}"]
    if not text.strip():
        problems.append("text is empty or only white space")
    if len(text) > MAX_CHARS:
        problems.append(f"{len(text)} characters, over the {MAX_CHARS} cap")
    if len(text.encode("utf-16-le")) // 2 > MAX_CHARS:
        problems.append("over the cap counted as UTF-16 code units")
    if len(raw) > MAX_CHARS * 4:
        problems.append("over the cap counted as bytes")
    if text != text.strip():
        problems.append("text starts or ends with white space")
    if "\n" in text or "\r" in text:
        problems.append("text spans more than one line")
    return problems


def run_once(out_dir: str) -> bytes:
    path = os.path.join(out_dir, "entry.txt")
    subprocess.run(
        [sys.executable, MAIN, path],
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"},
        timeout=60,
    )
    with open(path, "rb") as handle:
        return handle.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    runs: list[bytes] = []
    with tempfile.TemporaryDirectory() as tmp:
        for index in range(args.runs):
            out_dir = os.path.join(tmp, f"run-{index}")
            os.makedirs(out_dir)
            runs.append(run_once(out_dir))

    problems = gate(runs[0])
    digests = {hashlib.sha256(raw).hexdigest() for raw in runs}
    if len(digests) != 1:
        problems.append(f"output differs across {args.runs} runs: {sorted(digests)}")

    text = runs[0].decode("utf-8", "replace")
    print(f"entry:  {text}")
    print(f"chars:  {len(text)} / {MAX_CHARS}")
    print(f"bytes:  {len(runs[0])}")
    print(f"sha256: {sorted(digests)[0]}")
    print(f"runs:   {args.runs} identical" if len(digests) == 1 else "runs:   DIFFER")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print("PASS: gate and determinism")
    return 0


if __name__ == "__main__":
    sys.exit(main())
