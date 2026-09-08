# Candidate B: Ben-Tal 2006 CellML, with separated revisions

Review date: 2026-09-07. Recommendation: **HOLD.** This is discovery of a published respiratory model route; no model, session, COMBINE archive or reference dataset was acquired or executed. No SED-ML experiment has been verified.

## Exact identifiers and version distinction

| Record | Identity observed | What is established |
| --- | --- | --- |
| Original publication | Alona Ben-Tal, *Simplified models for gas exchange in the human lungs*, Journal of Theoretical Biology 238(2), 474–495 (2006); DOI `10.1016/j.jtbi.2005.06.005`; PMID `16038941` | Publication metadata and abstract read through PubMed. Full original paper was not obtained; publisher full-text route failed in the browser. [C1](https://pubmed.ncbi.nlm.nih.gov/16038941/) |
| Primary comparison exposure | `b503501533abcf0e70786789f08cb902`, file `bental_2006.cellml`, changeset `2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0` | Exposure metadata names Catherine Lloyd, publication and CC BY 3.0. Full changeset is exposed by a workspace file page; its commit description mentions a session and XUL file. The executable/session pair was not fully inspected. [C2](https://models.cellml.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/cmeta), [C5](https://models.cellml.org/workspace/bental_2006/file/2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0/ben-tal_2006d.xul) |
| Related newer exposure | `e/414`, `bental_2006.cellml`, short changeset `a854d85c5ff5` | Metadata says license unspecified. Documentation describes a combination of publication equations, rather than one of its four individual models. Historical PCEnv/COR success is a curator statement, not a local reproduction. [C3](https://models.cellml.org/e/414/view) |
| Distinct older model D | Exposure `966b97976e17411b935d387c871ecb10`, file `bental_2006_d.cellml`, changeset `aec2cb935d5ebf99fa6637ac490fb1aa7975ca95` | Expired exposure's generated-Python view reports a units-related code-generation error. It is not evidence that the newer comparison exposure fails for the same reason. [C4](https://models.physiomeproject.org/exposure/966b97976e17411b935d387c871ecb10/bental_2006_d.cellml/%40%40cellml_codegen/Python) |

These are different artifacts. Do not transfer a license, successful-execution statement, code-generation failure or publication mapping between them without inspecting the intervening changes. A filename ending in `d` or a cardio-respiratory keyword does not establish that a model exactly reproduces publication model D.

## Applicability and comparison gaps

The original abstract describes a hierarchy of human lung gas-exchange models and examines assumptions about mouth flow, volume change and oxygen binding. That does not establish a complete cardiovascular circulation model at the required context-of-use resolution. The exact exposure's supported reference parameter domain, biological interpretation and mapping to a published experiment remain unreviewed. [C1](https://pubmed.ncbi.nlm.nih.gov/16038941/)

No independent numeric trajectory, source-specific simulation horizon/time grid, prescribed solver/tolerances, stabilization procedure, reference precision or acceptance criterion was found in the inspected metadata. The generated-code index offers C, C_IDA, F77, MATLAB and Python views; this is not proof that any exact output runs, that defaults reproduce the paper, or that a current dependency graph is safe and portable. [C6](https://models.cellml.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/cellml_codegen)

The session-associated metadata shows candidate semantic paths such as `gasTransport/p_o`, `gasTransport/p_c`, `gasExchange/f_o`, `gasExchange/f_c`, `lungMechanics/V_A` and `Environment/time`. They are source labels to investigate, not a released observable contract. Exact units, pressure frames, sampling and event semantics must be read from the same immutable model/session and matched to the paper. No values or conversions are guessed. [C5](https://models.cellml.org/workspace/bental_2006/file/2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0/ben-tal_2006d.xul)

A COMBINE-download link only establishes a packaging option. It does not establish that the archive contains SED-ML, numeric reference results, convergence settings, a functioning solver or third-party redistribution rights. Agreement against outputs generated from the same translated equations would be numerical reproduction evidence with stated dependence; it cannot be presented as independent physiological validation.

## Rights and executable boundary

The older primary comparison exposure explicitly advertises CC BY 3.0; the Creative Commons deed was inspected and requires attribution and change indication for adaptations. This does not clear the original article or an unseen reference dataset, and it must not be applied to the newer exposure with unspecified terms. Model/package files require an exact rights inventory before storage or redistribution. The original paper's full-text availability and figure/data rights remain unresolved. [C2](https://models.cellml.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/cmeta), [C7](https://creativecommons.org/licenses/by/3.0/)

No runtime is selected. Historical PCEnv/COR claims, generated code and an OpenCOR launch link do not constitute a reviewed dependency graph. The visible XUL source includes scripts; it must not be launched as trusted model data merely because it is hosted by a model repository. Metadata reading here did not execute it. No model correction, invented parameter, generated physiology or manual curve tracing is an authorized way to repair missing publication correspondence.

## Sources inspected

| ID | Source | Access/evidence boundary |
| --- | --- | --- |
| C1 | [PubMed original publication record](https://pubmed.ncbi.nlm.nih.gov/16038941/) | Metadata/abstract read; full paper not read. Publisher link attempted and unavailable. |
| C2 | [Exact exposure metadata](https://models.cellml.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/cmeta) | Primary page search-index text read; direct open returned 403. Rights statement therefore requires live recheck before acquisition. |
| C3 | [Related exposure documentation](https://models.cellml.org/e/414/view) and [metadata](https://models.cellml.org/e/414/bental_2006.cellml/cmeta) | Primary indexed content read; direct documentation fetch returned 403. Short revision only verified. |
| C4 | [Older model D generated-code failure](https://models.physiomeproject.org/exposure/966b97976e17411b935d387c871ecb10/bental_2006_d.cellml/%40%40cellml_codegen/Python) and [full revision source metadata](https://models.cellml.org/workspace/366/file/aec2cb935d5ebf99fa6637ac490fb1aa7975ca95/bental_2006_d.cellml) | Indexed primary metadata and diagnostic text read; no code executed or saved. |
| C5 | [Full changeset/session-associated workspace metadata](https://models.cellml.org/workspace/bental_2006/file/2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0/ben-tal_2006d.xul) | Indexed primary source view read; confirms full revision and 2010-08-05 commit date, not experiment completeness. |
| C6 | [Generated-code index](https://models.cellml.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/cellml_codegen) | Indexed primary content read; exact Python view attempted and unavailable. |
| C7 | [Creative Commons BY 3.0 deed](https://creativecommons.org/licenses/by/3.0/) | Read directly; no statement that unseen assets inherit the model license. |

The smallest CellML-specific follow-up would obtain lawful reading access to the full original paper, then identify an exact experiment plus same-revision model/session and independent numeric reference. This is a fallback to the first-priority Pulse discovery packet, not a request to install multiple engines. The [admission HOLD](../VR-001-benchmark-decision.md) remains in force.
