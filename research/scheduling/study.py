#!/usr/bin/env python3
"""Original AGPL-3.0-or-later finite scheduling study. Run from any cwd.
Default execution writes a fresh evidence directory. --output must not exist.
"""
import argparse,csv,hashlib,json,math,platform,random,statistics,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).parent/'confirmation');p.add_argument('--platform',type=Path,default=ROOT/'dist/vital-rehearsal-1.0.0rc1-investigation.pyz');p.add_argument('--python',type=Path,default=ROOT/'.venv/bin/python');a=p.parse_args()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);archive=a.platform.resolve();build=digest(archive);begin=time.monotonic();inventory=[];rows=[];run_count=0
 put(out/'provenance.json',dict(build_sha256=build,build=str(archive),python=str(a.python),driver_python=sys.version,host=platform.platform(),protocol_sha256=digest(Path(__file__).with_name('protocol.md')),study_sha256=digest(Path(__file__)),started_unix=time.time(),model_verified='gpt-6-astra',rights='Original synthetic inputs and analysis; AGPL-3.0-or-later'))
 def cli(label,*args,expected=0):
  nonlocal run_count
  if args[0]=='run':
   run_count+=1;assert run_count<=32
  assert digest(archive)==build,'Build changed during confirmation'
  assert time.monotonic()-begin<900,'15 minute deadline exceeded'
  cmd=[str(a.python),str(archive),'research',*map(str,args)];t=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True)
  entry=dict(index=len(inventory)+1,label=label,command=cmd,returncode=r.returncode,expected_returncode=expected,wall_seconds=time.monotonic()-t,stdout=r.stdout,stderr=r.stderr)
  inventory.append(entry);put(out/'all-attempts.json',inventory)
  assert r.returncode==expected,(label,r.stdout,r.stderr)
  return json.loads(r.stdout),entry['wall_seconds']
 template,_=cli('example','example','--model','synthetic-fcfs','--output',out/'draft.json');base=json.loads((out/'draft.json').read_text())
 def jobs_for(kind,seed):
  rng=random.Random(seed);n=800;c=1 if kind in ('low','near','over') else 4;rho=dict(low=.5,near=.95,over=1.1,multi=.95,burst=.7,hetero=.7)[kind]
  if kind=='burst':services=[10.]*n;arrivals=[(i//40)*40*10/(c*rho) for i in range(n)]
  elif kind=='hetero':
   services=[2.]*640+[42.]*160;rng.shuffle(services);arrivals=[i*10/(c*rho) for i in range(n)]
  else:
   services=[rng.uniform(8,12) for _ in range(n)];services=[x*10/statistics.mean(services) for x in services]
   gaps=[rng.uniform(.8,1.2) for _ in range(n-1)];scale=10/(c*rho)/statistics.mean(gaps);arrivals=[0.]
   for gap in gaps:arrivals.append(arrivals[-1]+gap*scale)
  jobs=[dict(id=f'job-{i:04d}',arrival_s=t,service_s=s) for i,(t,s) in enumerate(zip(arrivals,services))];rng.shuffle(jobs)
  return c,rho,jobs
 def close(x,y):assert math.isclose(x,y,abs_tol=1e-8,rel_tol=1e-12),(x,y)
 def verify(spec,bundle,result):
  data=list(csv.DictReader((bundle/'schedule.csv').open()));jobs=sorted(spec['jobs'],key=lambda j:(j['arrival_s'],j['id']));assert len(data)==len(jobs)
  # Workload-vector recurrence, no heap and no import from platform source.
  workloads=[0.]*spec['servers'];prior_arrival=0.;finishes=[0.]*spec['servers'];waits=[];events=[];busy=0.;lindley=0.;last_service=0.;last_arrival=0.
  for idx,(j,r) in enumerate(zip(jobs,data)):
   assert j['id']==r['id'];arrival=j['arrival_s'];duration=j['service_s']+spec['service_delay_s']
   workloads=sorted(max(0.,w-(arrival-prior_arrival)) for w in workloads);wait=workloads[0];start=arrival+wait;finish=start+duration
   workloads[0]+=duration;workloads.sort();prior_arrival=arrival
   server=int(r['server']);expect_server=min(range(spec['servers']),key=lambda s:(finishes[s],s));assert server==expect_server
   actual={k:float(r[k]) for k in ('arrival_s','start_s','finish_s','wait_s')}
   for k,v in dict(arrival_s=arrival,start_s=start,finish_s=finish,wait_s=wait).items():close(actual[k],v)
   assert actual['start_s']>=finishes[server]-1e-8;assert actual['wait_s']>=0.;close(actual['finish_s']-actual['start_s'],duration);finishes[server]=actual['finish_s'];busy+=duration;waits.append(actual['wait_s'])
   events.extend([(arrival,1),(actual['start_s'],-1)])
   if spec['servers']==1:
    lindley=0. if idx==0 else max(0.,lindley+last_service-(arrival-last_arrival));close(lindley,actual['wait_s']);last_service=duration;last_arrival=arrival
  depth=0;area=0.;last=0.
  for t,delta in sorted(events):area+=depth*(t-last);depth+=delta;last=t
  close(area,sum(waits));assert depth==0
  metrics=result['metrics'];close(metrics['mean_wait_s'],statistics.mean(waits));close(metrics['max_wait_s'],max(waits));close(metrics['makespan_s'],max(finishes));assert metrics['jobs']==len(jobs)
  # Numeric round-trip through a second CSV serialization.
  import io
  stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data);assert list(csv.DictReader(io.StringIO(stream.getvalue())))==data
  return dict(mean_wait_s=statistics.mean(waits),p95_wait_s=sorted(waits)[math.ceil(.95*len(waits))-1],max_wait_s=max(waits),makespan_s=max(finishes),busy_work_s=busy,queue_area_job_s=area,realized_utilization=busy/(spec['servers']*max(finishes)),all_checks='PASS')
 def execute(label,c,jobs,delay,**meta):
  spec=dict(base,servers=c,jobs=jobs,service_delay_s=delay);draft=out/(label+'.draft.json');sealed=out/(label+'.sealed.json');put(draft,spec)
  cli(label+' seal','seal',draft,'--output',sealed);r,cost=cli(label+' run','run',sealed,'--output',out/'attempts');bundle=Path(r['bundle']);ins,_=cli(label+' inspect','inspect',bundle);assert ins['integrity']=='VERIFIED'
  measured=verify(spec,bundle,r);entry=dict(label=label,servers=c,jobs=len(jobs),delay_s=delay,bundle=str(bundle.relative_to(out)),cli_wall_s=cost,worker_wall_s=r['total_wall_seconds'],artifact_bytes=sum(x.stat().st_size for x in bundle.iterdir() if x.is_file()),**meta,**measured);rows.append(entry);put(out/'results.json',rows);return bundle
 cases={}
 for kind in ('low','near','over','multi','burst','hetero'):
  for seed in (1701,2903):
   c,rho,jobs=jobs_for(kind,seed)
   for delay in (0.,1.):cases[(kind,seed,delay)]=execute(f'{kind}-{seed}-d{int(delay)}',c,jobs,delay,kind=kind,seed=seed,nominal_load=rho*(1+delay/10))
 c,rho,jobs=jobs_for('low',1701);b=execute('heldout-permutation',c,list(reversed(jobs)),0.,kind='heldout',seed=0,nominal_load=rho);assert (b/'schedule.csv').read_bytes()==(cases[('low',1701,0.)]/'schedule.csv').read_bytes()
 execute('heldout-sixteen-ties',16,[dict(id=f'Z-{i:02}',arrival_s=0.,service_s=.001) for i in reversed(range(32))],0.,kind='heldout',seed=0,nominal_load=None)
 execute('heldout-boundaries',1,[dict(id='a',arrival_s=0.,service_s=.001),dict(id='b',arrival_s=0.,service_s=10000.),dict(id='c',arrival_s=1e6,service_s=.001)],100.,kind='heldout',seed=0,nominal_load=None)
 execute('heldout-idle-ascii',2,[dict(id='a',arrival_s=0.,service_s=1.),dict(id='A',arrival_s=0.,service_s=2.),dict(id='later',arrival_s=10.,service_s=1.)],0.,kind='heldout',seed=0,nominal_load=None)
 for label,jobs in [('duplicate',[dict(id='x',arrival_s=0.,service_s=1.)]*2),('nonascii',[dict(id='ñ',arrival_s=0.,service_s=1.)])]:
  draft=out/(label+'.invalid.json');put(draft,dict(base,jobs=jobs));cli(label+' rejection','seal',draft,'--output',out/(label+'.must-not-exist.json'),expected=2)
 tampered=json.loads((out/'low-1701-d0.sealed.json').read_text());tampered['service_delay_s']=1.;put(out/'tampered.json',tampered);cli('seal tamper rejection','validate',out/'tampered.json',expected=2)
 pairs=[]
 for kind in ('low','near','over','multi','burst','hetero'):
  for seed in (1701,2903):
   b=next(x for x in rows if x.get('kind')==kind and x['seed']==seed and x['delay_s']==0);d=next(x for x in rows if x.get('kind')==kind and x['seed']==seed and x['delay_s']==1)
   pairs.append(dict(kind=kind,seed=seed,baseline_mean_wait_s=b['mean_wait_s'],delayed_mean_wait_s=d['mean_wait_s'],delta_mean_wait_s=d['mean_wait_s']-b['mean_wait_s'],delta_p95_wait_s=d['p95_wait_s']-b['p95_wait_s'],delta_max_wait_s=d['max_wait_s']-b['max_wait_s'],delta_makespan_s=d['makespan_s']-b['makespan_s']))
 for name,data in [('summary',rows),('paired-effects',pairs)]:
  keys=list(dict.fromkeys(k for row in data for k in row));f=(out/(name+'.csv')).open('w',newline='');w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(data);f.close()
 put(out/'paired-effects.json',pairs);put(out/'costs.json',dict(total_driver_wall_s=time.monotonic()-begin,run_calls=run_count,command_calls=len(inventory),expected_rejections=3,artifact_bytes=sum(x.stat().st_size for x in out.rglob('*') if x.is_file()),sum_cli_run_wall_s=sum(x['cli_wall_s'] for x in rows),sum_worker_wall_s=sum(x['worker_wall_s'] for x in rows)))
 # Standalone quantitative SVG (no image editing or external rendering dependency).
 maxval=max(x['delta_mean_wait_s'] for x in pairs);svg=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="620" viewBox="0 0 960 620"><rect width="960" height="620" fill="#fafaf7"/><g font-family="sans-serif" fill="#183a40"><text x="32" y="38" font-size="24">One added service second: finite mean-wait amplification</text><text x="32" y="66" font-size="14">800 original synthetic jobs; paired delay 0 → 1 s; seeds 1701 / 2903</text>']
 for i,x in enumerate(pairs):
  y=102+i*37;w=x['delta_mean_wait_s']/maxval*620;svg.append(f'<text x="25" y="{y+17}" font-size="13">{x["kind"]} · {x["seed"]}</text><rect x="160" y="{y}" width="{w:.3f}" height="25" fill="{["#237b83","#e48b44"][i%2]}"/><text x="{170+w:.3f}" y="{y+17}" font-size="13">{x["delta_mean_wait_s"]:.2f} s</text>')
 svg.append('<text x="32" y="586" font-size="13">Descriptive finite cases only. Burst seeds duplicate the same workload. No clinical interpretation.</text></g></svg>');(out/'effects.svg').write_text(''.join(svg));print(json.dumps(dict(output=str(out),runs=run_count,all_checks='PASS'),indent=2))
if __name__=='__main__':main()
