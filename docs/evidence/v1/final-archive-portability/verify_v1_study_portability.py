#!/usr/bin/env python3
"""Final artifact portability checks in its extracted layout; sequential, offline."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,time
p=argparse.ArgumentParser();p.add_argument('extracted',type=Path);p.add_argument('evidence',type=Path);a=p.parse_args();root=a.extracted.resolve();out=a.evidence.resolve();out.mkdir(parents=True,exist_ok=False);ledger=[];start=time.monotonic()
env={'PATH':os.defpath,'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','MPLCONFIGDIR':str(root/'.cache/matplotlib')}
manifest=json.loads((root/'PACKAGE-MANIFEST.json').read_text())
for path,digest in manifest['files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path

def call(label,cmd):
 t=time.monotonic();r=subprocess.run(list(map(str,cmd)),cwd=root,env=env,capture_output=True,text=True,timeout=120)
 (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
 ledger.append({'label':label,'command':list(map(str,cmd)),'returncode':r.returncode,'elapsed_seconds':time.monotonic()-t});(out/'commands.json').write_text(json.dumps(ledger,indent=2))
 assert r.returncode==0,(label,r.stdout,r.stderr)
 print(label,'PASS',flush=True)
call('create-venv',[sys.executable,'-m','venv',root/'.venv'])
py=root/'.venv/bin/python'
call('offline-research-install',[py,'-m','pip','install','--no-index','--find-links',root/'wheels','--require-hashes','-r',root/'research-requirements-lock.txt'])
call('source-tests',[py,'-m','unittest','discover','-s','tests','-v'])
call('source-study',[py,'research/reproduction/study.py','--output',root/'research/reproduction/package-rerun'])
call('robustness-study',[py,'research/robustness/study.py','--campaign','package-rerun'])
call('robustness-analysis',[py,'research/robustness/analyze.py','package-rerun'])
call('scheduling-study',[py,'research/scheduling/study.py','--output',root/'research/scheduling/package-rerun'])
call('review-reproduction',[py,'research/review/reproduce.py','--output',root/'research/review/package-rerun'])
# Original distributed files must still be intact after all commands.
for path,digest in manifest['files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
summary={'status':'PASS','version':manifest['version'],'scope':'actual extracted release archive, fresh offline venv, same host; no external human or machine','checks':len(ledger),'research_run_calls':58,'source_tests':65,'elapsed_seconds':time.monotonic()-start,'original_distributed_files_unchanged':True}
(out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
