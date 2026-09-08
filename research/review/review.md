# Separate skeptical reproduction and review

8 September 2026. Reviewer runtime model independently verified as **gpt-6-astra** in its active turn context, session `01a0820e-778a-7b11-a349-1f3f594f1473`. Leaf reviewer; no delegation. Work confined to this review directory. This is a distinct automated process on the same host and shared working tree, not qualified human review, external-machine reproduction, or adversarial isolation.

**Disposition: accept all three as bounded local computational research drafts. No newly identified blocking product defect or incorrect substantive numerical result. Human interpretation, external human reproduction, publication and public release remain pending.**

| Study | Classification | Evidence and scope |
|---|---|---|
| Exact-exposure reproduction | ACCEPT for local research draft | All 28 retained state/comparator checks independently recomputed; selected frozen and revised archive runs reproduced bytes exactly. XML-derived pressure identity fails independently. No paper-model or empirical reproduction claim is accepted. |
| Solver/resistance robustness | ACCEPT for local research draft; minor wording improvement below | All 126 solver/state error rows and 14 parameter-effect rows recomputed; three tight Radau R settings rerun with revised archive, identical trajectories. The numerical envelope is observed agreement, never a truth-error bound. |
| Finite synthetic scheduling | ACCEPT for local research draft | All 28 schedules and 12 paired effects independently recomputed; paired near-capacity and idle-tie cases rerun identically. Finite synthetic engineering examples only. |

## Actual reproduction and numerical comparisons

The reviewer executed **eight sequential packaged CLI run calls**, against a maximum budget of ten. Two cases tested the reproduction study's Radau settings using rc1 and rc4; three tested robustness tight Radau at R multipliers 0.9, 1 and 1.1 using rc4; three tested scheduling near/seed1701 at delays 0/1 plus the idle-gap ASCII tie case using rc4. All eight ran into fresh disjoint directories and passed actual packaged `research inspect`. Sixteen successful CLI calls, no unsuccessful CLI calls. Measured reviewer script wall time was 9.592 seconds on this host; not a performance distribution or monetary estimate.

Every selected trajectory/schedule is byte-identical to its matched original study artifact. Statewise maximum numerical differences are exactly zero. Reports/runtime records are expected to differ because of version, timings, UUIDs and corrected wording. [Numerical comparison table](confirmation-v2/rerun-comparisons.csv) and [complete command ledger](confirmation-v2/commands.json) retain the evidence; stdout/stderr and full source-bearing bundles are adjacent.

| Independent check | Result |
|---|---:|
| Original bundle manifests, experiment seals and frozen source hashes | 50 / 50 pass |
| Original reproduction state/comparator checks | 28 / 28 pass |
| Original robustness solver/state errors | 126 / 126 match author values |
| Resistance effect rows | 14 / 14 match author values |
| Original queue schedule checks | 28 / 28 pass |
| Queue paired effects | 12 / 12 match author values |
| Maximum pressure derivative identity discrepancy | 7.406520731539602 mmHg/s |
| Independent centered finite-difference disagreement | 2.803514975724397e-9 mmHg/s |
| Minimum resistance effect / combined control width | 13,494,193.392676687 |

The original command ledgers reconcile to 18 commands / 4 runs for reproduction, 37 / 18 for robustness and 88 / 28 for scheduling. There are no unexpected nonzero return codes. The three scheduling rejection probes are retained and expected. Source retrieval failures are explicitly recorded separately. No missing completed confirmation attempt was found within the supplied campaign directories; this does not prove that undisclosed work outside the supplied records never occurred.

One **reviewer preparation error** is preserved: the initial review script independently used compact JSON instead of the platform's documented pretty canonical JSON for its seal check. It stopped before any platform CLI run. The corrected script and fresh `confirmation-v2` directory contain all eight executions; `confirmation/REVIEWER_ERROR.txt` records the failed preparation. No original study evidence was changed and no run budget was spent on that error.

## Independent scientific checks

The review reads and evaluates the retained XML MathML expressions for `PluralPressureFunction`, rather than importing either the generated model or the platform diagnostic helper. Its unit-bearing constants are evaluated as magnitudes in their declared source units. Separately differentiating P_L gives the expected cosine and sine terms; the XML dP_Ldt retains a −6.25 offset and a different sine coefficient. At t=0 its residual is already −6.25 mmHg/s, independent of integration. Evaluated XML pressure and encoded derivative match the exported columns to below 1e-10; centered differences of the XML pressure agree with the independent derivative below 1e-6. [XML audit CSV](confirmation-v2/xml-pressure-audit.csv).

The unit-bearing XML literals support the manuscript's correction that unusual E and z declarations are **not by themselves proven dimension errors**. Seconds and litres in pressure normalization restore dimensional balance; z is declared dimensionless and its rate and transport contribution include normalization factors. The reviewer did not perform a full formal CellML unit check or rederive the full gas-transport system. The calculus mismatch is established; its biological consequence and a corrected model are not.

The robustness reanalysis independently forms per-time algorithm ranges from the three tight controls at each R, takes their maximum widths, verifies the baseline Radau step refinement, and recomputes maximum and endpoint parameter changes. All seven states pass their frozen convergence thresholds, and all 14 effects exceed ten times the relevant combined widths. The smallest actual ratio is approximately 1.35e7. [Per-state results](confirmation-v2/independent-state-effects.csv). Separate retained-data analysis verifies all scalar-z error/relative-error entries against their trajectories. No probabilistic uncertainty estimate follows from these deterministic cases.

