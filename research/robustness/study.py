#!/usr/bin/env python3
"""Run the predeclared sequential platform campaign; preserve every attempt."""
import argparse,datetime,hashlib,json,os,pathlib,subprocess,time
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument('--campaign',default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')); a=p.parse_args()
 out=HERE/a.campaign; out.mkdir(exist_ok=False)
 py=ROOT/'.venv/bin/python'; build=ROOT/'dist/vital-rehearsal-1.0.0rc1-investigation.pyz'
 base=json.loads((ROOT/'scenarios/bental-baseline.json').read_text());base.pop('seal');base.update(samples=2001)
 specs=[]
 for r in [.9,1.,1.1]:
  for solver in ['Radau','BDF','DOP853']: specs.append((f'control-{r}-{solver}',solver,1e-11,1e-13,.01,r))
 specs += [('baseline','Radau',1e-8,1e-10,.05,1.)]
 specs += [(f'atol-{atol}','Radau',1e-8,atol,1.,1.) for atol in [1e-3,1e-6,1e-10,1e-13]]
 specs += [('source-default','source-vode',1e-6,1e-6,1.,1.),('source-tight','source-vode',1e-11,1e-13,.01,1.),('RK45','RK45',1e-8,1e-10,.05,1.),('refinement','Radau',1e-11,1e-13,.005,1.)]
 meta={'protocol_sha256':digest(HERE/'protocol.md'),'study_sha256':digest(pathlib.Path(__file__)),'build_sha256':digest(build),'model':'gpt-6-astra','specs':specs,'started':datetime.datetime.now(datetime.timezone.utc).isoformat()};(out/'campaign.json').write_text(json.dumps(meta,indent=2))
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 def command(args,label):
  cmd=[str(py),str(build),'research',*map(str,args)];t=time.perf_counter();r=subprocess.run(cmd,cwd=HERE,env=env,capture_output=True,text=True); dt=time.perf_counter()-t
  (out/f'{label}.stdout').write_text(r.stdout);(out/f'{label}.stderr').write_text(r.stderr)
  with (out/'commands.jsonl').open('a') as f:f.write(json.dumps({'command':cmd,'returncode':r.returncode,'elapsed_s':dt})+'\n')
  return r
 command(['models'],'models')
 for i,(name,solver,rtol,atol,step,rscale) in enumerate(specs):
  s=base|dict(solver=solver,rtol=rtol,atol=atol,max_step_s=step,resistance_scale=rscale)
  raw=out/f'{i:02d}-{name}.json';sealed=out/f'{i:02d}-{name}.sealed.json';raw.write_text(json.dumps(s,indent=2))
  if command(['seal',raw,'--output',sealed],f'{i:02d}-seal').returncode:continue
  r=command(['run',sealed,'--output',out/f'{i:02d}-{name}-attempts'],f'{i:02d}-run');print(i,name,r.returncode,flush=True)
 print(out)
if __name__=='__main__':main()
