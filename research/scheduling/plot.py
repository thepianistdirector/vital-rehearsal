#!/usr/bin/env python3
"""Render confirmed finite results. AGPL-3.0-or-later."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
rows=json.loads((p/'confirmation/paired-effects.json').read_text())
labels=['Smooth, 1 server · load 0.50','Smooth, 1 server · load 0.95','Smooth, 1 server · load 1.10','Smooth, 4 servers · load 0.95','Bursts, 4 servers · load 0.70','Heterogeneous, 4 servers · load 0.70']
fig,ax=plt.subplots(figsize=(11,6.4));fig.subplots_adjust(left=.34,right=.92,top=.80,bottom=.17)
for s,(seed,offset,fill) in enumerate([(1701,-.18,'#2864a5'),(2903,.18,'white')]):
 vals=[r['delta_mean_wait_s'] for r in rows if r['seed']==seed];y=[i+offset for i in range(6)]
 ax.barh(y,vals,height=.31,color=fill,edgecolor='#2864a5',linewidth=1.3,label=f'Seed {seed}')
 for yy,v in zip(y,vals):ax.text(v+4,yy,f'{v:.2f}',va='center',fontsize=9,color='#263238')
ax.set_yticks(range(6),labels,fontsize=10);ax.invert_yaxis();ax.set_xlim(0,445);ax.set_xlabel('Paired increase in mean wait (seconds)',fontsize=11);ax.xaxis.grid(True,color='#e2e5e8',linewidth=.7);ax.set_axisbelow(True)
for side in ['top','right']:ax.spines[side].set_visible(False)
ax.legend(loc='lower right',frameon=False,fontsize=10)
fig.text(.035,.95,'Mean waiting-time change across synthetic workloads',fontsize=17,weight='bold',color='#263238')
fig.text(.035,.90,'800 jobs per case; service extension 0 → 1 second; nominal baseline offered load shown',fontsize=11)
fig.text(.035,.065,'Source: confirmation/paired-effects.csv. Finite seed results, not confidence intervals.\nBurst seeds produce the same workload. No patient data or clinical interpretation.',fontsize=9,color='#465158')
for ext in ['png','svg']:fig.savefig(p/f'figure-1.{ext}',dpi=160,facecolor='white')
(p/'plot-runtime.json').write_text(json.dumps({'matplotlib':matplotlib.__version__},indent=2)+'\n')
