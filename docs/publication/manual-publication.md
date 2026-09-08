# Native publication procedure and import requirements

Status: **prepared procedure; not executed**. This is a manual/MCP mapping contract,
not an undocumented bulk-import endpoint. The canonical long-term ledger and its
generated export remain authoritative for content. The owner reviews the final
concrete export, count, scope, action and destination before external submission.

## Preserve identity and history

1. Re-read the public campaign, every tasks/proposals page, every relevant full
   brief and the roadmap. Authenticate through an existing authorized session;
   use `tanduna.projects.get` with `projectSlug: "vital-rehearsal"` and verify the
   observed project ID against `prj_e6d801111949d9ae4c1ac0d11c6ca463`. Read tasks,
   proposals, saved draft plans and requirements. Reconcile additions and changes.
2. Preserve the old eight-wave discussion proposal at revision 1. Recommend a
   **new** proposal that clearly describes the successor plan and references the
   old proposal and all 27 source identities. This is a proposed publication
   choice, not authorization to create or vote on it. Do not bind a larger new
   programme to the old Yes alternative without an explicit scope decision.
3. Keep all 27 original acceptance contracts and predecessor links in lineage.
   Publish successor outcomes once; do not also publish the 24 expanded originals
   as duplicate work. Preserve the 3 completed foundation outcomes as historical
   documentation evidence. A new native draft cannot inherit a fabricated DONE
   status from repository prose; use a verified supported status workflow if
   available and otherwise show the distinction visibly in its body.
4. Keep a durable receipt mapping for each source key, successor key and returned
   platform task ID, revision, proposal ID, option key, wave ID and publication ID.
   All unknown platform identifiers start null. Never substitute local IDs for
   server-issued IDs. Freeze the canonical export digest in the receipt.

## Native task field mapping

The documented `tanduna.tasks.create` request has `projectSlug` and `fields`; all
fields below are required by its schema. Each created record is an unpublished
draft. The source is the [official MCP schema](https://tanduna.com/docs#mcp).

| Native field | Canonical/manual material |
| --- | --- |
| `title` | Stable project-scoped successor ID plus outcome title, at most 300 characters |
| `goal` | User/system outcome, at most 20,000 characters |
| `body` | Complete instructions, outcome provenance, source IDs/revisions, source acceptance links, wave/order/outcome/exit evidence, release horizon, structured and textual prerequisites separately, risks, evidence/status, limits, scope and current execution-packet gate; at most 100,000 characters |
| `acceptanceCriteria` | At least one falsifiable criterion, each at most 2,000 characters |
| `repositoryId` | Actual repository ID returned by authenticated project metadata; null while unresolved, never the project ID |
| `baseSha` | Actual reviewed immutable source commit for the saved scope, or null while unresolved |
| `allowedPaths`, `prohibitedPaths` | Repository-relative owned paths and explicit exclusions from the approved execution packet; preserve historical owned paths in lineage separately |
| `requiredCommands` | Commands proven to exist and discover meaningful checks; use explicit manual acceptance in body when appropriate, not invented commands |
| `networkPolicy` | `none`, `restricted`, or `full`, chosen for the actual bounded work; do not infer unrestricted rights from source research needs |
| `secretScope`, `maxExecutionPermissions` | Explicit granted scopes only; otherwise empty arrays, never embedded secrets |
| `expectedArtifactType` | Concrete expected deliverable, or null if unresolved |

Do not falsely turn a high-level far-future outcome into an execution-ready packet.
Record unresolved choices and the requirement for a later maintainer-approved
packet. Model requirements use the supported requirements controls when permitted;
the explicit GPT-6 Astra policy must be preserved. A saved requested model is not
attestation of the actual model that executed work.

The task-creation API does not document an idempotency key. Persist each successful
receipt before proceeding. If a response is lost, list/read tasks and compare the
stable source key and full saved content before retrying. A duplicate or ambiguous
match requires reconciliation, not another blind create. `tasks.update` replaces
the complete revision fields; use the last read `expectedRevision`. Submitted or
published records are immutable: corrections require a new draft and lineage.

## Native wave/dependency mapping

Read `tanduna.task_plans.get_draft` for the chosen actual proposal. Save through
`tanduna.task_plans.save_draft` with the last saved `expectedRevision`, or null only
when no draft exists. Its `plan` contains:

- `optionKey`: null during preparation, then the actual saved option key chosen
  explicitly for this plan before submission.
- `waves`: ordered `{name, taskIds}` objects; omit `id` for new waves, preserve
  server-issued `id` when revising an editable draft. At most 32 waves, 80
  characters per name, and 1,000 unique task IDs per wave.
- `unassignedTaskIds`: explicit ordered unassigned IDs, at most 1,000. Prefer no
  unassigned tasks for this wave-based programme.
- `dependencies`: at most 1,000 rows of `{taskId, dependsOnTaskIds}` using selected
  actual native task IDs; each prerequisite array has at most 1,000 unique IDs.

The source's 27 outcome waves plus one historical foundation wave fit the 32-wave
limit. The native draft schema has no separate wave outcome, release horizon,
exit-evidence or source-lineage fields: retain those in the proposal and relevant
task bodies as well as the canonical export. Do not submit unknown extra fields.
Check the exact generated names against 80 characters. Validate duplicate outcome
elimination, task counts, ordering, missing mappings, dependency coverage, dangling
IDs, cycles, release consistency and all schema size limits before saving.

On a revision conflict, read the complete saved draft and reconcile before a new
save. Read back the saved task fields and ordered plan against the exact canonical
export; no guessed IDs or unresolved receipt substitutions may reach submission.

## Review, explicit decision and public verification

Obtain agreement to freeze the **exact saved draft revision**. Then the documented
`tanduna.task_plans.submit_draft` takes `projectSlug`, `proposalId`, and
`expectedDraftRevision`. Read its actual result. A disabled reviewer or pending
review stays pending. A changes-requested result needs corrected new draft content
and review while preserving the frozen record. A technical failure uses the
supported retry path; do not invent a passing review.

The [voting guide](https://tanduna.com/guide/how-voting-works) separates tally from
maintainer decision. Opening voting freezes roster/weights and is irreversible;
use only exact existing authorization for that action. Never cast fabricated
votes. An authorized maintainer records approval of the exact bound alternative
through the supported web decision flow; no such decision method is listed in the
current public MCP tools. Publication requires both the actual passing review and
this recorded decision. Neither alone is sufficient.

Read `tanduna.task_plans.list_published`, following `nextCursor` with the same limit
(1–25); a cursor reset means the first page restarted and requires deduplication.
Verify returned immutable publication IDs, proposal/option/review bindings, waves,
ordering, counts and links. Read the public roadmap and tasks without developer
credentials, including every page and full relevant brief. Confirm release horizon,
honest evidence status, source lineage and working actual 0.1 access instructions.
Update the canonical receipt mapping only from actual returned records. Retain
partial successes and failures for reconciliation. A GitHub link, draft collection
or unaccepted proposal cannot be counted as native plan publication.

## Concrete permission packet to complete later

Before the remaining publication decision, attach the final canonical export and
digest, exact task/wave counts, immutable source base, complete proposed content,
destination project/proposal choice, intended account/role, action sequence,
scope/cost/data exposure, irreversible freeze/vote implications, receipt strategy
and still-open product gates. Name the actual release URL/version and tested
obtain → validate → execute → evaluate → inspect/recover instructions only after
that release exists. Preserve the honest absence of 0.1 access in a planning-only
publication. The full Goal still requires the eventual real release and read-back.
