# Vital Rehearsal contributor tasks

The three Wave 0 foundation tasks are **DONE**; the original 24 tasks remain **PLANNED**. [STATUS.md](STATUS.md) is the mutable progress authority. This file is the human-readable task contract and [plan/tasks.json](plan/tasks.json) is its synchronized machine-readable projection. Update both together when task scope, dependencies or status changes. Tanduna publication/review and task execution are separate operations.

Before an implementation task starts, bind it to an actual repository branch/commit, inspect existing paths and dependencies, identify one primary owner and record the exact verification commands available in that checkout. Proposed directory names below are ownership boundaries to establish, not claims of existing modules. Later outcome packages may need decomposition at their wave gate; do not treat all 24 as one autonomous job.

Protected across every task: evaluator/holdouts outside the task's authority, accepted evidence, unrelated source, credentials, data rights, domain safety rules and resource ceilings. No production deploy, physical system connection, external outreach or paid compute is authorized by a task description. Do not commit, push or publish unless the specific contribution task authorizes it. The maintainer reviews source contributions and scientific claims separately.

Foundation status may move from **READY_FOR_REVIEW** to **DONE** after acceptance by the assigned root reviewer under the maintainer's current instruction and matching evidence in [STATUS.md](STATUS.md). Later original tasks use the evidence-bounded statuses defined by the active plan; a status change never weakens acceptance or bypasses a dependency.
## VR-F01 — Establish the architecture contract

- Wave: 0; status: **DONE**; owner: architecture foundation contributor; accepted by the assigned root on 2026-09-07.
- Dependencies: none.
- Owned scope: ARCHITECTURE.md, SOURCES.md.
- Acceptance: Define domain boundaries, model applicability, time/unit/conservation and coupling contracts, provenance and lawful-input controls, producer/evaluator separation, result/failure semantics, reproducibility, local recovery, security boundaries and measured scale triggers without claiming scientific implementation.
- Verification: inspect the complete architecture against the source ledger and run the repository plan validator. A qualified domain reviewer remains required before future clinical or biological interpretation, not for accepting this architecture-documentation task.
- Evidence: the assigned root reviewed the project-specific architecture and source boundaries; acceptance and reproduced checks are recorded in STATUS.md.

## VR-F02 — Establish the outcome and dependency roadmap

- Wave: 0; status: **DONE**; owner: architecture foundation contributor; accepted by the assigned root on 2026-09-07.
- Dependencies: VR-F01.
- Owned scope: ROADMAP.md, TASKS.md, plan/tasks.json, STATUS.md.
- Acceptance: Add Wave 0 and four-level programme logic while preserving all original 24 task IDs, acceptance criteria, wave numbers and dependency edges; identify critical constraints, evidence gates, cut order and replanning triggers.
- Verification: compare the foundation diff with baseline 94608775e6f93815688fa3e0e14b7e9332443dc7 and run the repository plan validator.
- Evidence: Wave 0, outcome gates and critical constraints are recorded; original plan preservation and assigned root acceptance remain review gates.

## VR-F03 — Establish the executable next-work packet and repository-plan validation

- Wave: 0; status: **DONE**; owner: architecture foundation contributor; accepted by the assigned root on 2026-09-07.
- Dependencies: VR-F02.
- Owned scope: plan/NEXT_WORK.md, tools/validate_plan.py, README.md, CONTRIBUTING.md.
- Acceptance: Define a bounded VR-001 packet with explicit public benchmark selection questions and justified acceptance, and provide a dependency/DAG/status/navigation validator that supports maintainer promotion of foundation tasks from READY_FOR_REVIEW to DONE.
- Verification: run python3 tools/validate_plan.py from the repository root and confirm both success and a representative invalid-plan failure using an isolated temporary copy.
- Evidence: the next-work packet and validator are present; observed command results belong in STATUS.md before maintainer acceptance.

