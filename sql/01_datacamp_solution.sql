-- DataCamp: Analyzing Unicorn Companies
-- Rank industries by how many NEW unicorns appeared in 2019-2021 COMBINED.
-- For those three industries, return a row for each year (including years with
-- zero new unicorns, if any). Valuation is a historical snapshot, NOT the
-- valuation at the moment each company joined the unicorn club.
WITH annual_new AS (
    SELECT
        TRIM(BOTH '"' FROM i.industry) AS industry,
        EXTRACT(YEAR FROM d.date_joined)::INT AS year,
        f.valuation
    FROM industries AS i
    JOIN dates AS d ON i.company_id = d.company_id
    JOIN funding AS f ON i.company_id = f.company_id
    WHERE d.date_joined >= DATE '2019-01-01'
      AND d.date_joined <  DATE '2022-01-01'
),
top_three AS (
    SELECT industry
    FROM annual_new
    GROUP BY industry
    ORDER BY COUNT(*) DESC, industry
    LIMIT 3
)
SELECT
    a.industry,
    a.year,
    COUNT(*) AS num_unicorns,
    ROUND(AVG(a.valuation::NUMERIC) / 1000000000, 2)
        AS average_valuation_billions
FROM annual_new AS a
JOIN top_three AS t USING (industry)
GROUP BY a.industry, a.year
ORDER BY a.year DESC, num_unicorns DESC, a.industry;
