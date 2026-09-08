"""Local CLI; packaged reviewed built-ins are the only execution registry."""

import argparse
import json
from pathlib import Path
import signal
import sys

from . import __version__, builtin
from .contracts import ContractError, canonical_json, digest, read_json, study_identity, validate_study


def _print(value):
    print(json.dumps(value, sort_keys=True, indent=2, allow_nan=False))


def _terminated(_signal, _frame):
    raise KeyboardInterrupt


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "research":
        from .research import main as research_main
        return research_main(argv[1:])
    if argv and argv[0] == "_worker":
        if len(argv) != 3 or sys.platform != "linux":
            return 2
        from .worker import execute
        try:
            return execute(Path(argv[1]), argv[2])
        except Exception as exc:
            print(f"Built-in control failed ({type(exc).__name__})", file=sys.stderr)
            return 7
    parser = argparse.ArgumentParser(
        prog="vital-rehearsal",
        description="Evidence tooling. Use research for the admitted source-model and synthetic scheduling workflow; legacy commands below are software controls.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("models", help="show admitted built-ins and scope limits")
    example = commands.add_parser("example", help="write the fixed software-control study")
    example.add_argument("--output", type=Path, required=True)
    validate = commands.add_parser("validate", help="validate a fixed study without execution")
    validate.add_argument("study", type=Path)
    run = commands.add_parser("run", help="execute a fixed software-control study and retain evidence")
    run.add_argument("study", type=Path)
    run.add_argument("--output", type=Path, required=True, help="local attempt-store directory")
    run.add_argument("--control-fault", default="none", choices=(
        "none", "perturbed", "wrong-unit", "truncated", "nonfinite", "impossible",
        "nonconvergence", "crash", "pause",
    ), help="explicit software fault injection; retained and labeled in the bundle")
    inspect = commands.add_parser("inspect", help="verify bundle integrity and independently recheck comparisons")
    inspect.add_argument("bundle", type=Path)
    listing = commands.add_parser("list-attempts", help="list complete, failed and interrupted attempts")
    listing.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "models":
            from .research_model import card
            _print({"physiology_models": [card()], "software_controls": [builtin.model_card()], "research_entrypoint": "vital-rehearsal research --help"})
        elif args.command == "example":
            with args.output.open("xb") as stream:
                stream.write(canonical_json(builtin.study()))
            _print({"state": "WRITTEN", "scope": "SOFTWARE_CONTROL_NOT_PHYSIOLOGY"})
        elif args.command == "validate":
            spec = validate_study(read_json(args.study))
            _print({"state": "VALID_CONTROL_STUDY", "study_identity": study_identity(spec), "study_sha256": digest(canonical_json(spec)), "limitation": builtin.LIMITATION})
        elif args.command == "run":
            from .attempts import run as execute_run
            previous = signal.signal(signal.SIGTERM, _terminated)
            try:
                directory, result = execute_run(
                    read_json(args.study), args.output, args.control_fault,
                )
            finally:
                signal.signal(signal.SIGTERM, previous)
            _print({
                "attempt_id": result["attempt_id"], "bundle": str(directory),
                "execution_state": result["execution_state"],
                "conclusion": result["evaluation"]["conclusion"], "limitation": builtin.LIMITATION,
            })
            if result["execution_state"] == "CANCELLED":
                return 130
            return 0 if result["evaluation"]["conclusion"] == "CONTROL_AGREEMENT" else 1
        elif args.command == "inspect":
            from .attempts import verify_bundle
            _print({"integrity": "VERIFIED", "authenticity": "NOT ESTABLISHED", "result": verify_bundle(args.bundle)})
        elif args.command == "list-attempts":
            from .attempts import list_attempts
            _print({"attempts": list_attempts(args.output)})
    except ContractError as exc:
        _print({"state": "REJECTED", "reason": str(exc)})
        return 2
    except (OSError, ValueError, TypeError, KeyError) as exc:
        _print({"state": "FAILED_SYSTEM", "reason": f"Local operation failed ({type(exc).__name__})"})
        return 3
    return 0
