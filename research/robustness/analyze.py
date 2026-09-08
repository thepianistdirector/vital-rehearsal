#!/usr/bin/env python3
"""Independent output-only analysis; no model imports or integrations."""
import csv,json,pathlib,sys,hashlib,math
import numpy as np
H=pathlib.Path(__file__).resolve().parent; C=H/(sys.argv[1] if len(sys.argv)>1 else 'confirmation-20260908')
meta=json.loads((C/'campaign.json').read_text()); specs=meta['specs']; arrays={}; results={}; inventory=[]
for i,s in enumerate(specs):
 d=next((C/f'{i:02d}-{s[0]}-attempts').iterdir()); results[i]=json.loads((d/'result.json').read_text());a=np.genfromtxt(d/'trajectory.csv',delimiter=',',names=True);arrays[i]=np.column_stack([a[n] for n in a.dtype.names[1:]])
 inventory.append(dict(index=i,name=s[0],bundle=str(d.relative_to(H)),execution_state=results[i]['execution_state'],candidate_wall_s=results[i]['cost']['wall_seconds'],total_wall_s=results[i]['total_wall_seconds'],nfev=results[i]['cost']['nfev'],runtime=json.loads((d/'runtime.json').read_text())))
(C/'inventory.json').write_text(json.dumps(inventory,indent=2))
names=list(a.dtype.names[1:]); units=['litre','mmHg','dimensionless','dimensionless','mmHg','mmHg','source-labelled dimensionless; unresolved']; thresholds=np.array([1e-6,1e-4,1e-7,1e-7,1e-4,1e-4,1e-8]);anchor=arrays[3]
def write(name,rows):
 with (C/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
widths={r:np.ptp(np.stack([arrays[k] for k in indices]),axis=0).max(axis=0) for r,indices in [(.9,[0,1,2]),(1.,[3,4,5]),(1.1,[6,7,8])]}
refine=np.abs(arrays[17]-anchor).max(axis=0)
convergence=[dict(state=n,unit=units[j],threshold=thresholds[j],width_R09=widths[.9][j],width_R10=widths[1.][j],width_R11=widths[1.1][j],refinement=refine[j],passes=bool(max(widths[r][j] for r in widths)<thresholds[j] and refine[j]<thresholds[j])) for j,n in enumerate(names)];write('convergence.csv',convergence)
errors=[]
for i,s in enumerate(specs):
 ref=arrays[{.9:0,1.:3,1.1:6}[s[5]]];diff=arrays[i]-ref
 for j,n in enumerate(names):errors.append(dict(run=s[0],state=n,unit=units[j],max_absolute=float(abs(diff[:,j]).max()),rms=float(np.sqrt(np.mean(diff[:,j]**2))),final=float(arrays[i][-1,j]),max_relative_excluding_initial=float((abs(diff[1:,j])/abs(ref[1:,j])).max())))
write('solver-errors.csv',errors)
effects=[]
for r,i in [(.9,0),(1.1,6)]:
 for j,n in enumerate(names):
  eff=abs(arrays[i][:,j]-anchor[:,j]).max();env=widths[r][j]+widths[1.][j]
  effects.append(dict(resistance_scale=r,state=n,unit=units[j],max_absolute_change=eff,final_signed_change=arrays[i][-1,j]-anchor[-1,j],sum_control_widths=env,effect_to_envelope_ratio=eff/env,numerically_separated=bool(eff>10*env and convergence[j]['passes'])))
write('resistance-effects.csv',effects)
tol=[dict(run=specs[i][0],rtol=specs[i][2],atol=specs[i][3],atol_over_rtol_z0=specs[i][3]/(specs[i][2]*anchor[0,-1]),max_absolute_z_error=next(e['max_absolute'] for e in errors if e['run']==specs[i][0] and e['state']=='z'),max_relative_z_error=next(e['max_relative_excluding_initial'] for e in errors if e['run']==specs[i][0] and e['state']=='z')) for i in [9,10,11,12,13,14,15]];write('z-tolerance.csv',tol)
# Standalone vector figure: solver disagreement normalized to predeclared thresholds.
selected=[9,10,11,12,13,14,15,16];svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620"><rect width="1000" height="620" fill="#f6f7fb"/><g font-family="sans-serif" fill="#152238"><text x="35" y="38" font-size="23">Solver differences relative to tight Radau</text><text x="35" y="65" font-size="14">log10(maximum sampled error / predeclared state threshold); 10 seconds, R scale 1</text>']
for j,n in enumerate(names):svg.append(f'<text x="{230+j*105}" y="103" font-size="16">{n}</text>')
for row,i in enumerate(selected):
 y=125+row*50;svg.append(f'<text x="30" y="{y+28}" font-size="15">{specs[i][0]}</text>')
 for j,n in enumerate(names):
  err=next(e['max_absolute'] for e in errors if e['run']==specs[i][0] and e['state']==n);log=math.log10(max(err/thresholds[j],1e-12));col='#b34137' if log>0 else '#247c75';svg.append(f'<rect x="{215+j*105}" y="{y}" width="95" height="40" rx="4" fill="{col}"/><text x="{235+j*105}" y="{y+26}" font-size="15" fill="white">{log:.2f}</text>')
svg.append('<text x="35" y="565" font-size="14">Red: above an engineering threshold. Green: below. Thresholds have no clinical interpretation.</text><text x="35" y="588" font-size="14">Reference is an observed convergence control, not an exact or empirical solution.</text></g></svg>');(C/'solver-figure.svg').write_text(''.join(svg))
print(json.dumps({'convergence':convergence,'effects':effects,'z':tol,'cost_s':sum(x['total_wall_s'] for x in inventory)},indent=2))
# Checksums for retained campaign evidence, excluding the checksum file itself.
(C/'sha256.json').write_text(json.dumps({str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(C.rglob('*')) if p.is_file() and p.name!='sha256.json'},indent=2))
