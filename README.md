# Vital Rehearsal

**An open simulation laboratory for physiology, disease research and safer care workflows.**

Help researchers compare medical hypotheses in reproducible virtual experiments using public models, public aggregate evidence and wholly synthetic patients. The ambition includes diseases, immune and vaccine-response research, heart-lung-liver physiology, injury recovery and the organization of care. Each result must say what the model can and cannot establish.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Tanduna project](https://tanduna.com/p/vital-rehearsal) · [Public repository](https://github.com/thepianistdirector/vital-rehearsal)

> **Starting from zero.** This repository currently contains project design, architecture and a contributor plan. No simulator, application, autonomous research system or benchmark result has been implemented here. All 24 build tasks are planned. Proposed capabilities below describe what we want to build.

## Who this is for

Computational physiology researchers, biomedical engineers, clinical simulation educators and open-science contributors working with qualified domain reviewers.

## First useful experiment

Reproduce one published, non-patient-specific cardiopulmonary benchmark, then compare baseline and delayed-care workflow scenarios over a small synthetic cohort. Export trajectories, uncertainty and a reproducible experiment report. The initial experiment studies model response and workflow timing; it does not recommend treatment or simulate a surgical technique.

Software experiments make it possible to compare ideas repeatedly, inspect failures and share reproducible evidence without operating physical systems. They remain bounded by the quality and applicability of their models. A convincing visualization or agent report is not independent validation.

## What we want to build

### Physiology workbench

Heart, lungs and liver represented by separate model cards and declared coupling interfaces; begin with a published cardiopulmonary model. Add hepatic perfusion/metabolism only after its own validation.

### Therapeutic hypothesis library

Reproduce publicly documented disease and drug-response models; retain negative findings and distinguish association, model prediction and experimental evidence.

### Immune and vaccine research

Compare public, aggregate immune-response and population-benefit models. Begin with published model reproduction; exclude sequence generation, pathogen engineering and actionable wet-lab designs.

### Care-process rehearsal

Discrete-event models of triage queues, staffing, transport, imaging and operating-room availability. Later trauma scenarios may include a synthetic liver injury as an abstract injury state; no weapon mechanics or procedural treatment instructions.

### Virtual anatomy research

A later, separately validated tissue/organ-mechanics adapter for educational visualization and computational investigation; no claim of patient-specific operative planning.

## Architecture in one paragraph

A Python experiment coordinator runs a C++ physiology engine through a narrow process adapter and a separate discrete-event workflow model. Use explicit units and interface contracts for time, physiological variables and workflow events. A workflow delay may change only a supported scenario input; never imply that an aggregate physiology engine resolves tissue geometry, infection biology or surgical maneuvers. Keep organ, immune, epidemiological and tissue models separate until a coupling validation demonstrates that time scales and state variables are compatible. Start with CLI reports; a local browser workbench comes after the numerical benchmark passes.

Agents propose and interpret experiments; numerical engines and protected evaluators determine results. Every experiment retains its inputs, assumptions, source version, environment, resource budget and failure state.

## Build plan

| Wave | Outcome | Gate |
| --- | --- | --- |
| 1 | Evidence and first benchmark | A reproducible, lawful and scientifically bounded first experiment is specified. |
| 2 | Physiology and workflow kernels | Numerical and process models can run separately and exchange a documented event. |
| 3 | First virtual cohort | A complete baseline-versus-delay experiment produces inspectable artifacts. |
| 4 | Uncertainty and falsification | The laboratory detects wrong models and fragile rankings. |
| 5 | Disease, immunity and organ extensions | New scientific domains enter through separately validated adapters. |
| 6 | Bounded research agents | Agents propose traceable experiments inside a fixed scientific contract. |
| 7 | Research workbench and scale | Researchers can compare runs and safely execute bounded batches. |
| 8 | Independent research release | A usable research preview has repeatable evidence and honest limitations. |

Read the [roadmap](ROADMAP.md), [24 contributor tasks](TASKS.md), [architecture](ARCHITECTURE.md), [experiment and evaluation contract](EXPERIMENTS.md), [sources and data policy](SOURCES.md) and [current state](STATUS.md). All waves are future work; a plan is not execution authorization.

## Scientific and operating boundaries

Reject real patient records and identifiers, controlled-access clinical datasets, unsupported parameter ranges and unreviewed intervention recommendations. Synthetic patients are not de-identified patients. No diagnosis, dosing guidance, surgical instructions, pathogen enhancement, infectious sequence design or wet-lab automation. Qualified reviewers must approve the clinical interpretation of a scenario; software tests do not substitute for them.

If the reference curve cannot be reproduced without undocumented tuning, stop optimization and repair the model or narrow the claim. If qualified domain review is unavailable, continue infrastructure and published benchmark reproduction only. Never bridge a gap with LLM-generated physiology.

## Contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). The next eligible work is the first benchmark/contract task. Implementation follows review of exact dependency choices and a maintainer-accepted bounded task. There are no install or runtime commands yet; do not interpret proposed paths or commands as an existing application.

## Related independent projects

- [Grid Horizons](https://github.com/thepianistdirector/grid-horizons): Simulate better grids, transformers and energy systems before proposing physical changes.
- [Earth Rehearsal](https://github.com/thepianistdirector/earth-rehearsal): A software laboratory for cleaner water, less pollution and testable climate interventions.
- [Civic Safelab](https://github.com/thepianistdirector/civic-safelab): Test public-safety sensing in synthetic worlds while measuring privacy and false alarms.
- [Lean Model Lab](https://github.com/thepianistdirector/lean-model-lab): Find reproducible training and inference efficiency gains without hiding quality tradeoffs.
- [Research Continuum](https://github.com/thepianistdirector/research-continuum): A reproducible autonomous research system that turns hypotheses into independently checked experiments.

These repositories are independently buildable. Shared experiment formats are a design intention; there is no shared service or integration implemented today. Extract a common library only after two real implementations demonstrate the need.

## License

Original repository content is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE). Third-party data, models, papers and code retain their own terms and are not relicensed by this repository. No third-party dataset, model weights or upstream implementation is bundled in this initial planning release.
