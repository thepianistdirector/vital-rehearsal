"""Trusted built-in integer control. No dynamic models, imports or expressions.

This producer deliberately does not import evaluator reference/criteria modules.
"""

import csv
import json
import os
from pathlib import Path
import resource
import signal
import time

FAULTS = (
    "none", "perturbed", "wrong-unit", "truncated", "nonfinite", "impossible",
    "nonconvergence", "crash", "pause",
)


def execute(output: Path, fault: str):
    if fault not in FAULTS:
        return 2
    # Linux-only resource controls. They do not provide security isolation.
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (2, 3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    # A hard-killed coordinator cannot leave this control worker alive indefinitely.
    signal.alarm(4)
    if fault == "pause":
        with (output / "trajectory.csv").open("w", encoding="utf-8") as partial:
            partial.write("time[s],counter[1]\n0,0\n1,1\n")
            partial.flush()
            os.fsync(partial.fileno())
        print("Injected pause for timeout/interruption verification", flush=True)
        time.sleep(60)
    if fault == "crash":
        print("Injected control process failure", flush=True)
        return 7
    if fault == "nonconvergence":
        diagnostics = {
            "schema_version": 1, "model_id": "integer-counter-control-v1",
            "solver": "integer-enumeration", "solver_version": "1",
            "state": "FAILED_NUMERICAL", "samples": 0, "fault": fault,
        }
        (output / "diagnostics.json").write_text(json.dumps(diagnostics) + "\n")
        return 0
    points = []
    for tick in range(5):
        value = tick
        if fault == "perturbed" and tick == 2:
            value = 2.25
        if fault == "nonfinite" and tick == 2:
            value = "nan"
        if fault == "impossible" and tick == 2:
            value = -1
        points.append((tick, value))
    if fault == "truncated":
        points.pop()
    with (output / "trajectory.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["time[s]", "counter[mL]" if fault == "wrong-unit" else "counter[1]"])
        writer.writerows(points)
        stream.flush()
        os.fsync(stream.fileno())
    diagnostics = {
        "schema_version": 1, "model_id": "integer-counter-control-v1",
        "solver": "integer-enumeration", "solver_version": "1",
        "state": "COMPLETED", "samples": len(points), "fault": fault,
    }
    (output / "diagnostics.json").write_text(json.dumps(diagnostics) + "\n")
    print("Built-in software control finished; no physiology executed", flush=True)
    return 0
