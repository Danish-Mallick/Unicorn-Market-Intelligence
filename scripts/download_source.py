"""Retrieve four source CSVs from the published educational GitHub copy.
Usage (internet required): python scripts/download_source.py
The public upstream data are historic (~2022), not current valuations.
"""
from pathlib import Path
from urllib.request import urlopen, Request

BASE = "https://raw.githubusercontent.com/ShaikhBorhanUddin/Unicorn_Company_Analysis/main/Dataset"
DEST = Path(__file__).resolve().parents[1] / 'data' / 'raw'
DEST.mkdir(parents=True, exist_ok=True)
for stem in ('companies', 'dates', 'funding', 'industries'):
    url = f'{BASE}/{stem}.csv'
    request = Request(url, headers={'User-Agent': 'Educational-Unicorn-Analysis/1.0'})
    with urlopen(request, timeout=30) as response:
        data = response.read()
    if len(data) < 1000:
        raise ValueError(f'Unexpectedly small download: {url}')
    target = DEST / f'{stem}.csv'
    target.write_bytes(data)
    print(f'{target.relative_to(DEST.parent.parent)}  {len(data):,} bytes')
print('Done. Run: python scripts/analyze.py')
