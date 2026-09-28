-- Headquarters country distribution for NEW unicorns 2019-2021.
SELECT c.country, COUNT(*) AS new_unicorns,
       ROUND(SUM(f.valuation::NUMERIC) / 1000000000, 2)
           AS snapshot_valuation_billions
FROM companies c
JOIN dates d USING (company_id)
JOIN funding f USING (company_id)
WHERE d.date_joined >= DATE '2019-01-01'
  AND d.date_joined < DATE '2022-01-01'
GROUP BY c.country
ORDER BY new_unicorns DESC, c.country
LIMIT 10;
