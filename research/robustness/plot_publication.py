"""Post-review figure from retained CSV only; no simulation or changed confirmation."""
from pathlib import Path
import csv,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent;data=root/'confirmation-20260908'
rows=list(csv.DictReader((data/'solver-errors.csv').read_text().splitlines()))
checks=list(csv.DictReader((data/'convergence.csv').read_text().splitlines()))
threshold={r['state']:float(r['threshold']) for r in checks};names=list(threshold)
fig,ax=plt.subplots(figsize=(11,6))
for key,label,marker,color in [('source-default','Source-default VODE','o','#b04432'),('source-tight','Tight VODE','s','#6b54a2'),('baseline','Baseline Radau','^','#146a75'),('RK45','RK45','D','#55752f')]:
 values=[next(float(r['max_absolute'])/threshold[name] for r in rows if r['run']==key and r['state']==name) for name in names]
 ax.plot(names,values,label=label,marker=marker,color=color,linestyle="none",markersize=7)
ax.axhline(1,color='#555555',linestyle='--',label='Frozen control threshold')
ax.set_yscale('log');ax.set_ylabel('Maximum sampled difference / state threshold')
ax.set_title('Numerical settings change disagreement with tight Radau',loc='left',fontweight='bold',pad=15)
ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);ax.legend(loc='lower right',fontsize=9)
fig.text(.08,.025,'Same equations, 10 s, 2001 samples. Numerical differences are not truth-error bounds or clinical tolerances.\nSource: confirmation-20260908/solver-errors.csv and convergence.csv. No new integrations.',fontsize=9)
fig.subplots_adjust(bottom=.19,left=.11,right=.97,top=.9)
fig.savefig(root/'publication-figure.png',dpi=160);fig.savefig(root/'publication-figure.svg')
(root/'publication-figure-provenance.json').write_text(json.dumps({'matplotlib':matplotlib.__version__,'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [data/'solver-errors.csv',data/'convergence.csv',Path(__file__)]},'change':'post-review rendering only; frozen evidence unchanged'},indent=2)+'\n')
