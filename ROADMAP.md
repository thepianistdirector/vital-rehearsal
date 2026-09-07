# Vital Rehearsal roadmap

Wave 0 is **DONE**: its three architecture-foundation tasks were accepted by the authorized root after independent review and reproduced checks. All 24 original scientific/build tasks remain **PLANNED** across Waves 1–8. The programme now contains nine waves and 27 tasks; no scientific result or runtime is claimed.

## Product objective

Help researchers compare medical hypotheses in reproducible virtual experiments using public models, public aggregate evidence and wholly synthetic patients. The ambition includes diseases, immune and vaccine-response research, heart-lung-liver physiology, injury recovery and the organization of care. Each result must say what the model can and cannot establish.

## Research-programme foundation

Wave 0 defines the platform architecture, outcome/dependency roadmap and the executable next-work packet. These are real documentation and plan-tooling deliverables, but they do not implement or validate a simulator. The assigned root reviewer may move VR-F01 through VR-F03 from **READY_FOR_REVIEW** to **DONE** under the maintainer's current instruction after inspecting the changes and recording evidence in [STATUS.md](STATUS.md).

The programme is organized at four levels:

1. **Product contract:** an open, non-clinical research laboratory using lawful public aggregate or wholly synthetic inputs.
2. **Outcome roadmap:** Wave 0 establishes foundations; Waves 1–4 earn the first reproducible and falsifiable cardiopulmonary/care-process experiment; Waves 5–8 extend domains, bounded research agents, scale and independent release evidence.
3. **Milestone contract:** the next original milestone is VR-001, whose selection and acceptance questions are explicit in [plan/NEXT_WORK.md](plan/NEXT_WORK.md).
4. **Work packet:** one bounded owner, exact paths, entry conditions, protected surfaces, acceptance, checks, failure states and handoff.

## First scientific milestone

Select and then reproduce one published, non-patient-specific cardiopulmonary benchmark. Only after its source, rights, units, acceptance basis and applicability pass review should the programme compare baseline and delayed-care workflow scenarios over a small synthetic cohort. Export trajectories, uncertainty and a reproducible experiment report. The initial experiment studies model response and workflow timing; it does not recommend treatment or simulate a surgical technique.

Waves 1–3 establish the first integrated experiment. Wave 4 tests whether its evidence is robust. Later waves expand domains, add agents, improve collaboration and prepare an independently reproduced research preview. Wave order is an integration dependency, not a calendar. The explicit task dependencies are in [TASKS.md](TASKS.md).

## Outcome and dependency logic

| Programme outcome | Required prior evidence | Gate |
| --- | --- | --- |
| Foundation can guide independent sessions | architecture, dependency graph, next packet and automated plan validation | maintainer accepts VR-F01 → VR-F02 → VR-F03 |
| First model can be implemented without inventing science | exact benchmark/context, lawful inputs and dependency/runtime decision | Wave 1 accepted |
| Workflow and physiology can exchange one supported event | each kernel verified separately; time, units and failure behavior tested | Wave 2 accepted |
| First paired synthetic study is inspectable | fixed cohort contract, paired inputs, retained failures and reproducible report | Wave 3 accepted |
| Evidence resists easy self-deception | sensitivity/identifiability, frozen confirmation evidence and invalid-state tests | Wave 4 accepted |
| New scientific domains remain bounded | each disease, immune and hepatic adapter has independent applicability evidence | Wave 5 accepted |
| Agents cannot grade or authorize themselves | grounded proposals, equal budgets and evaluator separation | Wave 6 accepted |
| More users/work does not corrupt evidence | accessible comparison, recovery/idempotency and portable bundles | Wave 7 accepted |
| Research preview claims are independently checked | two reproductions, qualified interpretation/usability review and exact candidate approval | Wave 8 accepted |

Critical path: VR-F01 → VR-F02 → VR-F03 → VR-001 → VR-002 → VR-003, then the existing wave gates. Near-critical constraints are qualified reviewer availability, rights clarity, supported hardware/runtime and access to machine-readable reference outputs. A blocked scientific candidate does not block contract and validator work, but it does block model adoption and every downstream claim that depends on it.

## Capacity and next planning window

