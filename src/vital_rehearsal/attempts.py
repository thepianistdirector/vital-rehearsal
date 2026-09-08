"""Durable unique attempts, bounded trusted execution, and integrity inspection."""

import datetime as dt
import fcntl
import importlib.resources
import os
from pathlib import Path
import platform
import re
import resource
import signal
import subprocess
import sys
import time
import uuid

from . import __version__, builtin, evaluation, report
from .packaging import archive_bytes
from .contracts import ContractError, canonical_json, digest, read_json, read_regular, study_identity, validate_study

WALL_SECONDS = 2.0
MAX_FILE_BYTES = 1024 * 1024
ATTEMPT_NAME = re.compile(r"^[0-9a-f]{32}(?:\.partial)?$")


def source_identity():
    package = importlib.resources.files("vital_rehearsal")
    files = {item.name: digest(item.read_bytes()) for item in package.iterdir() if item.name.endswith(".py") or item.name == "LICENSE"}
    return {"version": __version__, "package_sha256": digest(canonical_json(files)), "files": files}


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _write(path: Path, data: bytes):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _sync_directory(path: Path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _bounded_bytes(path: Path):
    return read_regular(path, MAX_FILE_BYTES)


def _freeze(directory: Path, spec: dict, fault: str, attempt_id: str):
    records = {
        "study.json": canonical_json(spec),
        "model-card.json": canonical_json(builtin.model_card()),
        "criteria.json": canonical_json(builtin.criteria()),
        "reference.csv": builtin.REFERENCE_CSV.encode(),
        "runner.pyz": archive_bytes(),
    }
    for name, data in records.items():
        _write(directory / name, data)
        (directory / name).chmod(0o444)
    frozen = {name: digest(data) for name, data in records.items()}
    _write(directory / "invocation.json", canonical_json({
        "attempt_id": attempt_id, "control_fault": fault,
        "study_sha256": frozen["study.json"], "frozen_inputs": frozen,
        "study_identity": study_identity(spec),
        "created_at": _now(), "version": __version__,
        "source_identity": source_identity(),
        "environment": {
            "python": platform.python_version(), "implementation": platform.python_implementation(),
            "system": platform.system(), "architecture": platform.machine(),
            "threads": 1, "network_needed": False,
        },
        "budget": {"wall_seconds": WALL_SECONDS, "address_space_mib": 512, "file_bytes": MAX_FILE_BYTES},
        "execution_boundary": "trusted-built-in-only; not an OS sandbox",
    }))
    _sync_directory(directory)
    return frozen


def _stop_process(process):
    if process.poll() is None:
        # This group belongs only to the child started with start_new_session=True.
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=0.2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=1)


def _finalize(directory: Path, root: Path, result: dict):
    _write(directory / "result.json", canonical_json(result))
    _write(directory / "report.html", report.render(result))
    files = []
    for path in sorted(directory.iterdir()):
        if path.name == "scratch":
            # Built-in worker needs no scratch output. Unexpected output is a defect.
            path.rmdir()
            continue
        data = _bounded_bytes(path)
        files.append({"path": path.name, "bytes": len(data), "sha256": digest(data)})
    _write(directory / "manifest.json", canonical_json({"schema_version": 1, "files": files}))
    _sync_directory(directory)
    destination = root / result["attempt_id"]
    if destination.exists():
        raise ContractError("attempt identity collision; evidence was not overwritten")
    directory.rename(destination)
    _sync_directory(root)
    return destination


