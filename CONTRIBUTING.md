# Contributing to Vital Rehearsal

Read [README.md](README.md), [STATUS.md](STATUS.md), the relevant [task](TASKS.md), [architecture](ARCHITECTURE.md) and [experiment contract](EXPERIMENTS.md). Project artifacts are in English. Lucas Santana is the maintainer and decides scope and source integration.

Run python3 tools/validate_plan.py before and after editing the roadmap, tasks, task JSON, status or navigation links. The validator checks structural plan consistency; it does not prove scientific correctness. STATUS.md is the mutable status authority, while TASKS.md and plan/tasks.json are synchronized projections.

Choose one bounded task whose prerequisites are accepted. Before implementation, agree the actual base branch/commit, owned files, acceptance evidence, available commands and resource/permission limits. One primary owner handles a coherent change. Preserve other contributors' files and avoid speculative shared infrastructure.

The next original milestone is the [VR-001 benchmark-selection packet](plan/NEXT_WORK.md), after the three foundation tasks are accepted in dependency order. VR-001 is research and documentation; the later VR-003 task creates the runnable skeleton and documents real setup/test commands. Until then, there is no scientific runtime to install or run. Referenced engines are candidates; do not install dependencies, download model weights or datasets, or start paid experiments without the corresponding task authority and exact dependency/data review.

A contribution should contain a focused change, why it addresses the task, actual checks and failures, reproduction inputs, source/license notices and honest limitations. Unit checks prove local behavior; benchmark agreement and independent scientific interpretation require their own evidence. Never weaken a metric, tolerance, holdout or privacy boundary to make a result pass.

Reject real patient records and identifiers, controlled-access clinical datasets, unsupported parameter ranges and unreviewed intervention recommendations. Synthetic patients are not de-identified patients. No diagnosis, dosing guidance, surgical instructions, pathogen enhancement, infectious sequence design or wet-lab automation. Qualified reviewers must approve the clinical interpretation of a scenario; software tests do not substitute for them.

Use ordinary GitHub changes for code and documentation, and the [Tanduna project](https://tanduna.com/p/vital-rehearsal) for project discussion and task coordination. Submitting a contribution does not authorize automatic merge, release, deployment or real-world action. Do not post sensitive vulnerabilities, personal data or credentials publicly; contact the maintainer through an appropriate private route if needed.

Contributions of original material must be compatible with [AGPL-3.0-only](LICENSE). Keep third-party licensing and attribution intact. Cite research precisely and avoid copying paper text or datasets into the repository without the applicable rights.