The scheduling review uses a completion-history scan to choose earliest prior completion and lowest server id on equality, independent of the production heap. All original schedules, including held-out cases, reproduce. The author's additional sorted-workload-vector recurrence was read: it subtracts interarrival time, clips workloads at zero, assigns to the minimum, then reorders; it computes wait/start/finish without depending on server labels. This provides a distinct numerical representation, while the identity check intentionally shares the declared dispatch rule. The review confirms the idle-gap example assigns `later` to server1 after its earlier prior completion even when both servers are idle. The 16-server tie, permutation and boundary cases are retained and included in the original-bundle checks. All paired mean/p95/makespan effects were recomputed from the independently checked schedules. [Queue checks](confirmation-v2/independent-queue-checks.csv).

## Provenance, rights and frozen methods

The admission and acceptance contract were read. The retained exposure documentation explicitly calls this a combination of equations, not one of the original paper's four models. Retained metadata and view pages attach CC BY 3.0 to this exact exposure. XML and generated source hashes agree with declared identities, and all 50 original bundles retain the model notice and application license. No article text/figures, empirical reference trajectory, patient data, clinical inference or novelty claim is needed for any accepted result. Rights beyond the exact admitted exposure are not inferred.

Reproduction's protocol JSON matches its frozen digest. Robustness and scheduling protocol and executable-driver hashes match their preconfirmation campaign metadata. The reproduction artifact inventory and robustness campaign checksum inventory have no mismatches. Scheduling has 28 internally consistent bundle manifests plus command and result inventories; it does not claim a separately signed campaign manifest. Hashes provide change detection, not trusted timestamps or proof of authorship. The prospective status rests on retained workflow evidence and disclosed prior exploratory information, not an external preregistration authority.

Frozen platform SHA256: `bc4043aa8c99b16354dd08aaf595c09a65a7b070be981ba435ba4c41210b2db2`.

Revised rc4 SHA256: `2d7f67e808e9cd176d753a49054882091184309586230f3b5a4a617f8e2ab1f9`.

## Product review and manuscript refinements

The review inspected the packaged rc1/rc4 differences and current research adapter, scheduler, persistence path, manifest inspection, worker launch and recovery. Generated equations and scheduler source are byte-identical between archives. The numerical adapter changes only its warning/unit text. Research-command changes concern reporting, integrity, resource/environment containment and new-attempt recovery. The eight completed runs provide selected revised-build compatibility evidence, not an exhaustive new-version campaign. [Retained source diff](confirmation-v2/build-source.diff).

No product blocker was found in this narrow review. Hard-killed coordinator attempts may remain unfinalized; this is documented and recovery creates a new attempt. Same-user modification and rewritten manifests remain possible and are explicitly outside hostile-isolation claims. Fresh-environment installation, interruption/resource-cap and browser accessibility evidence belong to the maintainer's separate package validation; this review does not claim to have repeated those tests.

Minor nonblocking refinements:

1. Robustness describes tightened VODE disagreement as predominantly “comparator tolerance error.” That run changes maximum step jointly with tolerances. “Comparator numerical settings” would make the attribution more exact; no isolated tolerance-only decomposition was performed. This does not change any measured result.
2. Link each manuscript's reproduction paragraph to the shared first-run/offline dependency guide, particularly robustness, whose commands assume an existing `.venv`. The current [first-run guide](../../docs/v1/FIRST_RUN.md) supplies the pinned offline setup and retained investigation-build layout. Original absolute paths in command logs are historical provenance, not portability requirements.
3. Preserve historical rc1 labels in immutable bundles. The revised normalized-unit wording is better supported than the earlier blanket “unit inconsistencies” warning; the reproduction manuscript already explains this distinction. Do not rewrite confirmation artifacts to make their wording match rc4.

None of these changes requires new integrations or changing a frozen protocol/driver. The scientific limitations are substantial but explicit: shared equations and libraries, one host, short horizon, fixed initial state, admitted numerical parameter range, sampled maxima, finite synthetic queues, two chosen seeds, duplicate burst workloads, and no reviewed coupling. Those limitations block physiological or clinical generalization, not the bounded computational findings.

## Reproduce this review and remaining gates

From `vital-rehearsal`, after the supported CPython 3.12 environment with NumPy 2.2.6 and SciPy 1.15.3 is installed:

```sh
.venv/bin/python research/review/reproduce.py --output research/review/your-new-review
```

The output must not exist. Keep the retained study directories and both named distributions in the supplied project layout. This review script uses its invoking interpreter for subprocesses and verifies archive hashes before running; it needs NumPy but no plotting package. It performs eight sequential integrations/queue runs and exits on a failed check. The second script, `audit_retained.py`, performs only retained-data verification; its original output is `retained-audit/` and it refuses to overwrite it. Its source is executable evidence of the table and ledger audit, not a simulator.

Original synthetic reviewer code/tables follow repository AGPL-3.0-or-later. Existing source notices are preserved in bundles. No paid services or public writes were performed. LLM token/billing counters were unavailable and are not estimated.

**Local research review gate: satisfied by this separate automated review.** Qualified human interpretation, external human reproduction, publication, public release approval and Tanduna readback remain **PENDING**, as required by the contract. This document does not close the overarching Goal or authorize those actions.