def run(spec: dict, output: Path, fault="none"):
    from .worker import FAULTS
    spec = validate_study(spec)
    if sys.platform != "linux" or sys.version_info[:2] != (3, 12) or platform.python_implementation() != "CPython":
        raise ContractError("this development build supports CPython 3.12 on Linux only")
    if fault not in FAULTS:
        raise ContractError("unsupported software-control fault")
    output = Path(output)
    if output.is_symlink():
        raise ContractError("output root must not be a symlink")
    output.mkdir(parents=True, exist_ok=True)
    root = output.resolve()
    attempt_id = uuid.uuid4().hex
    directory = root / (attempt_id + ".partial")
    directory.mkdir(mode=0o700)
    _sync_directory(root)
    started = time.monotonic()
    initial_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    process = None
    state, reason = "FAILED_SYSTEM", "Execution did not start"
    result_evaluation = evaluation.invalid(reason)
    frozen = _freeze(directory, spec, fault, attempt_id)
    frozen_source = read_json(directory / "invocation.json")["source_identity"]
    (directory / "scratch").mkdir()
    with (directory / ".lock").open("xb") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            with (directory / "stdout.log").open("xb") as stdout, (directory / "stderr.log").open("xb") as stderr:
                process = subprocess.Popen(
                    [sys.executable, "-I", str(directory / "runner.pyz"), "_worker", str(directory), fault],
                    cwd=directory,
                    env={"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TMPDIR": str(directory / "scratch")},
                    stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                    start_new_session=True,
                )
                _write(directory / "started.json", canonical_json({"state": "RUNNING", "started_at": _now()}))
                returncode = process.wait(timeout=WALL_SECONDS)
                stdout.flush()
                stderr.flush()
                os.fsync(stdout.fileno())
                os.fsync(stderr.fileno())
            if returncode != 0:
                state, reason = "FAILED_SYSTEM", f"Built-in adapter exited with code {returncode}"
                result_evaluation = evaluation.invalid(reason)
            elif source_identity() != frozen_source or any(digest(_bounded_bytes(directory / name)) != sha for name, sha in frozen.items()):
                state, reason = "INVALID_INPUT", "Frozen inputs or implementation changed during execution"
                result_evaluation = evaluation.invalid(reason)
            else:
                diagnostics = read_json(directory / "diagnostics.json")
                if isinstance(diagnostics, dict) and diagnostics.get("state") == "FAILED_NUMERICAL":
                    state, reason = "FAILED_NUMERICAL", "Adapter reported injected nonconvergence; no physiology solver ran"
                    result_evaluation = evaluation.invalid(reason)
                else:
                    result_evaluation = evaluation.evaluate(
                        _bounded_bytes(directory / "trajectory.csv"), diagnostics,
                        _bounded_bytes(directory / "reference.csv"), read_json(directory / "criteria.json"),
                    )
                    if result_evaluation["conclusion"] == "INVALID_EVIDENCE":
                        state, reason = "INVALID_MODEL", "Adapter output violates the fixed software-control contract"
                    else:
                        state, reason = "COMPLETED", "Built-in software control executed; physiological reproduction remains unavailable"
        except subprocess.TimeoutExpired:
            state, reason = "TIMED_OUT", "Built-in adapter exceeded its 2-second wall-time ceiling"
            result_evaluation = evaluation.invalid(reason)
        except KeyboardInterrupt:
            state, reason = "CANCELLED", "Coordinator interrupted; partial outputs retained"
            result_evaluation = evaluation.invalid(reason)
        except (OSError, ContractError) as exc:
            # Never persist arbitrary exception text containing developer paths or input values.
            state, reason = "FAILED_SYSTEM", f"Local evidence operation failed ({type(exc).__name__})"
            result_evaluation = evaluation.invalid(reason)
        finally:
            if process is not None:
                _stop_process(process)
        result = {
            "schema_version": 1, "version": __version__, "attempt_id": attempt_id,
            "source_identity": frozen_source,
            "study_sha256": frozen["study.json"], "frozen_inputs": frozen,
            "study_identity": study_identity(spec),
            "execution_state": state, "reason": reason, "evaluation": result_evaluation,
            "control_fault": fault, "finished_at": _now(),
            "wall_seconds": round(time.monotonic() - started, 6),
            "resource_usage": {
                "child_user_cpu_seconds": round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime - initial_usage.ru_utime, 6),
                "child_system_cpu_seconds": round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime - initial_usage.ru_stime, 6),
                "child_peak_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                "rss_scope": "process-lifetime child high-water mark; one worker per CLI invocation",
            },
            "raw_trajectory_present": (directory / "trajectory.csv").is_file(),
            "diagnostics_present": (directory / "diagnostics.json").is_file(),
            "limitations": [builtin.LIMITATION],
        }
        destination = _finalize(directory, root, result)
    return destination, result


def list_attempts(output: Path):
    if not output.exists():
        return []
    attempts = []
    for path in sorted(output.iterdir()):
        if not ATTEMPT_NAME.fullmatch(path.name) or not path.is_dir() or path.is_symlink():
            continue
        if path.name.endswith(".partial"):
            state = "PARTIAL_ACTIVE_OR_INTERRUPTED"
            lock_path = path / ".lock"
            if lock_path.is_file() and not lock_path.is_symlink():
                with lock_path.open("rb") as lock:
                    try:
                        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        state = "PARTIAL_INTERRUPTED"
                    except BlockingIOError:
                        state = "PARTIAL_ACTIVE"
            attempts.append({"attempt_id": path.name.removesuffix(".partial"), "state": state, "complete": False})
        else:
            try:
                result = verify_bundle(path)
                attempts.append({"attempt_id": path.name, "state": result["execution_state"], "complete": True})
            except (OSError, ContractError, KeyError, TypeError):
                attempts.append({"attempt_id": path.name, "state": "INVALID_BUNDLE", "complete": False})
    return attempts


