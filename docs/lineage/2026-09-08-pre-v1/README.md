# Vital Rehearsal

**An open simulation laboratory for physiology, disease research and safer care-process experiments.**

Vital Rehearsal aims to let researchers assemble lawful public models and wholly synthetic scenarios into reproducible virtual studies. The long-term platform spans heart, lung and liver physiology; disease and immune-response models; aggregate vaccine research; synthetic cohorts; and simulations of queues, staffing, transport and resource availability. Every result must expose its model, assumptions, provenance, uncertainty, failures and limits.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Tanduna project](https://tanduna.com/p/vital-rehearsal) · [Public repository](https://github.com/thepianistdirector/vital-rehearsal)

> **Local development build — physiology admission pending.** A dependency-free Python CLI now validates a fixed software-control study, executes a trusted built-in control, independently evaluates its output, and retains JSON/CSV/HTML evidence through failures and interruption. This is infrastructure evidence, **not a physiology benchmark or the public 0.1 release**. The three foundation tasks remain **DONE**; the original 24 broader contracts remain **PLANNED**. Current evidence and remaining gates are in [STATUS.md](STATUS.md).

## Try the local software control

Verified development environment: CPython 3.12 on Linux, using the standard library. No physiology engine, numerical dependency or patient input is installed. From this source checkout:

```sh
./vital-rehearsal models
./vital-rehearsal validate scenarios/contract-control.json
./vital-rehearsal run scenarios/contract-control.json --output runs/control
./vital-rehearsal list-attempts --output runs/control
```

The run prints its unique bundle path. Open that directory's `report.html` offline, or run `./vital-rehearsal inspect BUNDLE_DIRECTORY` to verify byte integrity, source/build identity and the independent comparison. Keep the matching runner build with its bundles. Integrity does not establish authenticity or scientific validity.

The control is the exact integer identity `counter(t) = t` at seconds 0 through 4. It is **not physiological simulation**. Its exact equality rule must never be reused as a physiology tolerance. The fixed study accepts no parameter variation, patient fields, external adapter paths or user-selected evaluation threshold. Inputs whose decimal meaning would be lost during parsing are rejected.

Exercise a retained negative result:

```sh
./vital-rehearsal run scenarios/contract-control.json --output runs/control --control-fault perturbed
```

That command returns nonzero and records `COMPLETED` execution with a `CONTRADICTED` comparison. Other explicit control faults cover wrong units, truncated/nonfinite/impossible output, injected nonconvergence, process failure and timeout. They are test cases, not model variations or physiological findings.

Every rerun creates a new attempt. Graceful interruption preserves a cancelled bundle; a hard interruption leaves a `.partial` directory that listing identifies separately. Preserve that directory and rerun the same study into the same attempt store. The last complete bundle remains unchanged. Rejected study input is not retained because it might contain out-of-scope private text; the CLI returns a sanitized rejection before creating an attempt.

To make a complete portable development executable without adding a build dependency:

```sh
python3 tools/package_cli.py
python3 dist/vital-rehearsal-0.1.0.dev1.pyz example --output runs/study.json
python3 dist/vital-rehearsal-0.1.0.dev1.pyz run runs/study.json --output runs/packaged
```

The packaging command refuses to overwrite a different build at the same path; supply a new project-local output filename after changing code. This is an unreleased software-control package. The actual 0.1 still needs admitted physiology, source-grounded reference comparison, qualified review, independent researcher reproduction, authorized public distribution and native Tanduna publication.

## The endgame

A researcher should eventually be able to:

1. choose an admitted public model and inspect exactly where it applies;
2. define a versioned experiment with explicit units, time semantics, conservation rules, comparators, uncertainty and a falsifier;
3. run isolated physiology and care-process models, then couple only the variables and events supported by both;
4. compare baseline and candidate studies over paired synthetic inputs without hiding failed or unfavorable runs;
5. reproduce a retained result on another supported machine;
6. distinguish source fact, model assumption, numerical result and qualified human interpretation;
7. let bounded agents propose experiments without giving them control of evaluators, confirmation evidence, budgets or publication.

The platform can grow into multi-organ and multi-model research, but each domain earns its claims independently. A heart-lung benchmark does not validate hepatic metabolism, immune dynamics, tissue geometry or a care policy. Aggregate vaccination data does not represent an individual's immune response. A reproducible simulation is still a model, not clinical evidence.

## The first research programme

The first original milestone is [VR-001: select and specify one public cardiopulmonary benchmark](plan/NEXT_WORK.md). It compares two candidate routes:

- a versioned Pulse validation case with inspectable inputs, outputs, limitations and reference evidence;
- a published CellML/SED-ML cardiopulmonary model with executable files, explicit units, reproducible outputs and clear rights.

The milestone does not choose a winner in advance. It records the question, context of use, applicable population or reference subject, source observables, units, solver settings, excluded uses and acceptance criteria justified from the selected source and numerical analysis. If neither candidate meets the gate, the result is a documented hold or a narrower benchmark.

After that selection and rights review, the first integrated programme is:

~~~mermaid
flowchart LR
  B[Reproduce public heart-lung benchmark] --> S[Verify deterministic care scheduler]
  S --> C[Pass one typed delay event at a supported communication point]
  C --> P[Run paired synthetic baseline and delay scenarios]
  P --> U[Quantify uncertainty and invalid runs]
  U --> R[Generate a reproducible, limitation-first report]
~~~

This experiment studies model response and workflow timing. It does not recommend treatment, dosage, triage policy or a surgical technique.

## Architecture

A local Python coordinator will validate immutable experiment specifications, enforce budgets and run reviewed numerical adapters as separate subprocesses. A physiology engine owns engine-specific state advancement; a separate discrete-event scheduler owns synthetic queues and resources. A typed coupling controller is the only bridge. It validates communication time, quantity semantics, UCUM units, applicability and conservation before accepting an exchanged state or event.

Results are atomically published bundles with inputs, source/model cards, solver and hardware settings, seeds, raw outputs, diagnostics, conservation residuals, uncertainty and explicit terminal states. Negative and inconclusive outcomes remain results. Nonconvergence, invalid units, unsupported actions and broken conservation are invalid evidence, never favorable scores.

The first implementation stays local and modular: standard-library coordination, JSON contracts, CSV trajectories and filesystem bundles. SQLite, array formats, process pools, GPUs, remote workers, object storage and browser UI each have explicit measured scale triggers. The project does not begin with microservices or speculative infrastructure.

A subprocess and scrubbed environment do not enforce a sandbox. Until OS/container/VM controls prove filesystem, credential, device, network, subprocess and resource isolation, only reviewed built-in adapters and non-protected development fixtures may execute. Untrusted adapters, generated code and protected confirmation artifacts remain blocked.

Read the full [architecture](ARCHITECTURE.md), [experiment contract](EXPERIMENTS.md) and [source/adoption ledger](SOURCES.md).

## Research domains

### Heart and lung

Start with a published lumped cardiopulmonary benchmark, fixed reference inputs and source-defined observables. Heart hemodynamics, cardiac electrophysiology, gas exchange and tissue mechanics remain distinct model classes with distinct evidence.

### Liver

Add hepatic perfusion, metabolism or injury models only through a separately benchmarked adapter. A low-resolution organ compartment cannot support tissue, metabolism or surgical claims it was not designed to answer.

### Disease and therapeutic hypotheses

Reproduce public mechanistic models and retain negative findings. Bioactivity records may support provenance; they do not establish efficacy, dose or clinical benefit.

### Immunity and vaccine research

Keep within-host immune dynamics, aggregate population coverage/transmission and care-capacity questions separate. Use only public aggregate or wholly synthetic inputs. Exclude sequence generation, pathogen engineering, mutation optimization and wet-lab instructions.

### Care-process rehearsal

Model abstract arrivals, queues, service, transport and resources with discrete events and synthetic entities. Report inputs, event ordering, replications, uncertainty and limitations. A care simulation may compare declared scenarios; it cannot prescribe a real workflow.

## Programme map

| Wave | Outcome | Current state |
| --- | --- | --- |
| 0 | Architecture and research-programme foundation | 3 tasks **DONE** |
| 1 | Evidence and first benchmark | 3 tasks **PLANNED** |
| 2 | Physiology and workflow kernels | 3 tasks **PLANNED** |
| 3 | First virtual cohort | 3 tasks **PLANNED** |
| 4 | Uncertainty and falsification | 3 tasks **PLANNED** |
| 5 | Disease, immunity and organ extensions | 3 tasks **PLANNED** |
| 6 | Bounded research agents | 3 tasks **PLANNED** |
| 7 | Research workbench and scale | 3 tasks **PLANNED** |
| 8 | Independent research release | 3 tasks **PLANNED** |

Wave order expresses evidence and integration dependencies, not dates. Human domain-review time, hardware and paid compute are unallocated. Future work is split into bounded packets after prerequisites pass, and scale decisions use observed run size, throughput and recovery behavior.

See the [outcome roadmap](ROADMAP.md), [task contracts and lineage](TASKS.md), [canonical machine-readable ledger](plan/tasks.json) and [current evidence and gates](STATUS.md).

## Scientific and operating boundaries

Reject real patient records and identifiers, controlled-access clinical datasets, patient-derived synthetic data, unsupported parameter ranges and unreviewed intervention recommendations. No diagnosis, treatment advice, dosing guidance, surgical instructions, pathogen enhancement, infectious sequence design or wet-lab automation. Qualified reviewers must approve clinical or biological interpretation; software tests and agent reports do not substitute for them.

If a reference result cannot be reproduced without undocumented tuning, stop and repair the model, select another benchmark or narrow the claim. If qualified domain review is unavailable, continue only with contracts, code verification and published benchmark reproduction. Never fill a physiology gap with generated assumptions.

## Start contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), then run:

    python3 tools/validate_plan.py
    python3 -m unittest discover -s tests -v

The validator checks task synchronization, the dependency DAG, Wave 0 status transitions, document navigation; original-task preservation was independently checked against the initial Git revision. It validates the repository plan; it does not run or validate a scientific model.

The foundation is accepted and Lucas's owner launch authorizes the current local build. The [original VR-001 packet](plan/NEXT_WORK.md) remains preserved; the [independent control packet](plan/CONTROL_PACKET.md) explicitly separates this implementation from scientific admission. Referenced physiology engines and datasets are candidates. Their exact dependency, source and permission reviews remain required before adoption.

## Related independent projects

- [Grid Horizons](https://github.com/thepianistdirector/grid-horizons): simulate grids, transformers and energy systems before proposing physical changes.
- [Earth Rehearsal](https://github.com/thepianistdirector/earth-rehearsal): study water, pollution and climate interventions in reproducible software experiments.
- [Civic Safelab](https://github.com/thepianistdirector/civic-safelab): test public-safety sensing in synthetic worlds while measuring privacy and false alarms.
- [Lean Model Lab](https://github.com/thepianistdirector/lean-model-lab): seek reproducible training and inference efficiency gains with explicit quality tradeoffs.
- [Research Continuum](https://github.com/thepianistdirector/research-continuum): explore reproducible autonomous research with independently checked experiments.

These repositories are independently buildable. Shared experiment formats remain a design intention. Extract a common library only after at least two implementations demonstrate a stable need.

## License

Original repository content is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE). Third-party data, models, papers and code retain their own terms and are not relicensed here. No third-party dataset, model weight or upstream implementation is bundled in this foundation.
