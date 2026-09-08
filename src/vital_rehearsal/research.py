"""Versioned research CLI. Seals bind intent; manifests detect changes, not authenticity."""
import argparse
import csv
import hashlib
import html
import importlib.resources as resources
import json
import math
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
import uuid
import zipfile
from . import __version__
from .contracts import canonical_json, read_json, read_regular, ContractError
from .research_model import card, MODEL, source_hash

SCHEMA='vital-research/1'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(path,value):
    with path.open('xb') as stream:stream.write(canonical_json(value))
def example(model):
    base={'schema':SCHEMA,'model':model,'time_unit':'second','timeout_s':60}
    if model==MODEL:base.update(source_sha256=source_hash(),solver='Radau',rtol=1e-8,atol=1e-10,max_step_s=0.05,duration_s=10.,samples=500,resistance_scale=1.)
    else:base.update(servers=1,service_delay_s=0.,jobs=[{'id':f'job-{i:04d}','arrival_s':float(i),'service_s':1.5} for i in range(12)])
    return base

def number(x,lo,hi):
    if type(x) not in (int,float) or not math.isfinite(x) or not lo<=x<=hi:raise ContractError(f'number outside supported [{lo}, {hi}]')
def validate(spec,sealed=True):
    if not isinstance(spec,dict):raise ContractError('spec must be an object')
    obj=dict(spec);seal=obj.pop('seal',None)
    if sealed and seal!=sha(canonical_json(obj)):raise ContractError('missing or changed immutable seal; seal a new experiment')
    if obj.get('schema')!=SCHEMA or obj.get('time_unit')!='second':raise ContractError('unsupported schema or time unit')
    model=obj.get('model')
    if model not in (MODEL,'synthetic-fcfs'):raise ContractError('unsupported model; arbitrary code and coupling are prohibited')
    if set(obj)!=set(example(model)):raise ContractError('unknown or missing fields')
    number(obj['timeout_s'],0.01,120)
    if model==MODEL:
        if obj['source_sha256']!=source_hash():raise ContractError('model source identity mismatch')
        if obj['solver'] not in card()['solver_methods']:raise ContractError('unsupported solver')
        for key,lo,hi in [('rtol',1e-11,1e-3),('atol',1e-13,1e-3),('max_step_s',0.001,1),('duration_s',0.01,10),('resistance_scale',0.9,1.1)]:number(obj[key],lo,hi)
        if type(obj['samples'])!=int or not 2<=obj['samples']<=2001:raise ContractError('samples must be 2..2001')
    else:
        if type(obj['servers'])!=int or not 1<=obj['servers']<=16:raise ContractError('servers must be 1..16')
        number(obj['service_delay_s'],0,100)
        jobs=obj['jobs']
        if not isinstance(jobs,list) or not 1<=len(jobs)<=10000:raise ContractError('jobs must contain 1..10000 entries')
        ids=set()
        for job in jobs:
            if not isinstance(job,dict) or set(job)!={'id','arrival_s','service_s'}:raise ContractError('job fields invalid')
            if not isinstance(job['id'],str) or not job['id'].isascii() or not job['id'].replace('-','').replace('_','').isalnum() or len(job['id'])>64 or job['id'] in ids:raise ContractError('job id invalid or duplicate')
            ids.add(job['id']);number(job['arrival_s'],0,1e6);number(job['service_s'],0.001,10000)
    return obj

def manifest(directory):
    entries=list(directory.iterdir())
    if any(p.is_symlink() or not p.is_file() for p in entries):raise ContractError('bundle must contain regular files only')
    return {p.name:sha(read_regular(p,32*1024*1024)) for p in sorted(entries) if p.name!='manifest.json'}
def inspect(directory):
    expected=read_json(directory/'manifest.json')
    if expected!=manifest(directory):raise ContractError('bundle integrity mismatch')
    spec=read_json(directory/'study.json')
    obj=dict(spec); seal=obj.pop('seal',None)
    if seal!=sha(canonical_json(obj)):raise ContractError('bundle study seal mismatch')
    return read_json(directory/'result.json')
