# Pulse exact-case metadata follow-up

Primary-owner follow-up, 2026-09-07. **HOLD continues; no physiology engine, scenario package or baseline trajectory acquired or run.** This record advances the bounded next discovery after the first browser-based candidate review. It does not erase the earlier access failures.

## Newly observed facts

The public GitLab API was accessible by ordinary anonymous HTTPS, although the earlier research browser received 403. Its supported [commit](https://docs.gitlab.com/api/commits/#get-a-single-commit) and [repository-tree](https://docs.gitlab.com/api/repositories/#list-repository-tree) metadata routes resolved the documentation marker to full source commit [`10710baa2835bdd0e43823fe50584574f5afec2a`](https://gitlab.kitware.com/physiology/engine/-/commit/10710baa2835bdd0e43823fe50584574f5afec2a), dated 2026-01-12. The root CMake manifest identifies **Pulse 4.3.2**, C++17 and CMake ≥3.15. This is source identity, not a verified release binary or local compatibility claim.

The exact root LICENSE and NOTICE were read in full. They identify Pulse's Apache-2.0 distribution, BioGears lineage and external components. Separate rights for reference archives and published research material still require their own coverage/provenance check. No source code was built and no install scripts ran.

| Exact same-commit path | Observed identity / purpose |
| --- | --- |
| `LICENSE` | Git blob `f49a4e16e68b128803cc2dcea614603632b04eac`; license text read |
| `NOTICE` | Git blob `b927f320bf830e55ce026f18c314ba0649c5dbed`; attribution/dependency notices read |
| `data/human/adult/validation/Scenarios/MechanicalVentilator/MechanicalVentilator.xlsx` | Git blob `5625b263fc0402cba4aa6f0cb749e8fbf44903f2`; metadata only, workbook not acquired |
| `data/human/adult/validation/Scenarios/MechanicalVentilator/MechanicalVentilator.json` | Git blob `2d1f1de57ecf53f0adfd2b136d22cb0d302aef49`; metadata only |
| `data/human/adult/validation/Scenarios/MechanicalVentilator/MechanicalVentilatorDataRequests.json` | Git blob `2fb63ae79b3cd352774f47c8151cb3142f3b5d7a`; metadata only |
| `data/human/adult/validation/Scenarios/MechanicalVentilator/MechanicalVentilatorTableDataRequests.json` | Git blob `22df048408e14bb21c989c2f15961e4e6b397f9f`; metadata only |
| `data/human/adult/validation/Scenarios/MechanicalVentilator/MechanicalVentilator-Healthy.md` | Git blob `38757c2d345d5b0a50418e0a2ea6dabfbd139a05`; source document read, generated output/table insertions identified |
| `data/human/adult/baselines/scenarios/MechanicalVentilator/Healthy.zip.sha512` | Git blob `e321ed95cf28a9900959595ff8b9f9439da59982`; content-addressed archive pointer read |

The baseline pointer is SHA-512:

```text
ce0daec2d64a119b57bc181d3a975cc97ccc3aaf87c08300ec413d5a30d3fcf766978d806046d30cec4a2018d4777d3a1629621c4e964dfe3bc349261c93a561
```

The same-commit `data/CMakeLists.txt` declares Kitware's content-addressed ExternalData download route. An anonymous HEAD of the [exact archive](https://data.kitware.com/api/v1/file/hashsum/sha512/ce0daec2d64a119b57bc181d3a975cc97ccc3aaf87c08300ec413d5a30d3fcf766978d806046d30cec4a2018d4777d3a1629621c4e964dfe3bc349261c93a561/download) returned HTTP 200, `application/zip`, filename `Healthy.zip`, and **6,791,285 bytes**. Its body was not downloaded. The archive's contents, complete required observables, time grid, source precision and rights are therefore unverified. A pointer and content length do not establish benchmark admission.

## Dependency metadata, not adoption

At this commit the inspected CMake external manifests reference Eigen 5.0.1, Abseil 20240722.0, Protobuf 29.2 (with a separately selectable 21.12 path), and optional pybind11 2.13.1. The default configuration enables Python/Java APIs and data generation. The Python requirements file is unpinned. The Protobuf CMake contains a Python `pip install --force-reinstall` build step when that API path is enabled. These settings have not been executed or approved. The native engine build must not inherit them blindly into this shared host.

This is not a complete approved dependency graph: build-option selection, transitive component licenses/security state, exact source hashes stronger than the supplied legacy checksums, generated-data completeness and a bounded local resource envelope are still needed. No numerical dependency approval request or installation is claimed.

## Remaining narrow gate

First verify separate reference-archive rights/provenance and inspect a permitted same-revision case manifest. If lawful intake is established, inspect only this archive under size/path/type bounds; do not fetch all validation data. Determine whether it contains a pre-existing numeric reference, the exact scenario and required reference-state inputs, and whether the case can be reconstructed without undocumented tuning or chart tracing. Freeze criteria from source precision/numerical analysis before running any local candidate output.

Reference generated by the upstream implementation can support only explicitly bounded model-reference regression reproduction. It cannot be promoted to empirical validation, clinical benefit, or an independent physiological confirmation. The evaluator must remain separately controlled. Qualified context review and independent researcher reproduction are still unavailable under the owner's current answer.

Read-only metadata/license/manifest responses and their local SHA-256 are retained in ignored `.cache/benchmark-metadata/`. The broad `data` tree inspection stopped after its first page once the relevant exact subtree was discovered; no claim of whole-repository enumeration is made. A guessed documentation directory returned 404; the relevant paths above were then obtained from actual tree entries. No patient record, generated model, publication figure or numerical reference output was saved by this follow-up.
