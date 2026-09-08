#!/usr/bin/env python3
"""Exercise a packaged control in a fresh project-local directory; no publication."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent.parent


def record(package: Path):
    directory = ROOT / "runs" / "packaged-evidence" / uuid.uuid4().hex
    directory.mkdir(parents=True)
    runner = directory / "runner.pyz"
    shutil.copyfile(package, runner)
    environment = {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    steps = []
    attempts = directory / "attempts"

    def invoke(name, arguments, expected=0):
        execution = subprocess.run([sys.executable, "-I", str(runner), *arguments],
                                   cwd=directory, env=environment, capture_output=True, text=True, timeout=8)
        parsed = json.loads(execution.stdout)
        sanitized = dict(parsed)
        if "bundle" in sanitized:
            sanitized["bundle"] = "attempts/" + Path(sanitized["bundle"]).name
        steps.append({"step": name, "arguments": arguments, "exit_code": execution.returncode, "result": sanitized})
        if execution.returncode != expected:
            raise RuntimeError(f"unexpected exit in {name}: {execution.returncode}")
        return parsed

    try:
        invoke("create fixed study", ["example", "--output", "study.json"])
        invoke("validate before execution", ["validate", "study.json"])
        first = invoke("execute reference control", ["run", "study.json", "--output", "attempts"])
        first_bundle = Path(first["bundle"])
        previous_manifest = (first_bundle / "manifest.json").read_bytes()
        inspected = invoke("inspect independent comparison", ["inspect", "attempts/" + first_bundle.name])
        if inspected["result"]["evaluation"]["conclusion"] != "CONTROL_AGREEMENT":
            raise RuntimeError("control did not agree")
        contrary = invoke("retain contradiction", ["run", "study.json", "--output", "attempts", "--control-fault", "perturbed"], 1)
        if contrary["execution_state"] != "COMPLETED" or contrary["conclusion"] != "CONTRADICTED":
            raise RuntimeError("completion was confused with agreement")
        invoke("retain timeout and partial raw output", ["run", "study.json", "--output", "attempts", "--control-fault", "pause"], 1)

        for name, sig, expected in (("graceful interruption", signal.SIGTERM, 130), ("hard interruption", signal.SIGKILL, -signal.SIGKILL)):
            process = subprocess.Popen([sys.executable, "-I", str(runner), "run", "study.json", "--output", "attempts", "--control-fault", "pause"],
                                       cwd=directory, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                deadline = time.monotonic() + 3
                while time.monotonic() < deadline:
                    if any(path.stat().st_size > 0 for path in attempts.glob("*.partial/trajectory.csv")):
                        break
                    if process.poll() is not None:
                        raise RuntimeError("packaged coordinator stopped before interruption")
                    time.sleep(.01)
                else:
                    raise RuntimeError("packaged coordinator did not produce partial output")
                process.send_signal(sig)
                stdout, stderr = process.communicate(timeout=3)
                if process.returncode != expected:
                    raise RuntimeError("unexpected interruption exit")
                steps.append({"step": name, "signal": sig.name, "exit_code": process.returncode,
                              "partial_numeric_output_observed": True})
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=2)
        listing = invoke("identify interrupted evidence", ["list-attempts", "--output", "attempts"])
        states = {item["state"] for item in listing["attempts"]}
        if not {"COMPLETED", "TIMED_OUT", "CANCELLED", "PARTIAL_INTERRUPTED"} <= states:
            raise RuntimeError("recovery states missing")
        replay = invoke("rerun after interruption", ["run", "study.json", "--output", "attempts"])
        if replay["attempt_id"] == first["attempt_id"] or previous_manifest != (first_bundle / "manifest.json").read_bytes():
            raise RuntimeError("rerun overwrote previous evidence")
        invoke("recheck preserved original", ["inspect", "attempts/" + first_bundle.name])
        # Give the hard-killed parent's worker time to reach its independently enforced alarm.
        time.sleep(4.1)
        result = {
            "status": "RUNTIME VERIFIED — SOFTWARE CONTROL ONLY",
            "package_sha256": hashlib.sha256(runner.read_bytes()).hexdigest(),
            "python": sys.version.split()[0], "environment": "fresh project-local cwd; scrubbed env; isolated Python imports; same host",
            "external_human": "NOT PERFORMED", "physiology": "NOT PERFORMED", "public_release": "NOT PERFORMED",
            "reference_attempt": first["attempt_id"], "contradicted_attempt": contrary["attempt_id"],
            "steps": steps,
        }
    except Exception as exc:
        result = {"status": "FAILED", "reason": type(exc).__name__, "steps": steps}
        (directory / "runtime-evidence.json").write_text(json.dumps(result, indent=2) + "\n")
        raise
    (directory / "runtime-evidence.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"directory": str(directory), "status": result["status"], "package_sha256": result["package_sha256"]}, indent=2))
    return directory


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 tools/record_control_evidence.py project-local-runner.pyz")
    record(Path(sys.argv[1]).resolve())
