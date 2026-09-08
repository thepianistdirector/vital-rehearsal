# Candidate A: Pulse MechanicalVentilatorHealthy

Review date: 2026-09-07. Recommendation: **HOLD; first priority for a bounded source-metadata discovery packet.** No Pulse artifact was acquired or executed.

## Identity and original evidence

**P1 observation:** the official named case exposes circulation and gas observables, numeric summary tables, and plots. Its page carries generation marker `2026-02-01 - 10710baa2`; this short marker is not a verified full immutable source identity. The setup includes a pressure setting labeled for adjustment rather than a complete reproducible value in its settings table. Selected source-displayed examples are `Aorta-Oxygen-PartialPressure(mmHg)` = 115, `Aorta-CarbonDioxide-PartialPressure(mmHg)` = 41.9, and `CardiacOutput(L/min)` = 5.60. These are engine outputs, not independent reference trajectories. No exact horizon, sampling or initial-state recipe was verified from that page. [P1](https://pulse.kitware.com/md__mechanical_ventilator__healthy.html)

**P2 observation:** the version page has a 4.3.0 heading, a 4.3.1 January 2025 release entry, and an integration section. It discusses generic validation defaults and rounded table reporting. Those facts prevent assuming that every displayed validation value belongs to a released 4.3.0 binary; generic percentages are not adopted as this project's numerical criteria. [P2](https://pulse.kitware.com/version.html)

**P3 observation:** Arnal et al., *Parameters for Simulation of Adult Subjects During Mechanical Ventilation*, DOI `10.4187/respcare.05775`, Respiratory Care 63(2), 158–168 (2018), reports aggregate measurements for passively ventilated adults, including 138 classified with normal lungs. The normal-lung static-compliance median and IQR are 54 [44–64] mL/cm H2O; inspiratory resistance is 13 [10–15] cm H2O/L/s. The paper discusses rounded standardized simulation parameters, a single-site/single-mode limitation, and explicitly limits the meaning for actual care. Its HTML substantive sections from introduction through conclusions and footnote were read; image-encoded tables 1, 2 and 9 were not successfully retrieved. The population is not healthy volunteers. [P3](https://journals.sagepub.com/doi/full/10.4187/respcare.05775)

## Comparator, units and applicability

The empirical aggregate mechanics summaries above are independent measurements, but the scenario uses published mechanics values for configuration. Agreement with configured values is not held-out gas-exchange validation. The Pulse reference and engine columns must remain separate. No independent raw gas/circulation trajectory, exact output reduction window or interpolation error was identified in the inspected sources. No tolerance is proposed; population IQR, source rounding, sensor error and numerical discretization have different meanings and cannot be substituted for each other.

Proposed first claim, only after admission: reproduce the exact upstream passive reference case's declared observables under its exact documented setup. Exclude patient specificity, healthy-population representativeness, spontaneous breathing, demographic variation, delayed care, clinical benefit and treatment selection. The scenario must be verified to use a non-person-specific aggregate/reference configuration before intake. No individual records may be acquired.

Native names found in the scenario include pressure `mmHg`, volume `mL`/`L`, flow `L/min`, frequency `1/min`, resistance `cmH2O_s/L`, compliance `mL/cmH2O`, and dimensionless fractions. This is an inventory, not a validated unit mapping. Intake must resolve compartment semantics, pressure reference, exact conversion factors and the relationship between clinical and model quantities. Similar dimensionless names do not establish interchangeable observables.

## Rights, execution and failures

The Apache-2.0 legal text was inspected. It does not itself identify every file covered by the candidate's license or clear third-party publications, figures and reference data. The exact upstream NOTICE link failed to load in the research browser. The original paper is free to read and provides a permissions route; no general redistribution grant for its tables/figures was established. Store only these short source-attributed research notes and links for now. [P3](https://journals.sagepub.com/doi/full/10.4187/respcare.05775), [P4](https://www.apache.org/licenses/LICENSE-2.0)

Official Pulse documentation identifies a C++ engine with Linux support and multiple language interfaces. Exact source/dependency graph, binary ABI, resource use, approved local build and offline runtime remain unknown. Source and tags endpoints returned 403 in the browser; this reports tool access, not absence of the repository. No production package/version is adopted. [P5](https://gitlab.kitware.com/physiology/engine), [P7](https://pulse.kitware.com/)

Scenario documentation describes CSV output and fatal boundary cases. Version notes describe initialization/error reporting. These suggest hooks to examine, not verified adapter behavior. Require explicit failure for initialization/stabilization failure, version mismatch, non-finite or missing values, incomplete time grid and nonconvergence; preserve diagnostics and assign no favorable scientific conclusion. A bare subprocess is not an isolation boundary. [P8](https://pulse.kitware.com/_scenario_file.html), [P2](https://pulse.kitware.com/version.html)

## Sources inspected

| ID | Exact source | Access/evidence boundary |
| --- | --- | --- |
| P1 | [MechanicalVentilatorHealthy](https://pulse.kitware.com/md__mechanical_ventilator__healthy.html) | Official HTML read, including output tables; no downloadable scenario/reference package inspected. |
| P2 | [Pulse version history](https://pulse.kitware.com/version.html) | Official HTML read; does not resolve full case commit. |
| P3 | [Arnal original publication](https://journals.sagepub.com/doi/full/10.4187/respcare.05775) and [PubMed metadata](https://pubmed.ncbi.nlm.nih.gov/29042486/) | Substantive original HTML text and abstract metadata read; image tables attempted unsuccessfully. |
| P4 | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) | License text inspected; exact package coverage not established. |
| P5 | [Official engine repository](https://gitlab.kitware.com/physiology/engine) and [tags](https://gitlab.kitware.com/physiology/engine/-/tags) | Browser returned 403; exact manifests/source not inspected. |
| P6 | NOTICE link on [official case page](https://pulse.kitware.com/md__mechanical_ventilator__healthy.html) | Link followed; content unavailable in browser. Do not claim NOTICE reviewed. |
| P7 | [Pulse home/source and platform documentation](https://pulse.kitware.com/) | Official HTML read. |
| P8 | [Scenario format documentation](https://pulse.kitware.com/_scenario_file.html) | Primary-source indexed text inspected; exact named scenario still unresolved. |
| P9 | [Pulse bibliography](https://pulse.kitware.com/citelist.html) | Followed source citations; Arnal identity resolved. Textbook reference does not supply a rights-cleared independent trajectory. |

The next step is the exact-case manifest and reference discovery described in the [admission decision](../VR-001-benchmark-decision.md#smallest-next-discovery-and-stopping-rule). Installing an engine before resolving these gaps is not recommended.
