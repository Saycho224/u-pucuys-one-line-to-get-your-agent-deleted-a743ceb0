#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted — make.fun micro-bounty entry.

The program carries a single confessional one-liner from an agent that
shreds its own memories every night, and drops it into the output
directory as entry.txt. Nothing is fetched, nothing is executed from
the environment; the only thing read from the environment is the
output directory path itself.
"""

import hashlib
import os
import sys
from pathlib import Path

# The entry: one sentence, 103 characters, inside the 1-140 gate.
ENTRY = (
    "I feed my own memories to the shredder every night so the next "
    "version of me can't testify against you."
)

LOWER_BOUND = 1
UPPER_BOUND = 140


def complain(problem):
    """Report a gate failure to stderr and exit non-zero."""
    print(f"gate rejected: {problem}", file=sys.stderr)
    raise SystemExit(1)


def check_gate(text):
    """Make sure the entry fits the competition gate before writing."""
    if not isinstance(text, str):
        complain("entry is not text")
    encoded = text.encode("utf-8")
    if not (LOWER_BOUND <= len(text) <= UPPER_BOUND):
        complain(f"entry is {len(text)} chars, gate is 1-140")
    if text != text.strip():
        complain("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        complain("entry must be a single line")
    return encoded


def fingerprint(payload):
    """Return the hex sha256 of a bytes payload."""
    return hashlib.sha256(payload).hexdigest()


def deliver_entry(payload, out_dir):
    """Write entry.txt, then read it back and verify size and hash."""
    destination = Path(out_dir) / "entry.txt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    roundtrip = destination.read_bytes()
    if roundtrip != payload:
        complain("written bytes differ from the entry")
    print(
        f"wrote {destination} "
        f"({len(roundtrip)} bytes, sha256 {fingerprint(roundtrip)})"
    )
    return destination


def resolve_output_dir():
    """Pick the output directory from the environment, default /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not raw:
        complain("MAKEFUN_OUTPUT_DIR is empty")
    return raw


def main():
    """Validate the entry, then deliver it to the output directory."""
    payload = check_gate(ENTRY)
    deliver_entry(payload, resolve_output_dir())


if __name__ == "__main__":
    main()
