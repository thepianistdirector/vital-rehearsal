# Vital Rehearsal

A bounded physiology and synthetic care-process research workbench. Inspect a public source model, seal an experiment, run its numerical equations, compare outputs, and export reproducible evidence.

Maintained by Lucas Santana ([thepianistdirector](https://github.com/thepianistdirector)). [Repository](https://github.com/thepianistdirector/vital-rehearsal) · [Tanduna project](https://tanduna.com/projects/vital-rehearsal).

**v1.0 prerelease candidate — publication approved; human review pending.** The admitted Ben-Tal 2006 CellML combination exposure is licensed for reuse and executable, with a documented source pressure-derivative inconsistency. It does not equal any single model from the original paper. Results are numerical reproduction and engineering evidence, not physiological validation, clinical advice or patient outcomes. Synthetic scheduling runs independently; no scientific event mapping currently supports coupling it to this model.

## Start a study

Supported: Linux x86_64, CPython 3.12, NumPy 2.2.6, SciPy 1.15.3. The prepared release archive contains offline dependency wheels, the executable and source. See the [external first-run guide](docs/v1/FIRST_RUN.md) for installation, supported resources, report navigation, export and recovery.

From this checkout:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python vital-rehearsal research models
.venv/bin/python vital-rehearsal research example --output draft.json
# Inspect the card and edit supported experiment settings before sealing.
.venv/bin/python vital-rehearsal research seal draft.json --output study.json
.venv/bin/python vital-rehearsal research run study.json --output runs/research
```

The run prints a bundle path. Open its report.html offline, inspect its CSV/JSON and source, then verify/export it:

```sh
.venv/bin/python vital-rehearsal research inspect BUNDLE
.venv/bin/python vital-rehearsal research export BUNDLE --output evidence.zip
```

Use `research example --model synthetic-fcfs` for synthetic scheduling. `research list` includes failed and unfinalized attempts; `research recover` reruns into a new attempt and preserves the original. Every run retains its exact source archive and immutable study. Hashes detect changes, not authorship or scientific validity.

## Evidence and limits

- [Exact model admission and rights](docs/benchmarks/bental-2006/ADMISSION.md), [v1.0 contract](docs/v1/CONTRACT.md), [current state](STATUS.md).
- Three finite investigations: [source reproduction](research/reproduction/), [solver/parameter robustness](research/robustness/), [synthetic scheduling](research/scheduling/). Drafts require skeptical reproduction and qualified review before any physiological interpretation.
- [Release materials](docs/v1/), [canonical task ledger](plan/tasks.json), [roadmap](ROADMAP.md).

The comparator uses the same model equations with a different numerical algorithm; no independent empirical reference data was obtained. Source-default R±10% cases are a numerical sensitivity neighbourhood, not a patient population or calibrated uncertainty distribution. The model's derivative inconsistency is preserved, measured and visible. Whole-body engines, arbitrary models, validated clinical coupling and broad platform support are longer-term work.

The original exact-integer software control remains available under `models`, `example`, `validate`, `run`, `inspect` and `list-attempts`. It is software verification only. Its [historical documentation](docs/lineage/2026-09-08-pre-v1/README.md) and evidence remain preserved.

## Development and contribution

```sh
.venv/bin/python -m unittest discover -s tests -v
python3 tools/validate_plan.py
.venv/bin/python tools/package_cli.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Useful contributions include qualified review of source semantics, independent first-run reproduction on the supported environment, rights-cleared reference datasets, numerical evaluator checks and accessibility testing. Report exact source/build, sealed study, expected/actual behavior and complete failed evidence; never send patient records.

Application code is [AGPL-3.0](LICENSE). The attributed Ben-Tal CellML model and generated Python retain **CC BY 3.0**, separately documented in [BENTAL_NOTICE.txt](src/vital_rehearsal/BENTAL_NOTICE.txt). NumPy/SciPy and bundled native-library notices accompany dependency wheels. The owner has approved publishing 1.0.0rc4 as an explicitly unreviewed prerelease, these research drafts and the prepared plan. Human-qualified review, external human reproduction and final v1.0 acceptance remain pending. Paper submission and participant outreach are not authorized.
