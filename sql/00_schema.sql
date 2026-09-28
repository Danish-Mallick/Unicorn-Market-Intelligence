-- PostgreSQL: four-table schema for the source snapshot.
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company TEXT,
    city TEXT,
    country TEXT,
    continent TEXT
);
CREATE TABLE IF NOT EXISTS dates (
    company_id INTEGER PRIMARY KEY REFERENCES companies(company_id),
    date_joined DATE,
    year_founded INTEGER
);
CREATE TABLE IF NOT EXISTS funding (
    company_id INTEGER PRIMARY KEY REFERENCES companies(company_id),
    valuation BIGINT,
    funding BIGINT,
    select_investors TEXT
);
CREATE TABLE IF NOT EXISTS industries (
    company_id INTEGER PRIMARY KEY REFERENCES companies(company_id),
    industry TEXT
);
