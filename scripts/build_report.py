"""Two-page executive brief generated from checked, historical source aggregates."""
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import json
r=Path(__file__).resolve().parents[1];s=json.loads((r/'data/verified_source_snapshot.json').read_text());dst=r/'report/executive_brief.pdf'
normal='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
bold='/usr/share/fonts/truetype/lato/Lato-Bold.ttf'
if not Path(normal).exists():
 normal='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('Lato',normal))
pdfmetrics.registerFont(TTFont('LatoBold',bold))
c=Canvas(str(dst),pagesize=(900,650));W,H=900,650
bg=HexColor('#0A1122');white=HexColor('#F4F8FE');muted=HexColor('#B2C3DA');pink=HexColor('#FC7CAC');line=HexColor('#263B5A');amber=HexColor('#FFC77B');cyan=HexColor('#5BDECE')
# Cover page
c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
c.setFont('LatoBold',12);c.setFillColor(pink);c.drawString(40,604,'UNICORN MARKET INTELLIGENCE  /  EXECUTIVE BRIEF')
c.setFont('LatoBold',24);c.setFillColor(white);c.drawString(40,562,'Where did the unicorn boom take shape?')
c.setFont('Lato',12);c.setFillColor(muted);c.drawString(40,541,'Historical cohort analysis   |   2019-2021   |   1,074 total companies in the source')
c.drawImage(ImageReader(str(r/'charts/LinkedIn_Dashboard_Preview.png')),40,95,width=820,height=461,mask='auto',preserveAspectRatio=True,anchor='c')
c.setFillColor(muted);c.setFont('Lato',10);c.drawString(40,51,'This image is a verified-data design preview, not a native Power BI screenshot.')
c.drawString(40,34,'Data are historical (~2022). Snapshot valuation is not a valuation history or an investment return.')
c.showPage()
# Sources and exact query output page
c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(pink);c.setFont('LatoBold',12);c.drawString(42,610,'VERIFIED FINDINGS / ORIGINAL FOUR-TABLE EXERCISE')
c.setFillColor(white);c.setFont('LatoBold',23);c.drawString(42,570,'The data behind the headline')
c.setFillColor(muted);c.setFont('Lato',11);c.drawString(42,546,'Rank industries by the combined number of new unicorns during 2019, 2020 and 2021.')
for ix,(x,label,sub) in enumerate([(732,'NEW UNICORNS','All industries'),(400,'TOP-THREE TOTAL','54.6% of the cohort'),(520,'NEW UNICORNS IN 2021','71.0% of the 2019-21 cohort')]):
 xx=42+ix*281;c.setFillColor(HexColor('#172641'));c.roundRect(xx,435,265,85,11,fill=1,stroke=0);c.setFillColor(amber if ix==2 else cyan);c.setFont('LatoBold',30);c.drawString(xx+14,475,str(x));c.setFillColor(white);c.setFont('LatoBold',9);c.drawString(xx+14,455,label)
headers=['Industry','Year','New','Avg snapshot $B'];x=[43,453,568,680];c.setFillColor(HexColor('#1E3553'));c.roundRect(42,385,813,31,4,fill=1,stroke=0)
for xx,label in zip(x,headers):c.setFillColor(white);c.setFont('LatoBold',10);c.drawString(xx,396,label)
rows=sorted(s['top3_by_industry_year'],key=lambda z:(-z['year'],-z['num_unicorns'],z['industry']))
for idx,row in enumerate(rows):
 yy=360-idx*25
 if idx%2==0:c.setFillColor(HexColor('#111F35'));c.rect(42,yy-6,813,24,stroke=0,fill=1)
 for xx,val in zip(x,[row['industry'],str(row['year']),str(row['num_unicorns']),f"${row['average_valuation_billions']:.2f}B"]):
  c.setFillColor(white if xx==43 else muted);c.setFont('LatoBold' if xx==43 else 'Lato',10);c.drawString(xx,yy+2,val)
c.setFillColor(pink);c.setFont('LatoBold',10);c.drawString(42,116,'CAUTION / SCOPE')
c.setFillColor(muted);c.setFont('Lato',9.5)
for ix,line_ in enumerate(['The source mirrors a historical dataset approximately from 2022, not current 2026 private-market conditions.',
                       'Mean valuation is the historical source snapshot mean for each join-year cohort, NOT the value at entry.',
                       'Some quality flags remain in the source: 16 missing cities, 13 zero-funding entries, 1 inconsistent founding year.']):
 c.drawString(42,99-ix*15,line_)
c.setFont('Lato',8);c.setFillColor(HexColor('#869BB8'));c.drawString(42,24,'Source lineage and reproducibility: data/SOURCE_AND_LICENSE.md  |  SQL output: results/01_top3_industry_2019_2021.csv')
c.showPage();c.save();print('Created',dst,'size',dst.stat().st_size)
