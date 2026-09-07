# Sources, candidate tools and data policy

Official entry points inspected while preparing this plan on 2026-09-07. These links support the bounded descriptions below; they do not prove an implemented integration, available benchmark data, endorsement or scientific validity for every planned scenario.

| Source | Supported planning use |
| --- | --- |
| [Pulse Physiology Engine](https://pulse.kitware.com/) | Official engine description and documentation entry point; candidate for physiology simulation. Every supported condition needs its own validation review. |
| [ChEMBL](https://www.ebi.ac.uk/chembl/) | Public bioactivity resource for later hypothesis provenance. Respect its dataset license and never interpret a bioactivity record as clinical efficacy. |

## Before adopting a dependency or dataset

Record the exact official release and license, maintenance/advisory state, runtime and transitive dependencies, safe loading behavior, telemetry/network use, storage/compute cost, alternatives and rollback. A source being listed here does not authorize installation or data download. Exact versions are deliberately deferred until the implementation environment and compatibility evidence exist.

For each dataset/model, document provenance, permitted use, attribution, redistribution rights, access requirements, geography/population/time coverage, uncertainty and missing variables. Link source records to all derived artifacts. Reject incompatible terms and use an honestly labeled synthetic fixture when appropriate. Keep private information, credentials, controlled-access data and third-party assets out of this public repository.

## Evidence limits

Pulse is a candidate for the first physiology adapter. A small standard-library event scheduler is the initial care-process baseline. Bioactivity data can inform a later literature/reproduction lane; they do not establish efficacy. Select an immune-model engine only after a public benchmark and lawful reusable model are identified.

Official tool documentation establishes the tool's stated purpose; our model cards and independent benchmarks must establish applicability to our experiment. Sources are not blanket proof for results we have not measured. The project's original documents use AGPL-3.0-only; referenced material retains its own terms.
