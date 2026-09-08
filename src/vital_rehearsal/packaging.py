"""Deterministic original-source zipapp for offline development reproduction."""

from io import BytesIO
import importlib.resources
import zipfile


def archive_bytes():
    package = importlib.resources.files("vital_rehearsal")
    files = {"__main__.py": b"from vital_rehearsal.cli import main\nraise SystemExit(main())\n"}
    for item in package.iterdir():
        if item.name.endswith((".py", ".txt", ".cellml")) or item.name == "LICENSE":
            files[f"vital_rehearsal/{item.name}"] = item.read_bytes()
    files["LICENSE"] = package.joinpath("LICENSE").read_bytes()
    data = BytesIO()
    data.write(b"#!/usr/bin/env python3\n")
    with zipfile.ZipFile(data, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return data.getvalue()
