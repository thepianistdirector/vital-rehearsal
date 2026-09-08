#!/usr/bin/env python3
"""Prepare native draft content from the approved canonical ledger; never calls a service."""
from pathlib import Path
import argparse,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
export=json.loads((ROOT/'plan/roadmap-export.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--base-sha');args=parser.parse_args()
base=args.base_sha or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
release='https://github.com/thepianistdirector/vital-rehearsal/releases/tag/v1.0.0rc4'
wavebyid={w['id']:w for w in export['waves']}
requests=[]
for task in export['tasks']:
 wave=wavebyid[task['wave']]
 body=f"""# {task['id']}: {task['title']}

Stable source key: vital-rehearsal:{task['id']}
Dispatch: tanduna-v1-research-20260908-vital-rehearsal
Canonical source: https://github.com/thepianistdirector/vital-rehearsal/blob/{base}/plan/tasks.json

## Outcome and acceptance
{task['outcome']}

{task['acceptance']}

## Wave and dependencies
Wave {wave['id']}: {wave['name']}
Wave outcome: {wave['outcome']}
Original release horizon: {task['targetRelease']} (preserved planning lineage, not a claim that the current prerelease satisfies all historical acceptance).
Structured prerequisite source keys: {', '.join(task['dependsOn']) or 'none'}.
Textual prerequisites: {'; '.join(task.get('textualPrerequisites',[])) or 'none recorded'}.
Native dependency IDs must come from successful server receipts; repository keys are not platform IDs.
Wave exit evidence: {'; '.join(wave['exitEvidence'])}.

## Current evidence and honest status
Repository evidence status: {task['status']}. This draft does not request or establish native DONE status.
{' ; '.join(task.get('evidence',[])) or 'No execution evidence is recorded for this outcome.'}
The public rc4 prerelease is {release}. It includes an admitted exact-source numerical workbench and three bounded computational drafts. Qualified interpretation review, real external human reproduction and final v1.0 acceptance remain pending. Shared-host agent verification is not human or institutional validation.

## Source history and risks
Source references: {', '.join(task['sourceRefs'])}.
Risk/evidence needs: {'; '.join(task['riskEvidenceNeeds'])}.
All 27 historical identities/acceptances and their mappings remain in plan/lineage and the canonical ledger. The 24 historical aggregate contracts are not duplicated as native tasks; the three foundations occur once as historical documentation evidence.

## Execution boundary
This is a scoped planning draft, not authority to execute a far-future outcome. Before execution, derive a finite packet with exact model/data rights, applicable tests, resources and permissions from this preserved acceptance. Use GPT-6 Astra only unless Lucas explicitly authorizes a different model for that scope; verify actual runtime before any root-only delegation. Do not infer qualified review, spending, patient data, clinical guidance, arbitrary model execution or coupling from a saved task. No new paid resources or participant outreach is authorized. Preserve all original confirmation artifacts and earlier unsuccessful attempts.
"""
 fields={'title':f"{task['id']} — {task['title']}",'goal':task['outcome'],'body':body,'acceptanceCriteria':[task['acceptance']],'repositoryId':None,'baseSha':base,'allowedPaths':task['ownedPaths'],'prohibitedPaths':['.git/','.env','.venv/','research/reproduction/confirmation/','research/robustness/confirmation-20260908/','research/scheduling/confirmation/'],'requiredCommands':[],'networkPolicy':'none','secretScope':[],'maxExecutionPermissions':[],'expectedArtifactType':'Versioned outcome and evidence satisfying the preserved acceptance; executable packet required before work'}
 assert len(fields['title'])<=300 and len(fields['goal'])<=20000 and len(body)<=100000 and len(task['acceptance'])<=2000
 requests.append({'sourceKey':'vital-rehearsal:'+task['id'],'tool':'tanduna.tasks.create','arguments':{'projectSlug':'vital-rehearsal','fields':fields}})
proposal={'projectSlug':'vital-rehearsal','title':'Vital Rehearsal rc4 evidence and the preserved 220-outcome roadmap','body':f"""The owner approved publishing the prepared plan accompanying the explicitly unreviewed rc4 prerelease: {release}.

This proposal preserves the old discussion proposal prp_e78d47cc6b905baa3e96fd4c6ad46f52, its revision and votes. It does not bind expanded content to that historical Yes option. The canonical ledger has 244 records: 27 unchanged historical records plus 217 scoped successors. Native publication selects 220 unique outcomes (217 successors and three foundations) across 28 waves, with structured dependencies, wave outcomes, source lineage, risks, scopes and explicit evidence status.

The finite v1.0 local product and three methodological/engineering drafts have separate automated review and reproducibility evidence. Final public v1.0 acceptance still requires qualified interpretation review and external human reproduction. A saved/submitted/reviewed/accepted/published native plan is not evidence of completed task execution.

Read the canonical plan and all individual task briefs before the exact option is decided. No fabricated votes or native completion states are permitted. The 244-record source ledger and 27-record lineage are linked from https://github.com/thepianistdirector/vital-rehearsal/blob/{base}/plan/tasks.json . Long-term aspirational work does not expand the finite rc4 promise or grant additional resources.
""",'pollOptions':[{'key':'adopt_v1_research_20260908','label':'Adopt the preserved successor plan','explanation':'Publish the reviewed 220-outcome, 28-wave plan with explicit source history, evidence statuses, dependencies and unresolved human gates.','risks':['Saved planning is not proof of implementation or qualified scientific review.','Far-future tasks require separate bounded execution packets and applicable rights/resources.']},{'key':'defer_v1_research_20260908','label':'Defer native plan publication','explanation':'Keep the current discussion and prepared evidence available while requesting specific plan revisions.','risks':['Native task coordination remains unavailable until a plan is actually reviewed and approved.']} ]}
packet={'status':'PREPARED_NOT_SENT','projectSlug':'vital-rehearsal','expectedProjectId':'prj_e6d801111949d9ae4c1ac0d11c6ca463','authorization':'docs/publication/v1/authorization.json','sourceCommit':base,'canonicalExportSha256':hashlib.sha256((ROOT/'plan/roadmap-export.json').read_bytes()).hexdigest(),'counts':export['counts'],'preflight':['Authenticate through the supported user sign-in; never accept pasted credentials.','Call tanduna.projects.search then projects.get; verify account/maintainer role/project id and repository binding.','Read all existing private/public tasks/proposals/plans; reconcile stable source keys before creating anything.','Use returned repositoryId and actual native task/proposal/option/wave IDs; persist each successful receipt before continuing.'],'proposalCreate':proposal,'taskCreateRequests':requests,'canonicalWaves':export['waves'],'canonicalDependencies':export['dependencies'],'planSavePolicy':'Map all source keys to observed native IDs; read get_draft, preserve returned wave IDs and expectedRevision. Never send source keys as platform IDs.','submissionPolicy':'Owner approved this plan publication; freeze only the exact reconciled saved revision. Preserve actual textual-review status, no fabricated vote/decision. Native publication additionally requires passing review and recorded approval of its exact option.','receipts':{'proposalId':None,'repositoryId':None,'taskIdMapping':{},'savedDraftRevision':None,'submissionId':None,'publishedPlanId':None}}
path=ROOT/'docs/publication/v1/tanduna-native-packet.json';path.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'prepared':str(path.relative_to(ROOT)),'tasks':len(requests),'waves':len(export['waves']),'bytes':path.stat().st_size,'no_external_calls':True}))