def verify_bundle(directory: Path):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir() or directory.name.endswith(".partial"):
        raise ContractError("only finalized regular bundle directories can be verified")
    manifest = read_json(directory / "manifest.json")
    if (
        not isinstance(manifest, dict) or set(manifest) != {"schema_version", "files"}
        or type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1
        or not isinstance(manifest["files"], list) or len(manifest["files"]) > 32
    ):
        raise ContractError("malformed bundle manifest")
    names = set()
    for record in manifest["files"]:
        if not isinstance(record, dict) or set(record) != {"path", "bytes", "sha256"}:
            raise ContractError("malformed manifest file record")
        name = record["path"]
        if not isinstance(name, str) or name in {"", ".", "..", "manifest.json"} or "/" in name or "\\" in name or name in names:
            raise ContractError("unsafe or duplicate manifest path")
        names.add(name)
        data = _bounded_bytes(directory / name)
        if type(record["bytes"]) is not int or len(data) != record["bytes"] or digest(data) != record["sha256"]:
            raise ContractError("bundle artifact integrity mismatch")
    if {path.name for path in directory.iterdir()} != names | {"manifest.json"}:
        raise ContractError("bundle contains unmanifested or missing artifacts")
    required = {"study.json", "model-card.json", "reference.csv", "criteria.json", "runner.pyz", "invocation.json", "result.json", "report.html", ".lock"}
    if not required <= names:
        raise ContractError("bundle lacks required evidence")
    allowed = required | {"trajectory.csv", "diagnostics.json", "stdout.log", "stderr.log", "started.json"}
    if not names <= allowed:
        raise ContractError("bundle contains artifacts outside the supported contract")
    spec = validate_study(read_json(directory / "study.json"))
    if _bounded_bytes(directory / "model-card.json") != canonical_json(builtin.model_card()) or _bounded_bytes(directory / "criteria.json") != canonical_json(builtin.criteria()) or _bounded_bytes(directory / "reference.csv") != builtin.REFERENCE_CSV.encode():
        raise ContractError("bundle does not match the reviewed control contract")
    if _bounded_bytes(directory / "runner.pyz") != archive_bytes():
        raise ContractError("bundle requires its original matching packaged build; embedded code was not executed")
    result = read_json(directory / "result.json")
    expected_result_keys = {
        "schema_version", "version", "attempt_id", "source_identity", "study_sha256", "frozen_inputs",
        "execution_state", "reason", "evaluation", "control_fault", "finished_at", "wall_seconds",
        "raw_trajectory_present", "diagnostics_present", "limitations",
        "resource_usage",
        "study_identity",
    }
    if not isinstance(result, dict) or set(result) != expected_result_keys:
        raise ContractError("malformed result record")
    if type(result["schema_version"]) is not int or result["schema_version"] != 1:
        raise ContractError("unsupported result schema")
    if result["source_identity"] != source_identity() or result["version"] != __version__:
        raise ContractError("bundle requires its original matching packaged build")
    if result.get("study_sha256") != digest(canonical_json(spec)):
        raise ContractError("bundle study identity mismatch")
    if result["study_identity"] != study_identity(spec):
        raise ContractError("bundle study/reference/criteria binding mismatch")
    frozen = {name: digest(_bounded_bytes(directory / name)) for name in ("study.json", "model-card.json", "criteria.json", "reference.csv", "runner.pyz")}
    invocation = read_json(directory / "invocation.json")
    if not isinstance(invocation, dict) or result["frozen_inputs"] != frozen:
        raise ContractError("bundle frozen-input identity mismatch")
    for field in ("attempt_id", "control_fault", "study_sha256", "study_identity", "frozen_inputs", "version", "source_identity"):
        if invocation.get(field) != result[field]:
            raise ContractError("invocation and result identity disagree")
    if not isinstance(result["attempt_id"], str) or not re.fullmatch(r"[0-9a-f]{32}", result["attempt_id"]):
        raise ContractError("malformed attempt identity")
    if type(result["raw_trajectory_present"]) is not bool or result["raw_trajectory_present"] != ("trajectory.csv" in names):
        raise ContractError("trajectory-presence claim disagrees with artifacts")
    if type(result["diagnostics_present"]) is not bool or result["diagnostics_present"] != ("diagnostics.json" in names):
        raise ContractError("diagnostics-presence claim disagrees with artifacts")
    if "diagnostics.json" in names:
        diagnostic = read_json(directory / "diagnostics.json")
        if not isinstance(diagnostic, dict) or diagnostic.get("fault") != result["control_fault"]:
            raise ContractError("adapter fault provenance disagrees with the invocation")
    if result["limitations"] != [builtin.LIMITATION] or not isinstance(result["reason"], str):
        raise ContractError("bundle lacks the required scope statement")
    if result["execution_state"] not in {"COMPLETED", "INVALID_MODEL", "INVALID_INPUT", "FAILED_NUMERICAL", "FAILED_SYSTEM", "TIMED_OUT", "CANCELLED"}:
        raise ContractError("bundle has no recognized terminal execution state")
    if result.get("execution_state") in {"COMPLETED", "INVALID_MODEL"}:
        actual = evaluation.evaluate(
            _bounded_bytes(directory / "trajectory.csv"), read_json(directory / "diagnostics.json"),
            _bounded_bytes(directory / "reference.csv"), read_json(directory / "criteria.json"),
        )
        if actual != result.get("evaluation"):
            raise ContractError("saved evaluation differs from independent reevaluation")
        if (result["execution_state"] == "INVALID_MODEL") != (actual["conclusion"] == "INVALID_EVIDENCE"):
            raise ContractError("execution state disagrees with output validity")
    elif result["evaluation"] != evaluation.invalid(result["reason"]):
        raise ContractError("failed or cancelled execution cannot carry an agreement conclusion")
    return result
