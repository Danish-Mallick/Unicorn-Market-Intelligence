-- Report source limitations explicitly; do not silently discard rows.
SELECT
    COUNT(*) AS total_companies,
    COUNT(*) FILTER (WHERE c.city IS NULL OR TRIM(c.city) = '') AS missing_city,
    COUNT(*) FILTER (WHERE f.funding = 0) AS zero_reported_funding,
    COUNT(*) FILTER (
        WHERE d.year_founded > EXTRACT(YEAR FROM d.date_joined)
    ) AS founded_after_joined_year
FROM companies c
JOIN dates d USING (company_id)
JOIN funding f USING (company_id);
