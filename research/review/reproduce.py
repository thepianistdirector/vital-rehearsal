#!/usr/bin/env python3
"""Independent bounded review: eight sequential packaged CLI runs; CSV/XML-only checks."""
import argparse,csv,hashlib,json,math,pathlib,subprocess,sys,time,xml.etree.ElementTree as ET,zipfile
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]; R=ROOT/'research'
OLD='bc4043aa8c99b16354dd08aaf595c09a65a7b070be981ba435ba4c41210b2db2'; NEW='2d7f67e808e9cd176d753a49054882091184309586230f3b5a4a617f8e2ab1f9'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.genfromtxt(p,delimiter=',',names=True)
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def table(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);start=time.monotonic();ledger=[];checks=[]
 old=R/'reproduction/platform.pyz';new=ROOT/'dist/vital-rehearsal-1.0.0rc4.pyz';assert sha(old)==OLD and sha(new)==NEW
 put(out/'plan.json',dict(model='gpt-6-astra',runtime_evidence='reviewer turn_context 2026-09-08 session 01a0820e-778a-7b11-a349-1f3f594f1473',old=OLD,new=NEW,planned_runs=8,maximum_runs=10,script_sha256=sha(pathlib.Path(__file__)),python=sys.version,started_unix=time.time()))
 def cli(build,label,*args):
  cmd=[sys.executable,str(build),'research',*map(str,args)];t=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,timeout=125)
  (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr);ledger.append(dict(label=label,command=cmd,returncode=p.returncode,wall_s=time.monotonic()-t));put(out/'commands.json',ledger);assert p.returncode==0,(label,p.stdout,p.stderr);return json.loads(p.stdout)
 # All existing bundle manifests, build identities, seals and retained notices.
 bundles=[]
 for study,base in [('reproduction',R/'reproduction/confirmation'),('robustness',R/'robustness/confirmation-20260908'),('scheduling',R/'scheduling/confirmation')]:
  for m in sorted(base.rglob('manifest.json')):
   b=m.parent;actual={p.name:sha(p) for p in b.iterdir() if p.name!='manifest.json'};assert actual==j(m),str(m)
   assert sha(b/'source.pyz')==OLD
   spec=j(b/'study.json');seal=spec.pop('seal');encoded=(json.dumps(spec,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();assert hashlib.sha256(encoded).hexdigest()==seal
   assert (b/'BENTAL_NOTICE.txt').is_file() and j(b/'result.json')['execution_state']=='COMPLETED';bundles.append(dict(study=study,path=str(b.relative_to(R)),files=len(actual),build=OLD))
 put(out/'original-bundles.json',bundles)
 # Frozen protocol and study checks; detect retrospective edits against retained declarations.
 frozen=[]
 for study,meta in [('robustness',j(R/'robustness/confirmation-20260908/campaign.json')),('scheduling',j(R/'scheduling/confirmation/provenance.json'))]:
  for fn,key in [('protocol.md','protocol_sha256'),('study.py','study_sha256')]:
   actual=sha(R/study/fn);assert actual==meta[key];frozen.append(dict(study=study,file=fn,sha256=actual))
 assert sha(R/'reproduction/protocol.json')=='c06c06960ebaf35df4e2024c42924bca67f37b073c3130b45e1c79df44f0d702'
 put(out/'frozen-checks.json',frozen)
 # Existing study artifact checksum inventories.
 inventories=[]
 for base,manifest in [(R/'reproduction','artifact-manifest.json'),(R/'robustness/confirmation-20260908','sha256.json')]:
  items=j(base/manifest);bad=[p for p,h in items.items() if not (base/p).is_file() or sha(base/p)!=h];inventories.append(dict(manifest=str((base/manifest).relative_to(R)),entries=len(items),mismatches=bad));assert not bad
 put(out/'inventory-checks.json',inventories)
 # Actual distribution runs, no imported platform simulator.
 selected=[('repro-frozen',old,R/'reproduction/confirmation/radau-sealed.json'),('repro-rc4',new,R/'reproduction/confirmation/radau-sealed.json')]
 for i,name in [(0,'control-0.9-Radau'),(3,'control-1.0-Radau'),(6,'control-1.1-Radau')]:selected.append((f'robust-{i}',new,R/f'robustness/confirmation-20260908/{i:02d}-{name}.sealed.json'))
 for name in ['near-1701-d0','near-1701-d1','heldout-idle-ascii']:selected.append((name,new,R/f'scheduling/confirmation/{name}.sealed.json'))
 reruns=[]
 for label,build,spec in selected:
  d=cli(build,label+'-run','run',spec,'--output',out/label);b=pathlib.Path(d['bundle']);cli(build,label+'-inspect','inspect',b);reruns.append((label,b,spec))
 # Compare all numerical trajectories/schedules to original matched immutable specifications.
 comparisons=[]
 for label,b,spec in reruns:
  oldb=next(R/x['path'] for x in bundles if j(R/x['path']/'study.json')==j(spec));fn='trajectory.csv' if (b/'trajectory.csv').exists() else 'schedule.csv'
  if fn=='trajectory.csv':
   x,y=arr(b/fn),arr(oldb/fn)
   for n in x.dtype.names:
    delta=float(np.max(np.abs(x[n]-y[n])));assert delta==0;comparisons.append(dict(case=label,observable=n,max_absolute_delta=delta,byte_identical=(b/fn).read_bytes()==(oldb/fn).read_bytes()))
  else:
   assert (b/fn).read_bytes()==(oldb/fn).read_bytes();comparisons.append(dict(case=label,observable='complete schedule',max_absolute_delta=0,byte_identical=True))
 table(out/'rerun-comparisons.csv',comparisons)
 # Recompute every original robustness state envelope, effects and refinement, without study analyzer.
 rb=R/'robustness/confirmation-20260908';data={}
 for i,s in enumerate(j(rb/'campaign.json')['specs']):data[i]=arr(next((rb/f'{i:02d}-{s[0]}-attempts').glob('*/trajectory.csv')))
 state_rows=[];thresholds=dict(V_A=1e-6,P_A=1e-4,f_o=1e-7,f_c=1e-7,p_o=1e-4,p_c=1e-4,z=1e-8)
 for n,threshold in thresholds.items():
  widths={r:float(np.max(np.max([data[k][n] for k in ids],axis=0)-np.min([data[k][n] for k in ids],axis=0))) for r,ids in [(0.9,[0,1,2]),(1.,[3,4,5]),(1.1,[6,7,8])]}
  refine=float(np.max(abs(data[17][n]-data[3][n])))
  for r,k in [(.9,0),(1.1,6)]:
   effect=float(np.max(abs(data[k][n]-data[3][n])));ratio=effect/(widths[1.]+widths[r]);assert max(widths.values())<threshold and refine<threshold and ratio>10
   state_rows.append(dict(state=n,R=r,max_effect=effect,final_effect=float(data[k][n][-1]-data[3][n][-1]),combined_width=widths[1.]+widths[r],effect_ratio=ratio,refinement=refine,threshold=threshold))
 table(out/'independent-state-effects.csv',state_rows)
 # All 28 original queues checked by a fresh completion-history scan, unlike heap or workload vector.
 queue_rows=[]
 for x in bundles:
  if x['study']!='scheduling':continue
  b=R/x['path'];s=j(b/'study.json');rows=list(csv.DictReader((b/'schedule.csv').open()));last=[0.]*s['servers'];wait=[];max_error=0.
  for job,row in zip(sorted(s['jobs'],key=lambda x:(x['arrival_s'],x['id'])),rows):
   chosen=sorted(range(len(last)),key=lambda k:(last[k],k))[0];st=max(job['arrival_s'],last[chosen]);end=st+job['service_s']+s['service_delay_s'];w=st-job['arrival_s'];assert row['id']==job['id'] and int(row['server'])==chosen
   err=max(abs(float(row[k])-v) for k,v in [('start_s',st),('finish_s',end),('wait_s',w)]);assert err<1e-8;max_error=max(max_error,err);last[chosen]=end;wait.append(w)
  assert len(rows)==len(s['jobs']);m=j(b/'result.json')['metrics'];assert abs(m['mean_wait_s']-sum(wait)/len(wait))<1e-8
  queue_rows.append(dict(bundle=x['path'],jobs=len(rows),max_error=max_error,mean_wait=sum(wait)/len(wait),p95_wait=sorted(wait)[math.ceil(.95*len(wait))-1],makespan=max(last)))
 table(out/'independent-queue-checks.csv',queue_rows)
 # XML MathML numeric evaluator, not a copied generated helper. Unit-bearing constants treated in declared source-unit magnitudes.
 xml=ET.parse(R/'reproduction/sources/model.cellml');ns={'c':'http://www.cellml.org/cellml/1.0#','m':'http://www.w3.org/1998/Math/MathML'};component=xml.find("c:component[@name='PluralPressureFunction']",ns);assert component is not None
 env={v.attrib['name']:float(v.attrib['initial_value']) for v in component.findall('c:variable',ns) if 'initial_value' in v.attrib}
 def evaluate(node):
  tag=node.tag.split('}')[-1]
  if tag=='cn':return float(node.text)
  if tag=='ci':return env[node.text.strip()]
  if tag=='pi':return math.pi
  op=node[0].tag.split('}')[-1];v=[evaluate(n) for n in node[1:]]
  if op=='times':return math.prod(v)
  if op=='divide':return v[0]/v[1]
  if op=='minus':return -v[0] if len(v)==1 else v[0]-v[1]
  if op=='power':return v[0]**v[1]
  if op=='sin':return math.sin(v[0])
  if op=='cos':return math.cos(v[0])
  raise ValueError(op)
 equations={e[1].text.strip():e[2] for e in component.find('m:math',ns)};env['R']=evaluate(equations['R']);al=arr(reruns[0][1]/'algebraic.csv');audit=[]
 for t in al['time_s']:
  env['time']=float(t);p=evaluate(equations['P_L']);encoded=evaluate(equations['dP_Ldt']);om=env['omega'];vt=env['V_T'];E=env['E'];deriv=-env['R']*om**2*vt/2*math.cos(om*t)-E*vt*om/2*math.sin(om*t)
  env['time']=float(t)+1e-4;pplus=evaluate(equations['P_L']);env['time']=float(t)-1e-4;pminus=evaluate(equations['P_L']);fd=(pplus-pminus)/2e-4
  audit.append(dict(time_s=float(t),xml_pressure=p,xml_derivative=encoded,analytic_derivative=deriv,residual=encoded-deriv,finite_difference_error=fd-deriv))
 assert max(abs(r['xml_pressure']-float(al['P_L_mmHg'][i])) for i,r in enumerate(audit))<1e-10
 assert max(abs(r['xml_derivative']-float(al['dP_Ldt_source_mmHg_per_s'][i])) for i,r in enumerate(audit))<1e-10
 assert max(abs(r['finite_difference_error']) for r in audit)<1e-6
 table(out/'xml-pressure-audit.csv',audit)
 # Archive source compatibility: numerical code unchanged; retain exact textual diffs for adapters/report.
 import difflib
 with zipfile.ZipFile(old) as za,zipfile.ZipFile(new) as zb:
  for name in ['vital_rehearsal/bental_source.py','vital_rehearsal/scheduler.py']:assert za.read(name)==zb.read(name)
  diffs=[]
  for name in ['vital_rehearsal/research_model.py','vital_rehearsal/research.py']:
   diffs.extend(difflib.unified_diff(za.read(name).decode().splitlines(True),zb.read(name).decode().splitlines(True),fromfile='rc1/'+name,tofile='rc4/'+name))
  (out/'build-source.diff').write_text(''.join(diffs))
 put(out/'summary.json',dict(run_calls=len(reruns),cli_calls=len(ledger),original_bundles=len(bundles),all_checks='PASS',max_derivative_identity_error=max(abs(r['residual']) for r in audit),max_fd_error=max(abs(r['finite_difference_error']) for r in audit),minimum_effect_ratio=min(r['effect_ratio'] for r in state_rows),wall_s=time.monotonic()-start))
 put(out/'sha256.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()})
 print((out/'summary.json').read_text())
if __name__=='__main__':main()
