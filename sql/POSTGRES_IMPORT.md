# Load the original four CSV tables into PostgreSQL

1. Run `python scripts/download_source.py` from the repository root with internet access.
2. Create an empty database, then run `psql -d YOUR_DB -f sql/00_schema.sql`.
3. The `dates.csv` source uses **DD/MM/YYYY**. Import dates as text into a staging table first, then explicitly convert; don't rely on your PostgreSQL session's `DateStyle`.

```sql
CREATE TEMP TABLE dates_stage (company_id INT, date_joined TEXT, year_founded INT);
```

Run the following in `psql` from the repository root:

```sql
\copy companies(company_id, company, city, country, continent) FROM 'data/raw/companies.csv' WITH (FORMAT csv, HEADER true);
\copy dates_stage FROM 'data/raw/dates.csv' WITH (FORMAT csv, HEADER true);
INSERT INTO dates(company_id, date_joined, year_founded)
SELECT company_id, to_date(date_joined, 'DD/MM/YYYY'), year_founded
FROM dates_stage;
\copy funding(company_id, valuation, funding, select_investors) FROM 'data/raw/funding.csv' WITH (FORMAT csv, HEADER true);
\copy industries(company_id, industry) FROM 'data/raw/industries.csv' WITH (FORMAT csv, HEADER true);
```

Use `sql/01_datacamp_solution.sql` for the assignment. Some mirrored source industry strings contain extra quotation marks; the query removes these before grouping. Validate the input count and join cardinality if DataCamp's database version differs from the downloadable mirror.