## VR-001 — Define the benchmark and clinical scope

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-F03.
- Owned scope: `docs/benchmarks/`.
- Acceptance: Record the exact publication, variables, units, applicable population, numerical tolerances justified by the source, and excluded clinical uses; obtain a qualified review before clinical interpretation.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-002 — Audit model and data rights

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-001.
- Owned scope: `docs/data/`.
- Acceptance: Record release, license, redistribution permission, model limitations and public/synthetic provenance; no restricted or patient-level data enters the fixture.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-003 — Create the local experiment skeleton

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-001, VR-002.
- Owned scope: `src/`, `tests/`, `scenarios/`.
- Acceptance: After the exact dependency review, implement CLI validation and a tiny synthetic smoke fixture; malformed units and unknown fields fail with a clear error.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-004 — Implement the physiology adapter

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-001, VR-002, VR-003.
- Owned scope: `adapters/physiology/`.
- Acceptance: Reproduce the fixed reference trajectory within the predeclared tolerance and report solver/version metadata.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-005 — Implement the event-time scheduler

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-001, VR-002, VR-003.
- Owned scope: `src/workflows/`.
- Acceptance: A hand-computable queue example matches expected waiting times; simultaneous events have a stable ordering.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-006 — Specify and test model coupling

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-001, VR-002, VR-003.
- Owned scope: `src/coupling/`.
- Acceptance: Prove unit/time conversion, reject unsupported actions and show uncoupled versus coupled traces without hidden state changes.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-007 — Build the synthetic cohort generator

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-004, VR-005, VR-006.
- Owned scope: `src/cohorts/`.
- Acceptance: Generate bounded synthetic parameters with explicit distributions and seeds; no invented representativeness claim.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-008 — Run paired care-delay scenarios

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-004, VR-005, VR-006, VR-007.
- Owned scope: `scenarios/cardiopulmonary/`.
- Acceptance: Use the same cohort and random inputs for both arms; retain all runs including failures and unknown applicability.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-009 — Export the first study report

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-004, VR-005, VR-006, VR-008.
- Owned scope: `src/reports/`.
- Acceptance: A fresh checkout regenerates tables, curves, sources and limitations; every clinical-sounding claim links to its evidence scope.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-010 — Add sensitivity and identifiability checks

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-007, VR-008, VR-009.
- Owned scope: `src/analysis/`.
- Acceptance: Show which parameters affect the result and which cannot be estimated from the selected data.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-011 — Separate calibration and validation

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-007, VR-008, VR-009.
- Owned scope: `benchmarks/`.
- Acceptance: Freeze a holdout before optimization and detect leakage; report prediction error by supported cohort slice.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-012 — Test numerical and physiological failures

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-007, VR-008, VR-009.
- Owned scope: `tests/validation/`.
- Acceptance: Representative unit errors, nonconvergence and impossible states cause explicit invalid results rather than favorable scores.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-013 — Reproduce one disease-response model

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-010, VR-011, VR-012.
- Owned scope: `adapters/disease/`.
- Acceptance: Select a publicly reusable model and reproduce its published behavior without asserting therapeutic efficacy.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-014 — Reproduce an immune or vaccine-response model

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-010, VR-011, VR-012.
- Owned scope: `adapters/immunity/`.
- Acceptance: Use public aggregate model inputs, predeclared endpoints and a qualified review; retain the no-sequence/no-pathogen-engineering boundary.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-015 — Add liver and trauma-process research scope

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-010, VR-011, VR-012.
- Owned scope: `adapters/hepatic/`, `scenarios/care-process/`.
- Acceptance: Independently validate a hepatic model and an abstract trauma-workflow case; document why neither establishes a surgical protocol.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-016 — Implement source-grounded hypothesis proposals

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-013, VR-014, VR-015.
- Owned scope: `src/agents/`.
- Acceptance: Every hypothesis cites an approved source and declares the measurable prediction and falsifier; unsupported medical claims are rejected.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-017 — Add budgeted experiment selection

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-013, VR-014, VR-015.
- Owned scope: `src/search/`.
- Acceptance: Compare agent proposals with a fixed search baseline using equal evaluation budgets and untouched holdouts.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-018 — Add independent result checking

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-013, VR-014, VR-015.
- Owned scope: `src/evaluation/`.
- Acceptance: A separate evaluator reproduces selected candidates and flags selective reporting or altered metrics.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-019 — Build the local study comparison view

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-016, VR-017, VR-018.
- Owned scope: `apps/workbench/`.
- Acceptance: Keyboard-accessible baseline/candidate comparison exposes uncertainty, sources, invalid results and simulation-only status.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-020 — Add isolated batch workers

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-016, VR-017, VR-018.
- Owned scope: `src/workers/`.
- Acceptance: Cancellation and timeout terminate subprocesses; interrupted studies resume without duplicate terminal results.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-021 — Package portable research bundles

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-016, VR-017, VR-018.
- Owned scope: `src/export/`.
- Acceptance: Another machine can inspect the bundle offline and reproduce a supported benchmark without private credentials.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-022 — Replicate two distinct scenarios

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-019, VR-020, VR-021.
- Owned scope: `benchmarks/replication/`.
- Acceptance: A contributor who did not author the adapter reproduces two cases; discrepancies remain visible.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-023 — Review scientific interpretation and usability

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-019, VR-020, VR-021.
- Owned scope: `docs/review/`.
- Acceptance: Qualified reviewers check supported claims and a researcher completes the import-run-compare-export flow.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## VR-024 — Prepare the research preview release

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: VR-019, VR-020, VR-021.
- Owned scope: `docs/releases/`.
- Acceptance: Publish only after maintainer approval; include evidence, dependency notices, known gaps and an explicit non-clinical-use statement.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
