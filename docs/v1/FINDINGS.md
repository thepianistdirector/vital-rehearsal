# Three reproducible findings from Vital Rehearsal

8 September 2026 · local methodological and engineering drafts · not peer reviewed

The three studies operated the real packaged CLI under frozen protocols. They retained **50 experiment bundles**: four source reproduction, eighteen numerical robustness, and twenty-eight synthetic scheduling runs. A separate GPT-6 Astra reviewer reproduced selected results with eight additional packaged runs and independently recomputed the original measurements. This is process separation on the same host, not human, institutional or empirical validation.

| Finding | What was measured | What an external researcher learns |
|---|---|---|
| **Solver agreement can reproduce inconsistent equations.** | The unchanged Ben-Tal combination exposure met the prespecified numerical comparison criteria, but its encoded pressure derivative differed from independent differentiation by as much as **7.406520732 mmHg/s**. | Reproduction needs semantic checks alongside cross-solver agreement. This finding concerns the exact CellML exposure, not a demonstrated error in the original paper. |
| **Local parameter response is distinguishable from observed numerical disagreement.** | R×0.9/1.1 gave maximum volume-trajectory differences of **0.0524807/0.0477650 L**, at least **13.49 million times** the combined observed numerical widths across all tested states. | Tight cross-algorithm controls help separate equation sensitivity from solver artifacts. The width is observed disagreement, not a certified error bound or a population confidence interval. |
| **Identical service increments behave differently across finite queue structures.** | Adding one second to each job increased mean waiting by **172.543–191.261 s** in two near-capacity single-server cases, exactly **399.5 s** in continuously busy cases, and **4.5 s** in separated batches. | Nominal load alone does not describe finite waiting. Matched inputs, workload recurrence and accounting explain the measured effects without clinical assumptions. |

The robustness study also found that tightening source-default VODE reduced its p_o disagreement from 0.001507 to 5.10×10⁻⁸ mmHg. An absolute-tolerance scaling concern for small z did **not** imply catastrophic realized error; unfavorable-to-that-hypothesis evidence is retained.

## Read and reproduce

1. [Source reproduction and semantic audit](../../research/reproduction/publication-manuscript.md): frozen protocol, four real platform bundles, independent XML/calculus checks, trajectory tables and figure.
2. [Solver and local resistance robustness](../../research/robustness/publication-manuscript.md): eighteen runs, three tight-algorithm controls, refinement, parameter effects, all-attempt inventory and uncertainty limits.
3. [Synthetic scheduling engineering study](../../research/scheduling/publication-manuscript.md): twenty-eight runs, twelve matched pairs, independent workload/Lindley/accounting checks and held-out semantics.
4. [Separate skeptical reproduction](../../research/review/review.md): independent checks, selected reruns, acceptance classification and remaining gates.

Use the [first-run guide](FIRST_RUN.md) to install the supplied offline dependencies. Each study gives rerun instructions that create new experiment directories. Historical absolute paths in inventories preserve what ran; fresh installs use their own paths. Confirmation code and its exact rc1 archive are preserved; candidate rc4 changes reporting, recovery and resource handling while the selected reproduced numeric outputs remain unchanged.

## Scientific boundary

The public source is [Catherine Lloyd's Ben-Tal CellML combination exposure](https://models.physiomeproject.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/view), revision 2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0, attributed under CC BY 3.0. It explicitly does not correspond to any one of the original paper's four models. No paper figures or independent empirical trajectories were obtained. The same-equation VODE comparator supports numerical comparison only. Explicit XML normalization constants account for unusual E and z unit labels; this work does not establish their dimensional invalidity.

No real patient records, clinical advice, treatment effects, validated physiological parameter distribution or scientifically reviewed care-to-physiology event mapping is included. The scheduler remains independent. The studies are a reproduction/negative semantic result, a numerical benchmark, and a synthetic engineering case study. No novelty or peer-review claim is made.

## Measured cost and coverage

Study-reported platform lifecycle wall totals were 4.097 s (source), 21.731 s (robustness), and 3.546 s (scheduling): **29.374 s across the 50 original attempts** on this host. These times include different proportions of integration and process overhead and are not throughput benchmarks. Study-driver and subprocess timings are nested and must not be added to these totals. The fresh-environment product check took 28.777 s, including offline installation and recovery checks; 65 regression tests passed in 9.852 s. Reviewer timing is retained separately. Monetary cost, full-host CPU use, and total LLM billing were not instrumented and are not estimated. No paid resources were purchased.

Qualified interpretation review and a real external researcher's first run remain pending. Public release, manuscript submission, outreach and Tanduna publication have not occurred.
