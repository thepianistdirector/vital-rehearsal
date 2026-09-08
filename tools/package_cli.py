#!/usr/bin/env python3
"""Build a deterministic dependency-free development zipapp; no publication."""

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from vital_rehearsal import __version__
from vital_rehearsal.packaging import archive_bytes


def build(destination=None):
    destination = destination or ROOT / "dist" / f"vital-rehearsal-{__version__}.pyz"
    payload = archive_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_bytes() != payload:
        raise FileExistsError("different artifact already exists; choose a new build output path")
    if not destination.exists():
        with destination.open("xb") as stream:
            stream.write(payload)
        destination.chmod(0o755)
    sha = hashlib.sha256(payload).hexdigest()
    print(f"LOCAL RELEASE CANDIDATE (not publicly released): {destination.name}\nSHA256 {sha}")
    return destination


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) == 2 else None)
