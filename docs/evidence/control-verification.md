# Local software-control evidence

Date: 2026-09-07. Scope: original software and evidence tooling; no physiological model, scientific result or public 0.1 release.

## Implemented behavior

The fixed CPython 3.12/Linux CLI validates a closed study schema, exact quantities/units and model/source/criterion identity. It runs only the packaged integer-identity control in a separate trusted process, copies evaluator-owned criteria/reference into the attempt before execution, evaluates every expected sample with bounded exact-decimal parsing, and finalizes a unique JSON/CSV/HTML bundle atomically. Source-file fingerprints, Python/OS/architecture identity, wall/CPU use and explicitly scoped child RSS records accompany raw output and diagnostics. No dependency, network, GPU, plugin, patient record or user-defined physiological variation is needed.

Each run reserves its own attempt. Graceful interruption finalizes `CANCELLED`; hard interruption leaves a separately listed incomplete directory. The worker's own alarm bounds its life even if the parent is killed. Earlier completed bundles remain untouched. Failure classes cannot carry an agreement conclusion. Rejected studies are not persisted; sanitized errors avoid echoing arbitrary input text.

## Observed automated evidence

The root ran 8 contract, 6 evaluator, 11 attempt/recovery and 4 CLI/package tests after the three critic findings were fixed (29 control tests). These tests exercise duplicate/unknown fields, malformed units, Boolean/nonfinite/rounded/underflowed input, external adapter selection, missing/perturbed/nonfinite/impossible trajectories, source criteria changes, manifest tampering and FIFO paths, real process crash/nonconvergence/timeout, SIGTERM/SIGKILL, unique reruns and same-build zipapp execution/inspection. Individual targeted runs passed; the final integrated plan-plus-control run is recorded in STATUS when performed.

The control reference gives exact agreement. Perturbing the counter at t=2 from 2 to 2.25 gives `COMPLETED` execution and `CONTRADICTED` comparison, with exact error `0.25`. Wrong units, truncated/nonfinite/impossible output give invalid evidence. Injected nonconvergence is `FAILED_NUMERICAL`, process failure is `FAILED_SYSTEM`, and the injected pause is `TIMED_OUT`. These are software fault injections, not observed physiology behavior.

## Unsuccessful evidence retained

- Initial run `0b784466362342fbb73b6f53dc96bd7a` failed under a 256 MiB address-space limit. The installed standalone Python reserved approximately 255 MiB of virtual memory before the control started; it used approximately 12.4 MiB resident memory in the measurement. The bound was adjusted to 512 MiB virtual address space, without an allocation or shared-host change. The initial failed bundle remains in ignored `runs/control/`; its original traceback contains local development paths and is excluded from any distributable example. Later worker failures emit sanitized exception classes.
- An initial false-success mutation test failed: a rehashed failed bundle could carry an agreement conclusion. Root fixed the terminal-state/evaluation cross-check and retained this test failure in the task's execution record.
- The fresh-context [software critic](../review/control-critic.md) reproduced three additional defects despite the initial 26 passing tests: exact-number loss through float parsing, FIFO manifest blocking, and conflicting fault provenance. Root fixed all three and added regression assertions. The critic report describes its pre-remediation snapshot rather than silently replacing failed evidence.
- The first narrow report clipped its six-column comparison. The next variant wrapped the result word. The final three-column variant keeps the status unbroken. Original screenshots remain alongside the revised evidence.

## Visual and interaction checks

An existing Chromium 140.0.7339.186 rendered the offline report with a project-local profile and default browser sandbox. Missing shared libraries were supplied only through verified official RPM contents extracted into ignored project cache; no installation script or shared configuration ran. The development browser uses a private debugging pipe, opens no listening port, and blocks external report requests. Node/Chromium are not CLI dependencies.

The [final phone report](visual-control-v3/report-phone.png) and [desktop report](visual-control-v3/report-desktop.png) were captured and visually inspected. Automated checks cover phone layout, visible keyboard focus and skip link, CSS zoom, relative evidence files, text status, table headers, no animation and no external requests. Narrow layout/reflow checks follow the concerns described in [W3C's reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html); this is limited software evidence, not a declaration of WCAG conformance. The [browser record](visual-control-v3/browser-check.json) states the actual observations and remaining manual checks.

A separate [fresh-context image critic](../review/report-critic.md) reviewed anonymous matched 390×1500 PNG captures with no text/EXIF metadata. It preferred the revised report because the per-observable result remained visible. Original source mapping and scientific scope were retained in [comparison provenance](visual-comparison-provenance.json). This visual preference does not establish accessibility, scientific validity or user acceptance.

## Evidence levels that remain open

Packaged local software runtime is distinct from external reproduction. Tests inside a clean project-scoped directory on this same host are not another machine or a human researcher. Lucas answered that no qualified reviewer or independent researcher is available for now. Physiology admission, source trajectory/reuse rights, any numerical dependency approval, real qualified review, independent public-artifact use, public GitHub release and accepted native Tanduna plan remain separate unfinished gates.
