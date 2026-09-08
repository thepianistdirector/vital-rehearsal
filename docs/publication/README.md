# Public plan and release publication audit

Status: **public reads verified; no publication performed**. Observed September 7,
2026, 23:10–23:12 UTC. This report records publication preparation, not product
implementation, scientific approval, reviewer acceptance or release completion.

## Verified public state

The [campaign](https://tanduna.com/projects/vital-rehearsal) and workspace identify
Vital Rehearsal as public project `prj_e6d801111949d9ae4c1ac0d11c6ca463`, slug
`vital-rehearsal`, linked to
[thepianistdirector/vital-rehearsal](https://github.com/thepianistdirector/vital-rehearsal).
The identifier was read from the server-rendered campaign data, not derived from
the slug. The saved Tanduna repository identifier was not exposed in the inspected
campaign record and remains unresolved.

| Public surface | Observed state |
| --- | --- |
| [Native tasks](https://tanduna.com/p/vital-rehearsal/tasks) | 0 tasks; empty list; no next page |
| [Native roadmap](https://tanduna.com/projects/vital-rehearsal/roadmap) | No published plan; no waves or pagination |
| [Proposals](https://tanduna.com/p/vital-rehearsal/proposals) | 1 proposal; its complete linked record was read; no next page |
| [Tanduna releases](https://tanduna.com/p/vital-rehearsal/releases) | 0 releases |
| [GitHub releases API](https://api.github.com/repos/thepianistdirector/vital-rehearsal/releases?per_page=100) | HTTP 200, empty array, no pagination Link header |

The [existing proposal](https://tanduna.com/p/vital-rehearsal/proposals/prp_e78d47cc6b905baa3e96fd4c6ad46f52)
is `prp_e78d47cc6b905baa3e96fd4c6ad46f52`, revision 1, **DISCUSSION**. Its
eight-wave direction refers to 24 draft repository tasks and requires task-level
preparation/review. It explicitly withholds execution, spending and deployment
authority. Its Yes/No options have zero ballots, no opened vote, no approved
alternative and no associated plan. Current owner authorization enables the
new local work; it does not turn that historical discussion into an accepted
platform decision. Leave this proposal and all historical acceptance intact.

The complete [frozen repository ledger](https://github.com/thepianistdirector/vital-rehearsal/blob/9fa99f392c93f6f1e33a2cd85b9348cb68afe39e/plan/tasks.json)
was freshly retrieved. Its 27 identities comprise 3 DONE documentation/tooling
foundations and 24 PLANNED outcomes. All original platform task IDs remain null:
repository IDs are not evidence of saved Tanduna tasks. The existing proposal is
a separate lineage record, not another implementation task. The canonical
successor mapping belongs in `plan/tasks.json` and generated exports; this audit
does not create a second task-status ledger.

## Supported native route and its limits

The official [MCP reference](https://tanduna.com/docs#mcp),
[review checklist](https://tanduna.com/guide/task-review-checklist), and
[voting guide](https://tanduna.com/guide/how-voting-works) describe a supported
draft → submitted immutable plan → textual review → explicit decision route.
See [manual/import procedure](manual-publication.md) for the concrete mapping.

`tanduna.tasks.create` saves an unpublished maintainer draft. It does not expose a
completion-status argument. `tanduna.task_plans.save_draft` records ordered waves,
selected task IDs and dependency links but does not publish. The current schema
permits at most 32 named waves, each with a name of at most 80 characters and up
to 1,000 selected task IDs. There are at most 1,000 dependency **rows**, each
containing up to 1,000 prerequisite IDs; this is not a 1,000-edge total limit.
Published plans are independently ordered per poll, not one global wave registry.

`tanduna.task_plans.submit_draft` freezes the saved revision and requires explicit
agreement. A real passing review and recorded approval of the exact bound poll
alternative are both necessary. Textual review does not attest product QA or
execution. The documented public MCP list has no maintainer poll-decision method;
recording that decision uses the authorized web workflow. An open vote, a vote
tally, a saved draft, or a pending submission never establishes publication.

## Remaining capability and authority gates

No Tanduna tool is callable in this task's available tool registry. The public
[connection guide](https://tanduna.com/guide/connect-through-mcp) documents a local
sign-in helper and short-lived authenticated client session; direct Codex MCP
OAuth is listed as unavailable. No helper was downloaded/executed, no account
configuration was changed, and no credentials were accessed or requested. An
anonymous GET to the documented MCP endpoint returned 405 (method unsupported),
which is **not** evidence that an authenticated MCP call succeeds or fails.

An authorized maintainer must use an existing suitable authenticated session or
complete the supported sign-in personally. The exact account, project editing
authority, saved repository ID, unpublished drafts, reviewer availability and
decision controls must then be read and verified. Public reads cannot rule out
private drafts. Concrete prepared content and the precise destination/action
must be authorized before external writes. No new credentials, broader access,
shared-host changes or publication approval are implied by this report.

There is no actual public 0.1 access path yet. The public GitHub repository is a
source destination, not a verified runnable release. The release gate still
requires an admitted lawful model, candidate verification, qualified/human
evidence, exact release authority, public read-back and reproduction from the
publicly obtained artifact. Do not advertise unreleased commands as working
0.1 instructions. Publication-ready access text must be populated from actual
release evidence when that gate passes.

## Evidence boundaries

[sources.json](sources.json) records source URLs, retrieval times, HTTP status and
SHA-256 of the retrieved bytes; [live-state-2026-09-07.json](live-state-2026-09-07.json)
contains the exact observed identities and null unknowns. All network requests
were anonymous read-only HTTPS GETs. Project-scoped cache snapshots support this
audit and are not intended for redistribution: the pages may also render unrelated
project navigation. Only relevant facts are transcribed here.

The web browsing tool rejected these Tanduna pages as unsafe to open; ordinary
anonymous HTTPS retrieval succeeded. This report relies on the retrieved HTML
and its server-rendered data, not on a fabricated browser or authenticated session.
No messages, votes, proposals, native tasks, commits or releases were created by
this audit. Re-read live public and authenticated state immediately before any
later publication, since these observations are time-bound.
