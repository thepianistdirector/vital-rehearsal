# Sources, candidate tools and data policy

Primary standards, official documentation and research sources inspected for the architecture foundation on 2026-09-07 are listed below. A listing supports only the stated planning decision. It does not establish that a model is applicable, a dataset may be redistributed, an integration works or a scientific claim is valid.

## Modeling credibility and verification

| Source | What it supports here | Boundary |
| --- | --- | --- |
| [FDA: Assessing the Credibility of Computational Modeling and Simulation in Medical Device Submissions](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-credibility-computational-modeling-and-simulation-medical-device-submissions) | A risk-informed credibility plan tied to a precise question and context of use; distinct verification, validation and uncertainty evidence for mechanistic models. | Vital Rehearsal is not claiming a medical-device submission or regulatory acceptance. The framework must be tailored to this research context. |
| [FDA Regulatory Science Tool: Verification Test Problems for Cardiac Electrophysiology Modeling Software](https://cdrh-rst.fda.gov/verification-test-problems-cardiac-electrophysiology-modeling-software) | Known analytic solutions and convergence-rate checks are strong code-verification patterns. | The monodomain/bidomain problems apply to cardiac electrophysiology solvers. They do not validate whole-body hemodynamics, gas exchange or the first cardiopulmonary context of use. |
| [FDA Regulatory Science Tool: Identifiability of Cardiac Electrophysiology Models](https://cdrh-rst.fda.gov/identifiability-cardiac-electrophysiology-models) | Sensitivity and uncertainty analyses can be misleading when model parameters are not identifiable. | The supplied example is cardiac electrophysiology-specific and must not be generalized as a validated method or parameter set for other organ models. |
| [AHRQ: Guidance for the Conduct and Reporting of Modeling and Simulation Studies in Health Technology Assessment](https://effectivehealthcare.ahrq.gov/products/decision-models-guidance/methods) | Transparent model structure, inputs, source traceability and communication of uncertainty. | It is reporting guidance, not approval of this architecture or any future outcome. |
| [STRESS guidelines entry and source paper](https://www.equator-network.org/reporting-guidelines/strengthening-the-reporting-of-empirical-simulation-studies-introducing-the-stress-guidelines/) | Reporting fields for discrete-event, system-dynamics and agent-based simulation studies, including objectives, inputs, execution and uncertainty. | Checklist completion improves transparency; it does not establish model validity or reproducibility on its own. |

## Candidate physiology engines and models

| Source | What it supports here | Conditional decision |
| --- | --- | --- |
| [Pulse Physiology Engine documentation index](https://pulse.kitware.com/pages.html) | Pulse documents cardiovascular, respiratory, tissue and other systems, validation pages, a current version page and Apache-2.0 distribution. | Candidate A for VR-001/VR-002. Adopt only if an exact public benchmark artifact exposes the required heart-lung observables, the release/build works in the approved environment, terms permit the intended use, and limitations fit the first context of use. |
| [Pulse cardiovascular methodology](https://pulse.kitware.com/_cardiovascular_methodology.html) | The cardiovascular model is a closed lumped-parameter circuit with systemic/pulmonary circulation, documented assumptions, system feedback and named limitations. | Its low-resolution whole-body behavior must not be treated as tissue mechanics, cardiac electrophysiology or patient-specific anatomy. Validate only the selected outputs and scenario. |
| [Pulse respiratory methodology](https://pulse.kitware.com/_respiratory_methodology.html) | Candidate source for respiratory model scope, variables, coupling assumptions and limitations. | The exact validation case, inputs, outputs and reference evidence must be selected before any tolerance or applicability claim is written. |
| [Physiome Model Repository](https://models.cellml.org/welcome) and [CellML model overview](https://www.cellml.org/model/index) | Candidate B discovery surface for versioned, published CellML models, including cardiovascular, respiratory, hepatology and immunology categories. | Repository/curation status is discovery evidence only. Select a model only after execution, publication match, license, units, completeness and benchmark artifacts are audited. |
| [BioModels](https://www.ebi.ac.uk/biomodels/) | Discovery surface for literature-based mathematical models in standard formats, including disease, signaling, pharmacology and epidemiology. | A later disease or immune candidate must be individually audited; catalog presence does not prove reuse rights, identifiability, reproducibility or applicability. The official service is migrating, so pin stable record identifiers and retrieval metadata. |
| [ChEMBL](https://www.ebi.ac.uk/chembl/) | Public bioactivity records may provide later source provenance for hypothesis reproduction. | Bioactivity does not establish therapeutic efficacy, clinical effect or dosing. No ChEMBL download is part of the first milestone. |

## Interoperability, units and provenance

| Source | What it supports here | Conditional decision |
| --- | --- | --- |
| [UCUM specification 2.2](https://ucum.org/ucum) | Case-sensitive machine-readable unit syntax and semantics based on dimensional analysis. | Use UCUM codes where applicable, but do not claim full conformance from syntax checking. Exact supported units and conversion tests belong to the first implementation contract. |
| [SED-ML Level 1](https://sed-ml.org/) | A tool-independent way to encode models, simulation procedures, modifications, outputs and presentation for reproducible simulation experiments. | Candidate export/import format after the internal contract is stable. Supporting a subset requires explicit feature bounds and round-trip tests. |
| [COMBINE Archive specification](https://combinearchive.org/) | Candidate packaging convention for related model and simulation files. | Use only after exact current specification, implementation behavior and nested-archive safety are reviewed. It does not replace the project's result, failure, rights or provenance contract. |
| [SBML](https://sbml.org/) | Candidate upstream model representation for systems-biology adapters. | Preserve exact upstream semantics; do not force whole-body or care-process models into SBML. |
| [Functional Mock-up Interface 3](https://fmi-standard.org/) and [FMI co-simulation semantics](https://github.com/modelica/fmi-standard/blob/main/docs/4___co-simulation.adoc) | Defines model exchange/co-simulation interfaces, communication points, capability flags, early return and state handling across simulators. | Defer adoption until at least two independent engines need it and a spike proves it reduces adapter code without masking time, rollback or direct-feedthrough limits. |
| [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/) | Entity/activity/agent relations provide a sound vocabulary for source and derivation lineage. | Begin with a small JSON projection. Add RDF/PROV-O serialization only when interoperable provenance exchange is an observed need. |

## Public aggregate health inputs for later research

| Source | What it supports here | Boundary |
| --- | --- | --- |
| [WHO Immunization Data Portal and data description](https://www.who.int/teams/immunization-vaccines-and-biologicals/immunization-analysis-and-insights/global-monitoring/data-statistics-and-graphics) | Candidate aggregate country/regional vaccination coverage, disease surveillance and programme indicators for later population-level research. | Exact extracts, revision dates, definitions, corrections, missingness and reuse terms require a source record. Coverage data cannot calibrate within-host immune response or establish effectiveness for an individual. |
| [CDC open data portal](https://data.cdc.gov/) | Discovery point for public aggregate public-health datasets. | Each dataset needs its own license/terms, schema, revision, suppression and population audit. Portal availability alone is not permission to redistribute. |
| [NIH notice on controlled-access human genomic data and generative AI](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-081.html) | Reinforces that controlled-access genomic data and derivatives cannot be distributed outside authorized access. | Vital Rehearsal excludes controlled-access and patient-level data entirely; it does not build a workflow for obtaining access. |

## Benchmark selection still open

VR-001 must compare at least these two routes:

1. **Pulse route:** one exact healthy or non-patient-specific cardiopulmonary validation case whose downloadable inputs, reference observables, engine output fields and limitations can be inspected.
2. **Published CellML/SED-ML route:** one literature-backed cardiopulmonary model with executable files, explicit units, reproducible reference outputs and clear reuse/redistribution terms.

The FDA cardiac electrophysiology test problems may later verify a cardiac EP solver but are not a substitute for either route. The selection questions and acceptance contract are in [plan/NEXT_WORK.md](plan/NEXT_WORK.md).

## Source admission checklist

Before adopting any dependency, model or dataset, record:

- exact publisher, stable identifier, release/revision date and retrieval route;
- code/data/model license, access terms, attribution and redistribution permission;
- governing equations or collection method, population/organism, coverage and missing variables;
- variables, quantity semantics, units, reference frames and source precision;
- calibration, confirmation and validation evidence, including known contradictory evidence;
- runtime/transitive dependencies, native code, safe-loading behavior and network/telemetry;
- storage/compute cost, supported platforms, maintenance/advisory state, alternatives and rollback;
- every transformation and whether derived artifacts may be shared.

No model or dataset download, dependency installation, paid run or external account action is authorized by this document. Exact versions are deferred until VR-001 and VR-002 have current compatibility and rights evidence.

## Evidence limits

Official documentation establishes what a source or tool says it provides. Vital Rehearsal must independently verify code behavior and reproduce the selected observable. A model card and qualified review establish only the declared context of use. No source listed here proves a clinical outcome, a safe intervention, a representative synthetic cohort or an implemented integration.
