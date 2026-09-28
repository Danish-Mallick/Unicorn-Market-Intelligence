-- Full 2019-2021 sector-wide cohort sizes.
SELECT EXTRACT(YEAR FROM date_joined)::INT AS year,
       COUNT(*) AS new_unicorns
FROM dates
WHERE date_joined >= DATE '2019-01-01'
  AND date_joined < DATE '2022-01-01'
GROUP BY year
ORDER BY year;
