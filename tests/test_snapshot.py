from pathlib import Path
import json, csv, unittest
root=Path(__file__).resolve().parents[1]
snap=json.loads((root/'data/verified_source_snapshot.json').read_text())
class AnalysisTests(unittest.TestCase):
    def test_cohort_and_top3_counts(self):
        self.assertEqual(snap['scope_count'], sum(snap['year_counts_all_sectors'].values()))
        self.assertEqual(snap['top3_scope_count'],sum(row['num_unicorns'] for row in snap['top3_by_industry_year']))
        self.assertEqual(snap['top3_scope_count'],400)
    def test_rank_methodology(self):
        ranks={industry:sum(x['num_unicorns'] for x in snap['top3_by_industry_year'] if x['industry']==industry)
             for industry in set(x['industry'] for x in snap['top3_by_industry_year'])}
        self.assertEqual(ranks,{'Fintech':173,'Internet software & services':152,'E-commerce & direct-to-consumer':75})
    def test_original_sql_shape(self):
        with (root/'results/01_top3_industry_2019_2021.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),9)
        self.assertEqual(list(rows[0]),['industry','year','num_unicorns','average_valuation_billions'])
        self.assertEqual([int(r['year']) for r in rows],[2021]*3+[2020]*3+[2019]*3)
    def test_report_disclosure(self):
        readme=(root/'README.md').read_text().lower()
        self.assertIn('not current',readme)
        self.assertIn('snapshot',readme)
if __name__=='__main__':unittest.main()
