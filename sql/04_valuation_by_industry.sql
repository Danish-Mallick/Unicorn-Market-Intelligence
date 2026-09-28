-- Cross-sectional valuation at data snapshot, not historical annual revenue.
SELECT TRIM(BOTH '"' FROM i.industry) AS industry,
       COUNT(*) AS company_count,
       ROUND(AVG(f.valuation::NUMERIC) / 1000000000, 2)
           AS avg_snapshot_valuation_billions,
       ROUND(SUM(f.valuation::NUMERIC) / 1000000000, 2)
           AS total_snapshot_valuation_billions
FROM industries i
JOIN funding f USING (company_id)
GROUP BY TRIM(BOTH '"' FROM i.industry)
ORDER BY company_count DESC, industry;