Assume one maintainer and one implementation owner per coherent surface. Human reviewer availability, hardware and paid-compute budget are currently unallocated. Plan the next one or two weeks around Waves 1–2 only after measuring the first task's throughput; later tasks are outcome packages to split when prerequisites exist. The conservative dependency graph waits for the previous wave's accepted gate. Within a wave, use disjoint work only when dependencies and shared resources permit it.

Proposed initial experiment ceiling for future approval: one local worker, at most 20 trial runs, at most two elapsed compute hours and 5 GiB of new artifacts per campaign. Agent inference costs count toward an explicitly approved budget. These are draft limits, not permission to start or spend. Reduce the workload if the first benchmark cannot fit. GPU, cloud, domain-review time and additional workers need an explicit allocation before execution.

## Waves and tasks

## Wave 0: Architecture and research-programme foundation

Outcome/gate: Future sessions can start the correct bounded work without guessing, and the plan detects dependency or synchronization drift.

Entry: Clean planning baseline at repository commit 94608775e6f93815688fa3e0e14b7e9332443dc7; documentation and standard-library tooling only.
- **VR-F01: Establish the architecture contract.** Define domain boundaries, model applicability, time/unit/conservation and coupling contracts, provenance and lawful-input controls, producer/evaluator separation, result/failure semantics, reproducibility, local recovery, security boundaries and measured scale triggers without claiming scientific implementation.
- **VR-F02: Establish the outcome and dependency roadmap.** Add Wave 0 and four-level programme logic while preserving all original 24 task IDs, acceptance criteria, wave numbers and dependency edges; identify critical constraints, evidence gates, cut order and replanning triggers.
- **VR-F03: Establish the executable next-work packet and repository-plan validation.** Define a bounded VR-001 packet with explicit public benchmark selection questions and justified acceptance, and provide a dependency/DAG/status/navigation validator that supports maintainer promotion of foundation tasks from READY_FOR_REVIEW to DONE.

Gate decision: the assigned root reviewer inspects the stable foundation diff, runs python3 tools/validate_plan.py, records evidence in [STATUS.md](STATUS.md), and moves VR-F01 through VR-F03 to **DONE** in dependency order under the maintainer's current instruction. Until then they remain **READY_FOR_REVIEW**. Scientific work remains **PLANNED**.

## Wave 1: Evidence and first benchmark

Outcome/gate: A reproducible, lawful and scientifically bounded first experiment is specified.

Entry: Wave 0 accepted; inspect the accepted foundation and [VR-001 packet](plan/NEXT_WORK.md). Only reviewed built-in code and non-protected development fixtures may execute until an OS/container/VM boundary demonstrably enforces filesystem, credential, device, network, subprocess and resource isolation. Untrusted adapters, agent-generated code and protected confirmation artifacts cannot execute or mount before that gate passes.
- **VR-001: Define the benchmark and clinical scope.** Record the exact publication, variables, units, applicable population, numerical tolerances justified by the source, and excluded clinical uses; obtain a qualified review before clinical interpretation.
- **VR-002: Audit model and data rights.** Record release, license, redistribution permission, model limitations and public/synthetic provenance; no restricted or patient-level data enters the fixture.
- **VR-003: Create the local experiment skeleton.** After the exact dependency review, implement CLI validation and a tiny synthetic smoke fixture; malformed units and unknown fields fail with a clear error.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 2: Physiology and workflow kernels

Outcome/gate: Numerical and process models can run separately and exchange a documented event.

Entry: Wave 1 accepted with its evidence recorded.
- **VR-004: Implement the physiology adapter.** Reproduce the fixed reference trajectory within the predeclared tolerance and report solver/version metadata.
- **VR-005: Implement the event-time scheduler.** A hand-computable queue example matches expected waiting times; simultaneous events have a stable ordering.
- **VR-006: Specify and test model coupling.** Prove unit/time conversion, reject unsupported actions and show uncoupled versus coupled traces without hidden state changes.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 3: First virtual cohort

Outcome/gate: A complete baseline-versus-delay experiment produces inspectable artifacts.

Entry: Wave 2 accepted with its evidence recorded.
- **VR-007: Build the synthetic cohort generator.** Generate bounded synthetic parameters with explicit distributions and seeds; no invented representativeness claim.
- **VR-008: Run paired care-delay scenarios.** Use the same cohort and random inputs for both arms; retain all runs including failures and unknown applicability.
- **VR-009: Export the first study report.** A fresh checkout regenerates tables, curves, sources and limitations; every clinical-sounding claim links to its evidence scope.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 4: Uncertainty and falsification

