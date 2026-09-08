# Contributing to Vital Rehearsal

Read [README.md](README.md), [STATUS.md](STATUS.md), the relevant [task](TASKS.md), [architecture](ARCHITECTURE.md) and [experiment contract](EXPERIMENTS.md). Project artifacts are in English. Lucas Santana is the maintainer and decides scope and source integration.

Run `python3 tools/validate_plan.py` after editing the roadmap, tasks, task JSON, status or navigation links. The validator checks structural plan consistency; it does not prove scientific correctness. `plan/tasks.json` is the canonical task ledger; TASKS/ROADMAP and publication exports are generated views. STATUS records narrative evidence and unresolved gates. Historical acceptance is retained in the lineage records.

Choose one bounded task whose prerequisites are accepted. Before implementation, agree the actual base branch/commit, owned files, acceptance evidence, available commands and resource/permission limits. One primary owner handles a coherent change. Preserve other contributors' files and avoid speculative shared infrastructure.

The three foundation tasks are accepted. The [VR-001 benchmark-selection packet](plan/NEXT_WORK.md) remains the original scientific milestone. Current owner authorization also permits the separately mapped [software-control packet](plan/CONTROL_PACKET.md), which does not satisfy physiology or broader historical acceptance. Referenced engines remain candidates; do not install a numerical dependency, acquire a model/data artifact, or start paid experiments without the corresponding task authority and exact dependency/data review.

The local CLI uses CPython 3.12 on Linux with no third-party production dependency. Run `python3 -m unittest discover -s tests -v` for contract, independent evaluation, real worker failure/recovery, packaging and plan falsifiers. Scratch belongs under ignored `runs/` or `.cache/`, never a shared parent or sibling. The development zipapp is built with `python3 tools/package_cli.py`; run it from a fresh project-scoped directory to test packaged behavior. Keep original unsuccessful attempts and the exact matching build.

Report verification may use an existing Chromium and `tools/verify_report.mjs` as optional development tools; Node/Chromium are not production dependencies. Browser output establishes only the observed layout/keyboard behavior. A qualified human's physiology review and an independent researcher's reproduction remain separate evidence.

A contribution should contain a focused change, why it addresses the task, actual checks and failures, reproduction inputs, source/license notices and honest limitations. Unit checks prove local behavior; benchmark agreement and independent scientific interpretation require their own evidence. Never weaken a metric, tolerance, holdout or privacy boundary to make a result pass.

Reject real patient records and identifiers, controlled-access clinical datasets, unsupported parameter ranges and unreviewed intervention recommendations. Synthetic patients are not de-identified patients. No diagnosis, dosing guidance, surgical instructions, pathogen enhancement, infectious sequence design or wet-lab automation. Qualified reviewers must approve the clinical interpretation of a scenario; software tests do not substitute for them.

Use ordinary GitHub changes for code and documentation, and the [Tanduna project](https://tanduna.com/p/vital-rehearsal) for project discussion and task coordination. Submitting a contribution does not authorize automatic merge, release, deployment or real-world action. Do not post sensitive vulnerabilities, personal data or credentials publicly; contact the maintainer through an appropriate private route if needed.

Contributions of original material must be compatible with [AGPL-3.0-only](LICENSE). Keep third-party licensing and attribution intact. Cite research precisely and avoid copying paper text or datasets into the repository without the applicable rights.

## Current v1.0 candidate contributions

Start with [the current contract](docs/v1/CONTRACT.md) and [offline first-run guide](docs/v1/FIRST_RUN.md). Project-local numerical dependencies are authorized by the September 8 owner mandate; old dependency-permission holds are historical. Keep source model code unchanged unless a separately reviewed model revision is explicitly admitted. Preserve every prior experiment and distinguish numerical output from physiological validity.

Concrete needs: a qualified cardio-respiratory modeling reviewer for the pressure-derivative/source-normalization audit; an external researcher to follow the packaged first-run guide; independent evaluator improvements; rights-cleared empirical/model reference evidence; and assistive-technology testing. Do not contact people or post publicly without owner authorization. New failed studies belong in fresh attempt/campaign directories with exact source/build, immutable settings, expected/actual behavior and raw logs.
