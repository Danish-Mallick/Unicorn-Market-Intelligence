"""Transparent static source-verified charts; recreate from included result CSVs."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
D=pd.read_csv(ROOT/'results/01_top3_industry_2019_2021.csv')
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
labels=['Fintech','Internet software\n& services','E-commerce\n& direct-to-consumer']
sectors=['Fintech','Internet software & services','E-commerce & direct-to-consumer']
colors=['#f07ba7','#e5b96d','#64cbbf']
fig,ax=plt.subplots(figsize=(10,5.4));x=np.arange(3);width=.25
for idx,year in enumerate([2019,2020,2021]):
 values=[int(D[(D.industry==sector)&(D.year==year)].num_unicorns.iloc[0]) for sector in sectors]
 bars=ax.bar(x+(idx-1)*width,values,width,color=colors[idx],label=str(year))
 ax.bar_label(bars,padding=3,fontsize=9)
ax.set_xticks(x,labels);ax.set_ylabel('New unicorns in each cohort')
ax.set_title('The three most active industries, 2019–2021',loc='left',fontweight='bold')
ax.legend(frameon=False,ncol=3);ax.grid(axis='y',alpha=.16)
fig.tight_layout();fig.savefig(ROOT/'charts/industry_year_comparison.png',dpi=180,bbox_inches='tight');plt.close(fig)
X=pd.read_csv(ROOT/'results/03_top_countries_2019_2021.csv').head(7)
fig,ax=plt.subplots(figsize=(8.8,4.7));y=np.arange(len(X))
ax.barh(y,X.new_unicorns,color='#637dd0')
ax.set_yticks(y,X.country);ax.invert_yaxis()
ax.set_xlabel('New unicorns, 2019–2021')
ax.set_title('Headquarters geography of new unicorns',loc='left',fontweight='bold')
for i,v in enumerate(X.new_unicorns):ax.text(v+4,i,str(v),va='center',fontsize=9)
ax.set_xlim(0,490);ax.grid(axis='x',alpha=.1);fig.tight_layout();fig.savefig(ROOT/'charts/country_distribution.png',dpi=180,bbox_inches='tight');plt.close(fig)
print('Saved 2 transparent analytical charts')
