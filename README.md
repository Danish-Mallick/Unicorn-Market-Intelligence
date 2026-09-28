# The Billion-Dollar Club
### Where did the 2019–2021 unicorn boom actually come from?

![Unicorn market intelligence dashboard](charts/LinkedIn_Dashboard_Preview.svg)

**SQL · Python · Power BI** | 1,074 companies in the historical source | 2019–2021 analysis window

[The SQL answer](sql/01_datacamp_solution.sql) · [Interactive dashboard](report/interactive_dashboard.html) · [Verified results](results/01_top3_industry_2019_2021.csv) · [Python analysis](scripts/analyze.py) · [Power BI build notes](powerbi/OPEN_IN_DESKTOP.md)

> These are **historical, approximately-2022 figures**, not live private-market data. The cover is a **designed, data-based preview**, not a screenshot of a live Power BI dashboard.

## The question I started with

The DataCamp exercise asks which industries produced the most *new* unicorns from 2019 through 2021. A unicorn, in this context, is a privately held company valued at $1 billion or more.

At first, I considered comparing industries by valuation. But that would answer a different question: a few unusually valuable companies can lift an industry's average without telling me how many companies *newly entered* the unicorn club. So I used **new-unicorn counts** to select the three industries and only then calculated their average recorded valuations.

I kept the exercise's 2019–2021 window and joined four tables on `company_id`: companies, dates, funding and industries. I checked that each source table contained **1,074 unique company IDs** so a many-to-many join couldn't quietly inflate the counts.

## What stood out

The dataset records **732** newly designated unicorns across all industries in 2019–2021. **400 of them (54.6%)** came from just three industries:

| Industry | Three-year total | 2019 | 2020 | 2021 |
|:--|--:|--:|--:|--:|
| Fintech | **173** | 20 | 15 | 138 |
| Internet software & services | **152** | 13 | 20 | 119 |
| E-commerce & direct-to-consumer | **75** | 12 | 16 | 47 |

What caught my attention was the change in pace. There were **104** new unicorns across all industries in 2019, **108** in 2020 and **520** in 2021. The last figure is much larger, so the next question was whether this was one industry's story or a broader shift.

![New unicorn counts by industry and year](charts/industry_year_comparison.svg)

The three industries above contributed **304** of the 520 new unicorns in 2021. Fintech and internet software together accounted for 257. These are *counts of new companies*, not measurements of industry profitability.

### Counts and valuations tell different stories

I also calculated the average valuation recorded for companies joining each year. The original nine-row SQL output is:

| Industry | Joined | New unicorns | Average recorded valuation ($B) |
|:--|--:|--:|--:|
| Fintech | 2021 | 138 | 2.75 |
| Internet software & services | 2021 | 119 | 2.15 |
| E-commerce & direct-to-consumer | 2021 | 47 | 2.47 |
| Internet software & services | 2020 | 20 | 4.35 |
| E-commerce & direct-to-consumer | 2020 | 16 | 4.00 |
| Fintech | 2020 | 15 | 4.33 |
| Fintech | 2019 | 20 | 6.80 |
| Internet software & services | 2019 | 13 | 4.23 |
| E-commerce & direct-to-consumer | 2019 | 12 | 2.58 |

An important detail: this source contains **one valuation per company from a later historical snapshot**, not the valuation *when it joined*. For example, the $6.80B average for the 2019 fintech cohort describes those companies as recorded by the source. It does **not** prove that fintech startups joined at higher valuations in 2019. I explicitly avoided plotting those averages as an annual valuation time series.

## My follow-up: where were the new unicorns based?

I joined headquarters data to the 2019–2021 cohort rather than treating unicorn activity as purely an industry story. In this sample, the **US accounted for 413** new unicorns, followed by **China (79)** and **India (47)**. Those are *headquarters locations*; they don't tell us where the companies generate sales, receive investment or deliver returns.

## How to inspect or reproduce it

The [original SQL](sql/01_datacamp_solution.sql) filters the time window first, ranks industries by the **combined** three-year new-unicorn count and reports annual counts plus average recorded valuations for the **same** top three. Ranking industries separately in each year would answer a different question.

I then used Python to recreate the groupings independently and added SQL for [geographic concentration](sql/02_country_concentration.sql), [annual entries](sql/03_annual_growth.sql), [industry valuations](sql/04_valuation_by_industry.sql), [time to unicorn](sql/05_time_to_unicorn.sql) and [quality checks](sql/06_quality_checks.sql). The [offline dashboard](report/interactive_dashboard.html) gives a visual way to explore the historical cohorts.

To run the files after downloading the source CSVs:

```bash
python -m pip install -r requirements.txt
python scripts/download_source.py
python scripts/analyze.py
python -m unittest discover -s tests -v
```

The raw third-party CSVs are **not republished here**; the download script retrieves the documented public copy. See [source and licensing notes](data/SOURCE_AND_LICENSE.md) before redistributing any raw data.

The repository also includes an [editable Power BI project generation script](scripts/build_powerbi.py), [DAX definitions](powerbi/dax_measures.dax) and [Desktop instructions](powerbi/OPEN_IN_DESKTOP.md). **The native Power BI layout was generated programmatically, not verified on a Windows Desktop installation.**

## Where the data stops being useful

This isn't a live 2026 market report or an investment recommendation. There are **16 missing cities**, **13 zero-reported funding entries** and **one company whose recorded founding year comes after its unicorn joining year**. I flagged these rather than changing records without evidence.

More importantly, we don't have dated funding rounds, full valuation histories or outcomes for startups that never became unicorns. I can describe which companies in this historical sample entered the club and when; I cannot infer investment returns or confidently explain *why* 2021 saw more entries.

The public four-table copy also contains at least one early-April-2022 joining date, so I describe it as an **approximately-2022 historical dataset**, not an exact match to every published version.

### Credit

The starting challenge is [DataCamp: Analyzing Unicorn Companies](https://www.datacamp.com/projects/1531). The four public CSV tables are sourced from [Shaikh Borhan Uddin's educational dataset mirror](https://github.com/ShaikhBorhanUddin/Unicorn_Company_Analysis/tree/main/Dataset); the related [Maven Analytics Unicorn Companies](https://mavenanalytics.io/data-playground/unicorn-companies) distribution is documented in the source note. This portfolio's questions, reproducible analysis and presentation focus on **the 2019–2021 cohort**, rather than reproducing the mirror repository's broader set of questions.
