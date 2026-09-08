#!/usr/bin/env python3
"""Exercise the actual candidate in a new, project-local venv with offline wheels."""
import argparse,csv,hashlib,json,os,platform,shutil,signal,subprocess,sys,time,zipfile
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('output',type=Path);a=p.parse_args();package=a.package.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);ledger=[];begin=time.monotonic()
 manifest=json.loads((package/'PACKAGE-MANIFEST.json').read_text())
 for name,digest in manifest['files'].items():assert sha(package/name)==digest,name
 env={'PATH':os.defpath,'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
 def call(cmd,label,expected=0):
  t=time.monotonic();r=subprocess.run(list(map(str,cmd)),cwd=out,env=env,capture_output=True,text=True,timeout=120)
  ledger.append({'label':label,'command':list(map(str,cmd)),'returncode':r.returncode,'expected':expected,'elapsed_s':time.monotonic()-t,'stdout':r.stdout,'stderr':r.stderr});(out/'commands.json').write_text(json.dumps(ledger,indent=2))
  assert r.returncode==expected,(label,r.stdout,r.stderr)
  return r.stdout
 call([sys.executable,'-m','venv',out/'clean-venv'],'create-clean-venv')
 py=out/'clean-venv/bin/python';app=package/'vital-rehearsal.pyz';base=[py,'-I',app,'research']
 call([py,'-m','pip','install','--no-index','--find-links',package/'wheels','--require-hashes','-r',package/'requirements-lock.txt'],'offline-install')
 assert call([py,'-I',app,'--version'],'version').strip()==manifest['version']
 call(base+['models'],'models')
 call(base+['example','--output',out/'draft.json'],'example')
 call(base+['seal',out/'draft.json','--output',out/'study.json'],'seal')
 call(base+['validate',out/'study.json'],'validate')
 data=json.loads(call(base+['run',out/'study.json','--output',out/'runs'],'model-run'));bundle=Path(data['bundle'])
 assert data['execution_state']=='COMPLETED';assert data['diagnostics']['source_derivative_max_abs_error_mmHg_per_s']>7
 call(base+['inspect',bundle],'inspect')
 call(base+['export',bundle,'--output',out/'export.zip'],'export')
 with zipfile.ZipFile(out/'export.zip') as z:z.extractall(out/'exported')
 call(base+['inspect',out/'exported'],'export-inspect')
 call(base+['example','--model','synthetic-fcfs','--output',out/'queue-draft.json'],'queue-example')
 call(base+['seal',out/'queue-draft.json','--output',out/'queue.json'],'queue-seal')
 q=json.loads(call(base+['run',out/'queue.json','--output',out/'runs'],'queue-run'))
 assert q['metrics']['mean_wait_s']==2.75
 # Supported rejection before an attempt is created.
 bad=json.loads((out/'study.json').read_text());bad['samples']=42;(out/'tampered.json').write_text(json.dumps(bad))
 call(base+['run',out/'tampered.json','--output',out/'rejected-store'],'tampered-seal',2);assert not (out/'rejected-store').exists()
 def spec(name,**settings):
  obj=json.loads((out/'draft.json').read_text());obj.update(settings);f=out/(name+'-draft.json');f.write_text(json.dumps(obj));sealed=out/(name+'.json');call(base+['seal',f,'--output',sealed],name+'-seal');return sealed
 timeout=spec('timeout',timeout_s=.01)
 failed=json.loads(call(base+['run',timeout,'--output',out/'runs'],'timeout',1));assert failed['execution_state']=='TIMED_OUT';call(base+['inspect',failed['bundle']],'timeout-inspect')
 numerical=spec('numerical-failure',solver='source-vode',samples=2,max_step_s=.001)
 failed=json.loads(call(base+['run',numerical,'--output',out/'runs'],'numerical-failure',1));assert failed['execution_state']=='FAILED';assert (Path(failed['bundle'])/'stderr.log').stat().st_size>0
 slow=spec('interrupt',max_step_s=.001)
 for kind,sig in [('graceful',signal.SIGTERM),('hard',signal.SIGKILL)]:
  store=out/kind;log=out/(kind+'.stdout');err=out/(kind+'.stderr')
  with log.open('w') as stdout,err.open('w') as stderr:
   process=subprocess.Popen(list(map(str,base+['run',slow,'--output',store])),cwd=out,env=env,stdout=stdout,stderr=stderr)
   deadline=time.monotonic()+10;partial=None
   while time.monotonic()<deadline:
    candidates=list(store.glob('*/trajectory.csv')) if store.exists() else []
    if candidates:partial=candidates[0].parent;break
    if process.poll() is not None:raise AssertionError('run completed before interruption checkpoint')
    time.sleep(.01)
   assert partial is not None;process.send_signal(sig);code=process.wait(timeout=10)
  ledger.append({'label':kind+'-interrupt','returncode':code,'retained_bundle':str(partial),'signal':sig.value})
  if kind=='graceful':assert json.loads((partial/'result.json').read_text())['execution_state']=='CANCELLED'
  else:
   assert not (partial/'manifest.json').exists()
   # The orphaned finite trusted worker may finish its computation; await its completion marker.
   deadline=time.monotonic()+10
   while not (partial/'worker-result.json').exists() and time.monotonic()<deadline:time.sleep(.02)
   assert (partial/'worker-result.json').exists()
  before={p.name:sha(p) for p in partial.iterdir() if p.is_file()}
  call(base+['list','--output',store],kind+'-list')
  recovered=json.loads(call(base+['recover',partial,'--output',out/'recovered'],kind+'-recover'));assert recovered['execution_state']=='COMPLETED';assert recovered['bundle']!=str(partial)
  assert before=={p.name:sha(p) for p in partial.iterdir() if p.is_file()}
 # Retained original runner reproduces trajectories without imports from checkout.
 rerun=json.loads(call([py,'-I',bundle/'source.pyz','research','run',bundle/'study.json','--output',out/'source-rerun'],'original-source-rerun'))
 assert (Path(rerun['bundle'])/'trajectory.csv').read_bytes()==(bundle/'trajectory.csv').read_bytes()
 corrupt=out/'corrupt';shutil.copytree(bundle,corrupt);(corrupt/'trajectory.csv').write_text('changed\n');call(base+['inspect',corrupt],'tampered-output',2)
 summary={'status':'PASS','scope':'fresh venv, scrubbed environment and isolated Python imports; same host, no container or external human','version':manifest['version'],'application_sha256':sha(app),'platform':platform.platform(),'python':sys.version,'commands':len(ledger),'elapsed_seconds':time.monotonic()-begin,'model_report':str(bundle/'report.html'),'queue_report':str(Path(q['bundle'])/'report.html'),'public_release':'NOT_PERFORMED','human_review':'PENDING'}
 (out/'commands.json').write_text(json.dumps(ledger,indent=2));(out/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
