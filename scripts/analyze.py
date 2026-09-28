"""Read original four source CSVs, recreate verified outputs and quality checks.

Run: python scripts/download_source.py && python scripts/analyze.py
This script does not infer annual historical values from snapshot valuations.
"""
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data' / 'raw'
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
inputs = {x: pd.read_csv(D / (x + '.csv')) for x in ('companies','dates','funding','industries')}
for name, df in inputs.items():
    assert len(df) == 1074, f'Unexpected {name} count: {len(df)}; verify source version'
    assert df.company_id.is_unique, f'Duplicate company IDs in {name}'

companies, dates, funding, industries = (inputs[x] for x in ('companies','dates','funding','industries'))
dates['date_joined'] = pd.to_datetime(dates.date_joined, dayfirst=True, errors='raise')
industries['industry'] = industries.industry.str.strip('"')
full = companies.merge(dates, on='company_id', validate='one_to_one').merge(
    funding, on='company_id', validate='one_to_one').merge(
    industries, on='company_id', validate='one_to_one')
full['year'] = full.date_joined.dt.year
full['valuation_billions'] = full.valuation / 1e9
full['funding_billions'] = full.funding / 1e9
full['years_to_unicorn'] = full.year - full.year_founded
full.to_csv(OUT / 'merged_source_reproducible.csv', index=False)

scope = full[full.year.between(2019, 2021)].copy()
top = (scope.groupby('industry').company_id.nunique().sort_values(ascending=False).head(3).index)
q1 = (scope[scope.industry.isin(top)].groupby(['industry','year'])
      .agg(num_unicorns=('company_id','nunique'),average_valuation_billions=('valuation_billions','mean'))
      .reset_index())
q1['average_valuation_billions'] = q1['average_valuation_billions'].round(2)
q1 = q1.sort_values(['year','num_unicorns','industry'],ascending=[False,False,True])
q1.to_csv(OUT/'01_top3_industry_2019_2021.csv',index=False)

countries=(scope.groupby('country').agg(new_unicorns=('company_id','nunique'),
              snapshot_valuation_billions=('valuation_billions','sum'))
           .reset_index().sort_values('new_unicorns',ascending=False).head(10))
countries.snapshot_valuation_billions=countries.snapshot_valuation_billions.round(2)
countries.to_csv(OUT/'03_top_countries_2019_2021.csv',index=False)

new_all = scope.groupby('year').company_id.nunique()
new_top = scope[scope.industry.isin(top)].groupby('year').agg(
    top3_new_unicorns=('company_id','nunique'),top3_avg_valuation_billions=('valuation_billions','mean'))
year = new_all.rename('all_new_unicorns').to_frame().join(new_top).reset_index()
year.top3_avg_valuation_billions=year.top3_avg_valuation_billions.round(2)
year.to_csv(OUT/'02_yearly_growth.csv',index=False)

quality={"missing_city":int(full.city.isna().sum()+(full.city.fillna('').str.strip()=='').sum()-full.city.isna().sum()),
         "zero_reported_funding":int(full.funding.eq(0).sum()),
         "founded_after_unicorn_date":int(full.years_to_unicorn.lt(0).sum())}
print('Full dataset:',len(full),'| Period 2019-2021:',len(scope),'| top-3 industries:',list(top))
print('Quality:',quality)
print(q1.to_string(index=False))
# Independently check against the published snapshot before updating the project.
import json
snapshot=json.loads((ROOT/'data'/'verified_source_snapshot.json').read_text())
assert len(full)==snapshot['full_dataset_company_count']
assert len(scope)==snapshot['scope_count']
assert set(top)=={'Fintech','Internet software & services','E-commerce & direct-to-consumer'}
expected={ (r['industry'],r['year']):r for r in snapshot['top3_by_industry_year']}
for r in q1.to_dict('records'):
    e=expected[(r['industry'],r['year'])]
    assert r['num_unicorns']==e['num_unicorns'] and r['average_valuation_billions']==e['average_valuation_billions']
print('Source snapshot validation: PASS')