def render(directory,result,spec):
    esc=lambda x:html.escape(str(x))
    table=''
    if 'comparison' in result:
        table='<h2>Source-default solver comparison</h2><p>Shared equations; this comparator is numerical evidence. Each observable retains its own units. On a narrow screen, scroll the table horizontally.</p><div class="scroll" tabindex="0" role="region" aria-label="Observable comparison table"><table><caption>Candidate versus source VODE</caption><thead><tr><th scope="col">Observable</th><th scope="col">Unit</th><th scope="col">Maximum absolute difference</th><th scope="col">Final value</th></tr></thead><tbody>'
        for n,v in result['comparison'].items():table+=f'<tr><th scope="row">{esc(n)}</th><td>{esc(v["unit"])}</td><td>{v["max_absolute_difference"]:.6g}</td><td>{v["final"]:.6g}</td></tr>'
        table+='</tbody></table></div>'
    conclusion_label={'NUMERICAL_OUTPUT_WITH_SOURCE_WARNINGS':'Numerical result · source warnings','SYNTHETIC_SCHEDULE_ONLY':'Synthetic schedule · no physiology coupling','NO_SCIENTIFIC_RESULT':'Incomplete attempt · no scientific result'}.get(result['conclusion'],result['conclusion'])
    links=' '.join(f'<a href="{p.name}">{esc(p.name)}</a>' for p in sorted(directory.iterdir()) if p.name in ['trajectory.csv','reference.csv','algebraic.csv','schedule.csv','study.json','result.json','source.pyz','model-card.json','BENTAL_NOTICE.txt'])
    doc=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vital Rehearsal · research report</title><style>
    :root{{color-scheme:light}}body{{font:17px/1.6 system-ui,sans-serif;color:#172f36;background:#f3f6f3;margin:0}}main{{max-width:1040px;margin:auto;padding:32px 24px}}header{{border-bottom:2px solid #245e62}}h1{{font-size:clamp(2rem,6vw,3.5rem);line-height:1.1}}h2{{margin-top:2rem}}.label{{font-size:13px;letter-spacing:.12em;text-transform:uppercase}}.notice{{overflow-wrap:anywhere;padding:20px;background:#fff1d2;border-left:5px solid #986400;margin:24px 0}}section{{padding:16px 0}}a{{color:#125465;margin-right:18px;display:inline-block;padding:5px 0}}a:focus-visible,summary:focus-visible,.scroll:focus-visible{{outline:3px solid #a34b00;outline-offset:3px}}table{{border-collapse:collapse;width:100%;background:white}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #ccd7d4}}.scroll{{overflow:auto}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#e3ece7;padding:18px;font-size:13px}}.id{{overflow-wrap:anywhere}}.skip{{position:absolute;left:24px;top:-80px;background:white;padding:8px}}.skip:focus{{top:0}}@media print{{body{{background:white}}main{{max-width:none}}details{{display:block}}}}</style>
    <a class="skip" href="#evidence">Skip to evidence</a><main><header><p class="label">Vital Rehearsal / {esc(__version__)} / research workbench</p><h1>Inspect the evidence.</h1><p>{esc(spec['model'])}</p></header><div class="notice"><strong>{esc(conclusion_label)}</strong><p>{esc(result.get('limitation','Incomplete attempt; no scientific conclusion.'))}</p></div>
    <p class="id">Experiment seal: {esc(spec['seal'])}</p><p>Execution: <strong>{esc(result['execution_state'])}</strong> · Qualified interpretation review: pending</p>{table}<h2 id="evidence" tabindex="-1">Diagnostics and measurements</h2><pre>{esc(json.dumps(result.get('diagnostics',result.get('metrics',result)),indent=2))}</pre><h2>Reproduce and export</h2><p>Retain this complete folder. Inspect its manifest using the CLI. Rerun study.json into a new store with the retained source.pyz and the documented dependencies. Use your browser’s Print action for a PDF.</p><nav aria-label="Evidence files">{links}</nav><details><summary>Full result and measured costs</summary><pre>{esc(json.dumps(result,indent=2))}</pre></details><details><summary>Immutable experiment settings</summary><pre>{esc(json.dumps(spec,indent=2))}</pre></details><p>Hashes detect changes relative to the manifest; they do not establish authorship. No patient records or clinical recommendations.</p></main></html>'''
    (directory/'report.html').write_text(doc)

def worker(directory):
    spec=read_json(directory/'study.json');validate(spec)
    import resource
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(120,120))
    signal.alarm(math.ceil(spec['timeout_s'])+2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024*1024,32*1024*1024))
    if spec['model']==MODEL:
        from .research_model import solve
    else:from .scheduler import solve
    result=solve(spec,directory)
    write(directory/'worker-result.json',result)
    return 0

def run(spec,output):
    validate(spec)
    from .packaging import archive_bytes
    output.mkdir(parents=True,exist_ok=True)
    directory=output/uuid.uuid4().hex;directory.mkdir()
    write(directory/'study.json',spec)
    write(directory/'model-card.json',card() if spec['model']==MODEL else {'model':'synthetic-fcfs','license':'AGPL-3.0-or-later','order':'jobs: arrival then ASCII id; server: earliest prior finish time then server id','coupling':'NONE'})
    payload=archive_bytes();(directory/'source.pyz').write_bytes(payload)
    for name in ['LICENSE','BENTAL_NOTICE.txt']:(directory/name).write_bytes(resources.files('vital_rehearsal').joinpath(name).read_bytes())
    runtime={'version':__version__,'python':sys.version,'platform':platform.platform(),'source_archive_sha256':sha(payload),'started_unix':time.time(),'isolation':'second process, same host; artifact access is a workflow convention'}
    try:
        import numpy,scipy
        runtime.update(numpy=numpy.__version__,scipy=scipy.__version__)
    except ImportError:pass
    write(directory/'runtime.json',runtime)
    start=time.monotonic();process=None
    result={'execution_state':'FAILED','conclusion':'NO_SCIENTIFIC_RESULT'}
    previous=signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        env={'PATH':os.defpath,'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONHASHSEED':'0'}
        with (directory/'stdout.log').open('xb') as out,(directory/'stderr.log').open('xb') as err:
            process=subprocess.Popen([sys.executable,'-I',str((directory/'source.pyz').resolve()),'research','_worker',str(directory.resolve())],stdout=out,stderr=err,env=env)
            try:code=process.wait(timeout=spec['timeout_s'])
            except subprocess.TimeoutExpired:
                process.kill();process.wait();result['execution_state']='TIMED_OUT';code=None
            if code==0:result=read_json(directory/'worker-result.json')
            elif code is not None:result['worker_exit_code']=code
    except KeyboardInterrupt:
        if process is not None:process.kill();process.wait()
        result['execution_state']='CANCELLED'
    except OSError as exc:result['error']=str(exc)
    finally:signal.signal(signal.SIGTERM,previous)
    result.update(attempt_id=directory.name,total_wall_seconds=time.monotonic()-start)
    write(directory/'result.json',result);render(directory,result,spec);write(directory/'manifest.json',manifest(directory))
    return directory,result

def main(argv):
    parser=argparse.ArgumentParser(prog='vital-rehearsal research',description='Bounded source-model and synthetic-process research; no clinical interpretation.')
    subs=parser.add_subparsers(dest='command',required=True)
    subs.add_parser('models')
    p=subs.add_parser('example');p.add_argument('--model',choices=[MODEL,'synthetic-fcfs'],default=MODEL);p.add_argument('--output',type=Path,required=True)
    for c in ['seal','validate','run']:
        p=subs.add_parser(c);p.add_argument('study',type=Path)
        if c in ['seal','run']:p.add_argument('--output',type=Path,required=True)
    for c in ['inspect','export','_worker']:
        p=subs.add_parser(c);p.add_argument('bundle',type=Path)
        if c=='export':p.add_argument('--output',type=Path,required=True)
    p=subs.add_parser('list');p.add_argument('--output',type=Path,required=True)
    p=subs.add_parser('recover');p.add_argument('bundle',type=Path);p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='models':result={'models':[card(),{'id':'synthetic-fcfs','coupling':'NONE'}]}
        elif args.command=='example':write(args.output,example(args.model));result={'written':str(args.output),'next':'edit then seal'}
        elif args.command=='seal':
            obj=validate(read_json(args.study),False);obj['seal']=sha(canonical_json(obj));write(args.output,obj);result={'seal':obj['seal']}
        elif args.command=='validate':validate(read_json(args.study));result={'state':'VALID'}
        elif args.command=='_worker':return worker(args.bundle)
        elif args.command=='run':
            directory,result=run(read_json(args.study),args.output);result={'bundle':str(directory),**result}
            print(json.dumps(result,indent=2,allow_nan=False));return 0 if result['execution_state']=='COMPLETED' else 1
        elif args.command=='recover':
            spec=read_json(args.bundle/'study.json');validate(spec)
            directory,result=run(spec,args.output)
            result={'bundle':str(directory),'original_preserved':str(args.bundle),**result}
            print(json.dumps(result,indent=2,allow_nan=False));return 0 if result['execution_state']=='COMPLETED' else 1
        elif args.command=='inspect':result={'integrity':'VERIFIED','authenticity':'NOT_ESTABLISHED','result':inspect(args.bundle)}
        elif args.command=='list':result={'attempts':[{'directory':str(p),'state':read_json(p/'result.json')['execution_state'] if (p/'result.json').exists() else 'INTERRUPTED_UNFINALIZED'} for p in sorted(args.output.iterdir()) if p.is_dir()]}
        elif args.command=='export':
            inspect(args.bundle)
            with zipfile.ZipFile(args.output,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for p in sorted(args.bundle.iterdir()):
                    if p.is_file():z.write(p,p.name)
            result={'export':str(args.output),'sha256':sha(args.output.read_bytes())}
        print(json.dumps(result,indent=2,allow_nan=False));return 0
    except (ContractError,ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'state':'REJECTED_OR_FAILED','reason':str(exc)}));return 2
