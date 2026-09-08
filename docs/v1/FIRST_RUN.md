# First run: Vital Rehearsal v1.0 release candidate

Status: [public unreviewed rc4 prerelease](https://github.com/thepianistdirector/vital-rehearsal/releases/tag/v1.0.0rc4); independent human first run remains pending. Anonymous public downloads and same-host first-run checks passed; see [receipt](../publication/v1/receipt.json). This package is for bounded computational research. The included respiratory exposure has a demonstrated source pressure-derivative discrepancy. It does not represent any single model in the original paper. No clinical use, patient data, physiological validation or care-to-model coupling is supported.

## Supported environment

Linux x86_64, CPython **3.12**, glibc compatible with the supplied manylinux wheels, 2 GiB available RAM and 1 GiB free disk for the archive, installation, study plots and retained evidence. NumPy 2.2.6 and SciPy 1.15.3 are pinned and supplied. Numerical workers use one BLAS thread, at most 120 CPU seconds and the experiment's wall timeout (default 60 seconds). Each worker has a 2 GiB address-space limit; this is resource containment, not a security sandbox. Browser use is offline; a modern Chromium browser was checked on this same host. Other operating systems, Python versions, browsers and physical machines are unverified. No private account is required.

## Install from the prepared archive

Extract the versioned archive into a new directory and enter that directory. Verify its published SHA256 before using it (approved prerelease; human review remains pending). Then:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --find-links wheels --require-hashes -r requirements-lock.txt
.venv/bin/python vital-rehearsal.pyz --version
.venv/bin/python vital-rehearsal.pyz research models
```

The wheel set is specifically for CPython 3.12 on Linux x86_64. If your interpreter cannot install it, use the supported environment; do not bypass the hashes. From a source checkout, install requirements.txt in a local virtual environment, then run `python tools/package_cli.py` using that environment. The local `vital-rehearsal` script accepts the same commands as the pyz.

## Define an immutable respiratory experiment

```sh
.venv/bin/python vital-rehearsal.pyz research example --output draft.json
```

Inspect the model card first. Edit draft.json only within its supported numerical scope: methods Radau, BDF, RK45, DOP853 or source-vode; time 0..10 seconds; 2..2001 samples; source initial state; lungMechanics R multiplier 0.9..1.1. R perturbations are software sensitivity cases, not a physiological population distribution. Relative/absolute solver tolerances and maximum step are recorded in the experiment. Time is always seconds; state units are in the model card. The unusual E/z source labels are not silently converted. Never add patient fields or medication/care events.

```sh
.venv/bin/python vital-rehearsal.pyz research seal draft.json --output study.json
.venv/bin/python vital-rehearsal.pyz research validate study.json
.venv/bin/python vital-rehearsal.pyz research run study.json --output runs
```

Sealing hashes canonical JSON. Editing a sealed study invalidates it; edit the draft and seal to a **new** file. A seal fixes experiment intent, not source authorship. Each execution retains its exact runner build. The run prints its unique bundle path and execution state. Substitute that path for BUNDLE below:

```sh
.venv/bin/python vital-rehearsal.pyz research inspect BUNDLE
.venv/bin/python vital-rehearsal.pyz research export BUNDLE --output report-bundle.zip
```

Open BUNDLE/report.html directly in your browser. It contains per-observable comparison, unit labels, diagnostic warnings and evidence links. Tab to “Skip to evidence”; expand the experiment and full-results sections. Use the browser's Print action for PDF. CSV files retain numeric trajectories; the JSON files retain complete diagnostics and costs. A successful numerical run is labeled with source warnings; it is never a physiological validity pass.

The fixed reference is another numerical algorithm using the **same source equations**: VODE/BDF at source-generated defaults. It is neither independent empirical data nor proof of agreement with the original article's figures. Cross-algorithm convergence and independent mathematical checks appear in the research packages.

## Synthetic process study

```sh
.venv/bin/python vital-rehearsal.pyz research example --model synthetic-fcfs --output queue-draft.json
.venv/bin/python vital-rehearsal.pyz research seal queue-draft.json --output queue-study.json
.venv/bin/python vital-rehearsal.pyz research run queue-study.json --output runs
```

Edit synthetic job arrival/service seconds, 1..16 servers, and an optional fixed additional service delay before sealing. FCFS sorts jobs by arrival then ASCII ID. Server assignment chooses earliest previous finish time, then server ID; it does not always choose the lowest-numbered currently idle server. No patient records or empirical service estimates are bundled. `synthetic.service_completed.v1` is an output label only and is not passed to the respiratory model.

## Failure and recovery

```sh
.venv/bin/python vital-rehearsal.pyz research list --output runs
.venv/bin/python vital-rehearsal.pyz research recover BUNDLE --output recovered-runs
```

A timeout, solver failure or graceful interruption retains a failure bundle and stderr. A hard-killed coordinator can leave an unfinalized directory; list labels it `INTERRUPTED_UNFINALIZED`. Its worker has a separate finite alarm/CPU cap. Preserve that directory. Recovery executes its sealed study as a **new** attempt and never overwrites the original. It does not resume from an intermediate state or declare partial output valid. If the timeout was too small, preserve the failed study and create a separately sealed study with a larger supported timeout.

`inspect` rejects changed/missing/extra artifacts and non-regular files. A manifest is a change detector, not a signature; someone able to replace both files and manifest can forge it. Trusted built-ins only; candidate/evaluator artifact separation is a workflow convention on this shared-user host. No hostile isolation is claimed.

Missing NumPy/SciPy: reinstall from the supplied wheel set in your venv. Existing output file: choose a new filename; sealing/export/package creation refuse overwrite. Unsupported/duplicate JSON fields, nonfinite numbers, wrong units and out-of-range parameters: correct the draft and reseal. Numerical failure: inspect stderr and settings, retain the attempt, and compare a justified alternative solver within the supported domain. Do not repair source equations or suppress unsuccessful runs to obtain a preferred answer.

## Reproduce the three studies

To install the included plotting dependencies offline as well, run `.venv/bin/python -m pip install --no-index --find-links wheels --require-hashes -r research-requirements-lock.txt`. This pins Matplotlib 3.10.3 and all its dependencies. The research manuscripts give commands for fresh campaign directories; the frozen investigation archive remains under dist/ so their defaults work from this package layout. Historical absolute paths in the original command logs are provenance, not paths that a new installation must reproduce.

## Reproduce a retained experiment exactly

Every bundle includes `source.pyz`, the full matching original-source application archive and model/license notice. With the pinned dependencies installed:

```sh
.venv/bin/python BUNDLE/source.pyz research run BUNDLE/study.json --output independent-rerun
```

This runs a second process. It becomes independent human or physical-machine reproduction only when such a person or machine actually performs it. Studies in research/ include frozen protocols and rerun instructions; reports state which code, equations, checks and personnel are independent.
