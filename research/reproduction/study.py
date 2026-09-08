#!/usr/bin/env python3
"""Rerun four frozen platform experiments; independently audit exported outputs.
Usage: ../../.venv/bin/python study.py --output confirmation
No model integration occurs in this analysis script.
"""
import argparse,csv,hashlib,json,math,os,platform,subprocess,sys,time,zipfile
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',default='confirmation');a=p.parse_args()
out=Path(a.output).resolve();out.mkdir(exist_ok=False,parents=True)
protocol=json.loads((BASE/'protocol.json').read_text());archive=BASE/'platform.pyz'
for frozen_file,expected in [('platform.pyz','bc4043aa8c99b16354dd08aaf595c09a65a7b070be981ba435ba4c41210b2db2'),('protocol.json','c06c06960ebaf35df4e2024c42924bca67f37b073c3130b45e1c79df44f0d702')]:
    if hashlib.sha256((BASE/frozen_file).read_bytes()).hexdigest()!=expected:raise RuntimeError('Frozen input hash changed: '+frozen_file)
logs=[];runs=[];start=time.monotonic()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def cli(*args):
    cmd=[sys.executable,str(archive),'research',*map(str,args)];t=time.monotonic()
    result=subprocess.run(cmd,capture_output=True,text=True)
    logs.append(dict(command=cmd,returncode=result.returncode,wall_seconds=time.monotonic()-t,stdout=result.stdout,stderr=result.stderr))
    dump(out/'all-cli-attempts.json',logs)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    return json.loads(result.stdout)
cli('models');cli('example','--output',out/'example.json')
base=json.loads((out/'example.json').read_text())
for case in protocol['scenarios']:
    spec=base|protocol['fixed']|{k:v for k,v in case.items() if k!='name'}
    draft=out/(case['name']+'-draft.json');sealed=out/(case['name']+'-sealed.json');dump(draft,spec)
    cli('seal',draft,'--output',sealed)
    result=cli('run',sealed,'--output',out/'bundles');bundle=Path(result['bundle'])
    cli('inspect',bundle);cli('export',bundle,'--output',out/(case['name']+'.zip'))
    runs.append(dict(name=case['name'],bundle=str(bundle),result=result))
dump(out/'run-inventory.json',runs)
load=lambda path:np.genfromtxt(path,delimiter=',',names=True)
arrays={r['name']:load(Path(r['bundle'])/'trajectory.csv') for r in runs}
rows=[]
for r in runs:
    candidate=arrays[r['name']];reference=load(Path(r['bundle'])/'reference.csv')
    for name,threshold in protocol['absolute_thresholds_vs_source'].items():
        err=candidate[name]-reference[name]
        rows.append([r['name'],name,float(np.max(abs(err))),float(np.sqrt(np.mean(err**2))),threshold,bool(np.max(abs(err))<=threshold),r['result']['comparison'][name]['unit']])
with (out/'comparisons.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['case','observable','max_abs','rms','threshold','within_threshold','source_unit']);w.writerows(rows)
convergence=[]
for name,threshold in protocol['absolute_thresholds_vs_source'].items():
    convergence.append(dict(observable=name,radau_refinement=float(max(abs(arrays['radau'][name]-arrays['radau-tight'][name]))),tight_cross_algorithm=float(max(abs(arrays['bdf-tight'][name]-arrays['radau-tight'][name]))),threshold=threshold*.1))
dump(out/'convergence.json',convergence)
algebraic=load(Path(runs[0]['bundle'])/'algebraic.csv');t=algebraic['time_s']
# Independently transcribed XML PluralPressureFunction. Numeric magnitudes in source units.
R=2*math.pi/5;omega=1.256637;VT=.41;E=2.5;Pm=760
pressure=lambda t:Pm-R*omega*VT/2*np.sin(omega*t)-E*(2.5-VT/2*np.cos(omega*t))
derivative=-R*omega**2*VT/2*np.cos(omega*t)-E*VT*omega/2*np.sin(omega*t)
h=1e-4;fd=(pressure(t+h)-pressure(t-h))/(2*h)
source=algebraic['dP_Ldt_source_mmHg_per_s'];error=source-derivative
with (out/'independent-pressure-audit.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['time_s','pressure_mmHg','source_derivative_mmHg_s','independent_derivative_mmHg_s','centered_difference_mmHg_s','signed_error_mmHg_s']);w.writerows(zip(t,pressure(t),source,derivative,fd,error))
summary=dict(pressure_export_max_error=float(max(abs(pressure(t)-algebraic['P_L_mmHg']))),analytic_export_max_error=float(max(abs(derivative-algebraic['dP_Ldt_analytic_mmHg_per_s']))),finite_difference_max_error=float(max(abs(fd-derivative))),source_derivative_max_error=float(max(abs(error))),source_derivative_rms_error=float(np.sqrt(np.mean(error**2))),signed_error_mean=float(np.mean(error)),signed_error_min=float(min(error)),signed_error_max=float(max(error)),continuous_signed_error_bounds=[-E*2.5-E*VT*(1+omega)/2,-E*2.5+E*VT*(1+omega)/2],all_500_source_points_fail=bool(np.all(abs(error)>1e-6)),all_source_comparisons_pass=all(row[5] for row in rows),all_convergence_pass=all(max(row['radau_refinement'],row['tight_cross_algorithm'])<=row['threshold'] for row in convergence))
dump(out/'summary.json',summary)
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(2,1,figsize=(9,7),sharex=True,layout='constrained')
ax[0].plot(t,source,label='Encoded dP_Ldt',color='#b54b39');ax[0].plot(t,derivative,label='Independent derivative of P_L',color='#176a75');ax[0].set_ylabel('Pressure derivative (mmHg/s)');ax[0].legend(loc='upper right');ax[0].set_title('Numerical agreement does not establish derivative consistency')
ax[1].plot(t,error,color='#b54b39');ax[1].axhline(0,color='black',lw=.7);ax[1].set_ylabel('Encoded − independently derived\n(mmHg/s)');ax[1].set_xlabel('Time (s)')
fig.savefig(out/'pressure-audit.png',dpi=180);fig.savefig(out/'pressure-audit.svg');plt.close(fig)
import scipy
metadata=dict(archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),protocol_sha256=hashlib.sha256((BASE/'protocol.json').read_bytes()).hexdigest(),python=sys.version,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform(),model='gpt-6-astra',wall_seconds=time.monotonic()-start,cli_calls=len(logs),platform_runs=len(runs),failed_cli_calls=sum(x['returncode']!=0 for x in logs),total_run_wall_seconds=sum(x['result']['total_wall_seconds'] for x in runs),paid_services=0,limitations='LLM token usage/billing not exposed to this leaf; wall time is measured, not monetary cost.')
dump(out/'study-runtime.json',metadata)
dump(out/'files.sha256.json',{str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob('*')) if f.is_file()})
print(json.dumps(summary,indent=2))