Outcome/gate: The laboratory detects wrong models and fragile rankings.

Entry: Wave 3 accepted with its evidence recorded.
- **VR-010: Add sensitivity and identifiability checks.** Show which parameters affect the result and which cannot be estimated from the selected data.
- **VR-011: Separate calibration and validation.** Freeze a holdout before optimization and detect leakage; report prediction error by supported cohort slice.
- **VR-012: Test numerical and physiological failures.** Representative unit errors, nonconvergence and impossible states cause explicit invalid results rather than favorable scores.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 5: Disease, immunity and organ extensions

Outcome/gate: New scientific domains enter through separately validated adapters.

Entry: Wave 4 accepted with its evidence recorded.
- **VR-013: Reproduce one disease-response model.** Select a publicly reusable model and reproduce its published behavior without asserting therapeutic efficacy.
- **VR-014: Reproduce an immune or vaccine-response model.** Use public aggregate model inputs, predeclared endpoints and a qualified review; retain the no-sequence/no-pathogen-engineering boundary.
- **VR-015: Add liver and trauma-process research scope.** Independently validate a hepatic model and an abstract trauma-workflow case; document why neither establishes a surgical protocol.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 6: Bounded research agents

Outcome/gate: Agents propose traceable experiments inside a fixed scientific contract.

Entry: Wave 5 accepted with its evidence recorded.
- **VR-016: Implement source-grounded hypothesis proposals.** Every hypothesis cites an approved source and declares the measurable prediction and falsifier; unsupported medical claims are rejected.
- **VR-017: Add budgeted experiment selection.** Compare agent proposals with a fixed search baseline using equal evaluation budgets and untouched holdouts.
- **VR-018: Add independent result checking.** A separate evaluator reproduces selected candidates and flags selective reporting or altered metrics.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 7: Research workbench and scale

Outcome/gate: Researchers can compare runs and safely execute bounded batches.

Entry: Wave 6 accepted with its evidence recorded.
- **VR-019: Build the local study comparison view.** Keyboard-accessible baseline/candidate comparison exposes uncertainty, sources, invalid results and simulation-only status.
- **VR-020: Add isolated batch workers.** Cancellation and timeout terminate subprocesses; interrupted studies resume without duplicate terminal results.
- **VR-021: Package portable research bundles.** Another machine can inspect the bundle offline and reproduce a supported benchmark without private credentials.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 8: Independent research release

Outcome/gate: A usable research preview has repeatable evidence and honest limitations.

Entry: Wave 7 accepted with its evidence recorded.
- **VR-022: Replicate two distinct scenarios.** A contributor who did not author the adapter reproduces two cases; discrepancies remain visible.
- **VR-023: Review scientific interpretation and usability.** Qualified reviewers check supported claims and a researcher completes the import-run-compare-export flow.
- **VR-024: Prepare the research preview release.** Publish only after maintainer approval; include evidence, dependency notices, known gaps and an explicit non-clinical-use statement.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.


## Acceptance and release

Numerical benchmarks, source rights, failure behavior and an end-to-end reproduction take precedence over task counts. Scientific extensions need their own applicability evidence; domain reviewer availability is a real dependency. High-risk interpretations require an independent qualified reviewer. A software preview can pass without demonstrating a novel scientific improvement; state the distinction explicitly.

All source and clinical/environmental/privacy/performance claims stay within [EXPERIMENTS.md](EXPERIMENTS.md). A final release needs the exact candidate, clean reproducibility instructions, lawful inputs, resolved material defects and maintainer approval. No production deploy, physical action or unrestricted autonomous execution is included.

## Stop and reduce-scope rules

If the reference curve cannot be reproduced without undocumented tuning, stop optimization and repair the model or narrow the claim. If qualified domain review is unavailable, continue infrastructure and published benchmark reproduction only. Never bridge a gap with LLM-generated physiology.

Stop a campaign when its approved budget is exhausted, the evaluator is compromised, required provenance is missing or the task crosses its safety boundary. Do not keep adding agents to rescue an unsupported hypothesis. Cut rich visuals, distributed compute and additional domains before the initial benchmark. Reforecast after accepted task evidence, not from speculative agent throughput.
