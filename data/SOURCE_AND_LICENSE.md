# Data provenance, source version and redistribution

- Four original files: `companies.csv`, `dates.csv`, `funding.csv`, `industries.csv` (each 1,074 rows).
- Public split-table source: https://github.com/ShaikhBorhanUddin/Unicorn_Company_Analysis/tree/main/Dataset
- Related original dataset: https://mavenanalytics.io/data-playground/unicorn-companies
- Exercise: https://www.datacamp.com/projects/1531

**Licensing:** Maven Analytics labels its Unicorn Companies dataset **Public Domain**; the public GitHub host's repository is marked MIT for repository code. To prevent any ambiguity about redistribution of a third-party mirror, **the four raw CSV files are not committed here**. `scripts/download_source.py` obtains them from the public repo; the verified derived results and summaries are included. Verify source reuse terms before republishing raw files.

**Snapshot limitation:** Maven describes its dataset as of March 2022. The mirrored four-table CSV split contains at least one early-April-2022 unicorn date; therefore this project describes the **specific four-table public mirror** as historical, approximately 2022. Do not present this as live or 2026 data and don't assume byte-for-byte parity with an active DataCamp instance.

**Numeric caveat:** `valuation` is the source's approximate snapshot valuation in USD. The query calculates the mean snapshot valuation for the cohort defined by year joined; it does NOT estimate valuation on the date the company first became a unicorn.

**Quality flags from the four-table mirror:** 16 missing city values, 13 funding entries of zero and one founding year recorded after the unicorn joining year. Source has 1,074 distinct IDs in each of its four tables and an exact one-to-one join over the IDs.
