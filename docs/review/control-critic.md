# Software-control critic review

Reviewed 2026-09-07 by a fresh-context GPT-6 Astra leaf critic. Scope: the local standard-library control implementation, CLI/zipapp packaging, four control test modules, fixed scenario and decision 0001. This is software review only: no physiology model is admitted, no qualified physiology review was performed, and this report supplies neither independent human reproduction nor release approval.

This report records the source before root remediation. Line references below refer to that reviewed snapshot; the root is addressing findings separately. Production source and tests were read-only to the critic.

## Findings

### P2 — Exact control comparisons silently accept rounded or underflowed inputs

Locations: `src/vital_rehearsal/contracts.py:47` and `src/vital_rehearsal/evaluation.py:29`.

JSON's default float parsing and CSV `float(cell)` erase distinctions before the fixed-value, time-grid and domain checks. A counter of `-1e-9999` at time zero becomes negative zero, passes the declared `[0,4]` domain and receives `CONTROL_AGREEMENT`. A study whose start value is `-1e-9999` is likewise accepted and normalized to zero. These are not numerically identical literals, although `validate_study` explicitly promises semantic normalization only. Ordinary producer output does not trigger this, but the evaluator's invalidity boundary and closed input contract do.

Reproduced from the project root with `src` on Python's module path:

```python
from vital_rehearsal import builtin
from vital_rehearsal.contracts import canonical_json, decode_json, validate_study
from vital_rehearsal.evaluation import evaluate
raw = canonical_json(builtin.study()).replace(b'"value": 0', b'"value": -1e-9999')
assert validate_study(decode_json(raw))["conditions"]["start"]["value"] == 0
diagnostics = dict(schema_version=1, model_id=builtin.CONTROL_ID,
    solver="integer-enumeration", solver_version="1", state="COMPLETED",
    samples=5, fault="none")
result = evaluate(builtin.REFERENCE_CSV.replace("0,0", "0,-1e-9999").encode(),
    diagnostics, builtin.REFERENCE_CSV.encode(), builtin.criteria())
assert result["conclusion"] == "CONTROL_AGREEMENT"
```

Recommendation: preserve exact numeric meaning until contract, domain and equality checks finish; bound numeric complexity as well as document size. Add coverage for underflow and values that round onto a supported integer.

### P2 — A FIFO manifest blocks inspection before regular-file validation

Location: `src/vital_rehearsal/attempts.py:243`; underlying reader `contracts.py:59`.

Artifact reads generally use `_bounded_bytes`, which checks regular-file and symlink status. The manifest is instead opened directly through `read_json`. A directory containing a FIFO named `manifest.json` makes `inspect` block indefinitely waiting for a writer. `list-attempts` also reaches this path for a UUID-named finalized directory. The 1 MiB limit bounds bytes only after opening; it does not bound this wait. Study JSON has the same reader issue.

Bounded reproduction: create `runs/critic/fifo-bundle/manifest.json` using `os.mkfifo`; launch `[sys.executable, '-B', 'vital-rehearsal', 'inspect', absolute_bundle_path]` with `subprocess.Popen`; `communicate(timeout=0.5)` raises `TimeoutExpired`. The critic killed and reaped this process. No unbounded reproduction was left running.

Recommendation: route all input files, including manifests, through regular-file reads that cannot block on a FIFO; use descriptor-based type checks and no-follow/nonblocking opening where supported, rather than a check/open race. Verify both `inspect` and `list-attempts` fail promptly.

### P2 — Inspection accepts contradictory fault provenance

Location: `src/vital_rehearsal/attempts.py:290` and independent reevaluation at line 303.

Inspection cross-checks invocation and result fault labels but never compares them with the adapter's diagnostics fault. In a successful `none` bundle, changing both `invocation.json` and `result.json` to `control_fault: "crash"`, then updating the manifest's file hashes, passes `verify_bundle`. The returned result claims `crash` and `CONTROL_AGREEMENT`, while retained diagnostics claim `none`. This concerns internal consistency of the retained evidence, not an expectation of authentication from a self-contained manifest.

Reproduction retained under `runs/critic/fault-consistency/`: run the normal control, modify only those two fault fields, regenerate each manifest file's byte count and SHA-256, then call `verify_bundle`. Observed output: `crash CONTROL_AGREEMENT`, diagnostics fault `none`.

Recommendation: validate fault labels against the supported registry and cross-check diagnostic fault with invocation/result whenever diagnostics are present; ensure unsupported diagnostic/execution combinations cannot be verified.

## Verification and rubric coverage

All 26 tests from `test_contracts`, `test_evaluation`, `test_attempts` and `test_cli` passed in 7.200 seconds on CPython 3.12.14 Linux. The test helper's temporary directory was redirected in memory to `runs/critic`; no test source changed. The two independently generated zipapps had identical SHA-256 `f0b4157075a66751b1b289a6d44c3e5783e809cb8db781903bd969317610edbc` and their isolated execution/inspection test passed. This digest identifies that test build, not a subsequently remediated build.

| Rubric | Evidence and assessment |
| --- | --- |
| Closed schema, units, nonfinite rejection | Fixed study comparison, duplicate-key/nonfinite/depth/size rejection, unknown-field and unit tests inspected and passed. Exact-number defect above remains in reviewed snapshot. |
| Evaluator independence and invalidity | Producer enumerates values without importing reference/criteria. Evaluator owns literal reference and rejects changed criteria/reference, wrong units, missing samples and invalid diagnostics. Exact parsing defect affects invalidity honesty. |
| Failure retention, interruption, no overwrite, containment | Real crash/nonconvergence/timeout/SIGTERM/SIGKILL tests passed. Unique attempt reservation, exclusive artifact creation and partial-state handling inspected. Resource limits and worker alarm are explicitly trusted-code hygiene, not OS isolation. No adversarial third-party adapter execution is claimed or tested. FIFO read defect affects inspection bounds. |
| Integrity, provenance, portable packaging | Hash mismatch, traversal, artifact symlink and false failed-run agreement checks passed. Same-build source identity and deterministic zipapp round trip passed. Fault provenance mismatch above is reproducible. Portability evidence is limited to the declared CPython 3.12 Linux environment. |
| Scope and claim honesty | Model card, CLI, report and decision consistently label the counter as software-only, distinguish completion from agreement and state missing physiology/human review. No invented scientific validation found. |
| Maintainability | Small modules separate contract, producer, evaluator, durable orchestration, rendering and CLI. Standard-library implementation and fixed registry keep scope reviewable. No consequential design finding beyond the defects above; no stylistic nits reported. |

No network, dependencies, external publication, delegation or scientific review was used. Critic findings are actionable software observations; remediation and final gate decisions remain with the root.
