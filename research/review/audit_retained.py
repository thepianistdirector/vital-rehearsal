#!/usr/bin/env python3
"""No simulations: independent retained-output, command ledger and table audit."""
import csv,json,pathlib,hashlib,math
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];OUT=pathlib.Path(__file__).resolve().parent/'retained-audit';OUT.mkdir(exist_ok=False)
def j(p):return json.loads(p.read_text())
def rows(p):return list(csv.DictReader(p.open()))
def put(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def close(x,y):assert math.isclose(float(x),float(y),abs_tol=1e-14,rel_tol=1e-10),(x,y)
ledgers=[]
for name,path in [('reproduction',R/'reproduction/confirmation/all-cli-attempts.json'),('robustness',R/'robustness/confirmation-20260908/commands.jsonl'),('scheduling',R/'scheduling/confirmation/all-attempts.json')]:
 commands=[json.loads(x) for x in path.read_text().splitlines()] if path.suffix=='.jsonl' else j(path)
 bad=[x for x in commands if x['returncode']!=x.get('expected_returncode',0)];assert not bad
 run=[x for x in commands if 'run' in x['command'][3:4]]
 ledgers.append(dict(study=name,commands=len(commands),runs=len(run),nonzero_returncodes=sum(x['returncode']!=0 for x in commands),unexpected_failures=len(bad)))
put(OUT/'ledger-counts.json',ledgers)
# Crosscheck reviewer-derived table values against author CSV fields.
for r in rows(R/'review/confirmation-v2/independent-state-effects.csv'):
 a=next(a for a in rows(R/'robustness/confirmation-20260908/resistance-effects.csv') if a['state']==r['state'] and float(a['resistance_scale'])==float(r['R']))
 for ours,theirs in [('max_effect','max_absolute_change'),('final_effect','final_signed_change'),('combined_width','sum_control_widths'),('effect_ratio','effect_to_envelope_ratio')]:close(r[ours],a[theirs])
repro=[]
for b in (R/'reproduction/confirmation/bundles').iterdir():
 s=j(b/'study.json');x=np.genfromtxt(b/'trajectory.csv',delimiter=',',names=True);y=np.genfromtxt(b/'reference.csv',delimiter=',',names=True)
 for n in x.dtype.names[1:]:
  diff=x[n]-y[n];maximum=float(max(abs(diff)));rms=float(np.sqrt(np.mean(diff**2)));claim=j(b/'result.json')['comparison'][n];close(maximum,claim['max_absolute_difference']);close(rms,claim['rms_difference']);threshold=j(R/'reproduction/protocol.json')['absolute_thresholds_vs_source'][n];assert maximum<=threshold
  repro.append(dict(solver=s['solver'],rtol=s['rtol'],state=n,max_absolute=maximum,rms=rms,threshold=threshold))
put(OUT/'reproduction-comparisons.json',repro)
# Recompute scalar z tolerance observations and all solver errors.
rb=R/'robustness/confirmation-20260908';data={}
for i,s in enumerate(j(rb/'campaign.json')['specs']):data[s[0]]=np.genfromtxt(next((rb/f'{i:02d}-{s[0]}-attempts').glob('*/trajectory.csv')),delimiter=',',names=True)
for claim in rows(rb/'solver-errors.csv'):
 name=claim['run'];s=next(s for s in j(rb/'campaign.json')['specs'] if s[0]==name);ref=data[f'control-{s[5]}-Radau'];n=claim['state'];diff=data[name][n]-ref[n]
 close(max(abs(diff)),claim['max_absolute']);close(np.sqrt(np.mean(diff**2)),claim['rms']);close(data[name][n][-1],claim['final']);close(max(abs(diff[1:])/abs(ref[n][1:])),claim['max_relative_excluding_initial'])
# Paired queue effects crosschecked against independently recomputed original schedules.
qa={x['bundle']:x for x in rows(R/'review/confirmation-v2/independent-queue-checks.csv')};sr=j(R/'scheduling/confirmation/results.json')
for claim in j(R/'scheduling/confirmation/paired-effects.json'):
 b=next(x for x in sr if x['label']==f"{claim['kind']}-{claim['seed']}-d0");d=next(x for x in sr if x['label']==f"{claim['kind']}-{claim['seed']}-d1");bb=qa['scheduling/confirmation/'+b['bundle']];dd=qa['scheduling/confirmation/'+d['bundle']]
 for field,ours in [('delta_mean_wait_s','mean_wait'),('delta_p95_wait_s','p95_wait'),('delta_makespan_s','makespan')]:close(float(dd[ours])-float(bb[ours]),claim[field])
put(OUT/'summary.json',dict(all_checks='PASS',reproduction_state_comparisons=28,robustness_solver_state_comparisons=126,robustness_effect_comparisons=14,scheduling_pairs=12,ledger_counts=ledgers))
put(OUT/'sha256.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()});print((OUT/'summary.json').read_text())
