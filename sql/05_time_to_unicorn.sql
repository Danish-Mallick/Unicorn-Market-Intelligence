-- Approximate years to unicorn by industry for the full historical sample.
-- Flag founded_year > joined_year rather than interpreting negative tenure.
WITH tenure AS (
    SELECT TRIM(BOTH '"' FROM i.industry) AS industry,
           EXTRACT(YEAR FROM d.date_joined)::INT - d.year_founded AS years_to_unicorn
    FROM industries i JOIN dates d USING (company_id)
    WHERE d.year_founded IS NOT NULL
)
SELECT industry, COUNT(*) AS valid_records,
       ROUND(AVG(years_to_unicorn::NUMERIC), 1) AS avg_years_to_unicorn
FROM tenure
WHERE years_to_unicorn >= 0
GROUP BY industry
ORDER BY valid_records DESC;
