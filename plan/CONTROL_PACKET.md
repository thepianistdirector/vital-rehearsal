# Independent control and evidence-retention packet

Owner: primary Vital Rehearsal task. Base: `9fa99f392c93f6f1e33a2cd85b9348cb68afe39e`. Status: IN PROGRESS. Scope derives from the current owner launch; this packet does not complete or rewrite VR-001–VR-004.

Owned production paths: `src/vital_rehearsal/`, `vital-rehearsal`, `scenarios/contract-control.json`, `tools/package_cli.py`. Owned checks: `tests/test_contracts.py`, `tests/test_evaluation.py`, `tests/test_attempts.py`, `tests/test_cli.py`. Documentation: `docs/decisions/0001-launch-and-control-slice.md`, `docs/evidence/`, README, STATUS, CONTRIBUTING and additive architecture/experiment/source updates. Independent leaves own the plan and benchmark documents.

Outcome: a researcher/developer can validate a sealed control study, execute a trusted built-in identity control, inspect complete raw output and honest per-observable evaluation, detect tampering, and preserve prior evidence through failure or interruption. The command must clearly state that no physiology model is admitted.

Falsifiers: malformed/duplicate/unknown JSON; Boolean or nonfinite numeric input; invalid units; changed conditions; adapter injection; missing/reordered/nonfinite/perturbed trajectory cells; mismatched diagnostics; timeout/crash; interrupted staging; changed manifest bytes; identical-spec reruns overwriting previous evidence. A fixed control is software verification only, never a substitute for a source-defined benchmark.

Entry: inspected ownership, explicit local authorization, accepted standard-library architecture, no new production dependency. Broad model implementation waits for benchmark admission and the expanded coherent roadmap. Exit: nonzero discovered tests exercise important failures; the packaged CLI completes the same control workflow from a clean project-scoped extraction; documentation records precise limitations and pending gates.

Planned commands become evidence only when they run: `python3 -m unittest discover -s tests -v`; `python3 tools/validate_plan.py`; `./vital-rehearsal validate scenarios/contract-control.json`; `./vital-rehearsal run scenarios/contract-control.json --output runs/control`; `python3 tools/package_cli.py`; packaged validate/run/inspect plus interrupted-run recovery. All temporary artifacts stay under this repository's ignored runs/cache directories.
