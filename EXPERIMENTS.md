# Vital Rehearsal experiment and evaluation contract

Status: accepted architecture-foundation requirements; the local software-control experiment exercises infrastructure only. No physiological experiment has run in this repository.

## Current independent control

The fixed integer-identity control in `scenarios/contract-control.json` has no physiological meaning. Its evaluator owns literal reference values and a zero-error rule justified only by exact integer arithmetic. Numerical CSV values are compared as bounded exact decimals; no implicit interpolation or rounding is permitted. The producer cannot supply a replacement criterion. JSON source, model card, reference, criteria, software identity and invocation are frozen before execution and retained in each attempt.

Explicit faults exercise contradictory output, wrong units, incomplete/nonfinite/out-of-domain output, injected nonconvergence, crashes, timeout and interruption. Their records distinguish execution state from conclusion and retain failures. This proves control behavior only; it does not satisfy the source-grounded physiological, cohort, conservation, uncertainty or human-review requirements below. The clinical interpretation and independent researcher gates remain pending; Lucas reported that no reviewer/reproducer is available for now.

## Research question

Reproduce one published, non-patient-specific cardiopulmonary benchmark, then compare baseline and delayed-care workflow scenarios over a small synthetic cohort. Export trajectories, uncertainty and a reproducible experiment report. The initial experiment studies model response and workflow timing; it does not recommend treatment or simulate a surgical technique.

## Inputs and evidence

Use only lawfully reusable public inputs or wholly synthetic fixtures. Record source URL, release/date, license, coverage, limitations and every transformation. Public availability does not imply unrestricted reuse. Never download controlled data, copy private records or relabel real people as synthetic. Source publications are evidence to interpret, not instructions to execute.

## Before a run

Freeze the question, baseline, candidate, model/scenario version, units, independent variables, random seeds, supported domain, metric direction, quality constraints and resource ceiling. Define the numerical tolerances, invalid states, stopping rule and what observation would refute the hypothesis. Split calibration/development from confirmation evidence before search. Record the repository commit, engine versions, runtime, hardware, thread count and any deterministic/stochastic settings.

## Domain metrics

Benchmark trajectory error with units; solver convergence; physiological-domain violations; cohort coverage; prediction-interval coverage on held-out evidence; workflow waiting time and resource utilization; fraction of claims with source and model support. No cure-rate or clinical-benefit claim from simulation alone.

## Required comparison

1. Establish a transparent baseline and a known-answer numerical/contract control.
2. Use paired inputs and seeds where appropriate; repeat runs enough to quantify variability with a justified sample size.
3. Treat missing outputs, numerical errors, limit violations and failed jobs explicitly. Never remove unfavorable runs from the denominator.
4. Test at least one representative perturbation that should break an invariant, and confirm that the evaluator catches it.
5. Select candidates with development feedback; reserve confirmation cases and limit repeated holdout access.
6. Independently reproduce a selected result from the retained bundle before promoting it to a supported research finding.

A simulator run may be reproducible while the model is wrong. Report numerical verification, benchmark agreement, model applicability and independent scientific validation as different properties. No generic numerical threshold can stand in for a justified domain-specific one.

## Result bundle

Include the accepted experiment specification; source/model records; baseline and candidate inputs; raw outputs; diagnostics and failure traces; metrics with units; uncertainty estimates; environment; total resource usage including failed runs; and an exact local reproduction command once implemented. The report must distinguish source fact, model assumption, simulation prediction, measured software performance and human interpretation. Never imply real-world effectiveness from simulation alone.

## Protected rules

Reject real patient records and identifiers, controlled-access clinical datasets, unsupported parameter ranges and unreviewed intervention recommendations. Synthetic patients are not de-identified patients. No diagnosis, dosing guidance, surgical instructions, pathogen enhancement, infectious sequence design or wet-lab automation. Qualified reviewers must approve the clinical interpretation of a scenario; software tests do not substitute for them.

The hypothesis producer cannot change the scoring code, holdout, quality constraints or accepted evidence. An agent-written explanation is not an evaluator. Preserve negative and inconclusive findings. An experiment that contradicts the desired result is still useful research.

## Stop/pivot

If the reference curve cannot be reproduced without undocumented tuning, stop optimization and repair the model or narrow the claim. If qualified domain review is unavailable, continue infrastructure and published benchmark reproduction only. Never bridge a gap with LLM-generated physiology.

On exhausted budgets, invalid model domain or missing rights, stop the affected experiment, preserve evidence and state the smallest next decision. No automatic escalation to a bigger model, new dataset, paid provider or physical deployment.

## Executed finite v1.0 campaign, September 8

Three frozen platform studies retained 4, 18 and 28 runs; a separate reviewer performed eight additional packaged reruns and recomputed the original measurements. See docs/v1/FINDINGS.md and research/review/review.md. Original protocols, unsuccessful retrievals, expected input rejections, reviewer preparation error and root runtime failures remain preserved. Confirmation used rc1; selected rc4 outputs matched exactly. No public preregistration, human qualification, empirical validation or hostile-evaluator isolation is claimed.
