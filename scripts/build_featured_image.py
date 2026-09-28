"""Render a verified, high-resolution editorial dashboard preview for README/LinkedIn."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parents[1];S=json.loads((ROOT/'data/verified_source_snapshot.json').read_text())
W,H=1920,1080
P={'bg':(9,16,34),'panel':(19,29,52),'stroke':(43,57,87),'white':(244,248,255),'muted':(157,176,207),'dim':(109,132,167),'pink':(250,125,172),'amber':(255,199,123),'cyan':(93,223,205),'purple':(146,157,255),'inactive':(63,83,119)}
# Deliberate visual glow and texture, without a misleading stock-chart background.
y,x=np.mgrid[0:H,0:W];base=np.zeros((H,W,3),dtype=np.float32)
for i,v in enumerate(P['bg']):base[:,:,i]=v
r=((x-1490)/1160)**2+((y+110)/750)**2
base+=np.exp(-r*4)[:,:,None]*np.array([19,8,39],dtype=np.float32)
noise=np.random.default_rng(2).normal(0,0.6,(H,W,1));base+=noise
img=Image.fromarray(np.clip(base,0,255).astype('uint8'),'RGB');d=ImageDraw.Draw(img)
fonts='/usr/share/fonts/opentype/inter/'
def ft(n,weight='Regular'):
    # Prefer Inter, but keep the preview reproducible on standard GitHub Actions Linux.
    original=Path(fonts+f'InterDisplay-{weight}.otf')
    fallback='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if weight in ('ExtraBold','Bold','SemiBold') else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(str(original) if original.exists() else fallback,n)

def text(x,y,s,size=20,weight='Regular',fill=None,anchor=None):d.text((x,y),s,font=ft(size,weight),fill=fill or P['white'],anchor=anchor)
def line(coords,c=P['stroke'],w=2):d.line(coords,fill=c,width=w)
def rr(coords,fill=P['panel'],outline=P['stroke'],radius=19,width=2):d.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)
# header
rr((56,36,102,82),fill=P['pink'],outline=None,radius=13)
text(80,40,'U',35,'ExtraBold',P['bg'])
text(118,40,'UNICORN / INTELLIGENCE',21,'ExtraBold')
text(118,67,'PRIVATE-MARKET DATA LAB',13,'Medium',P['dim'])
rr((1520,40,1860,81),fill=(38,35,65),outline=(75,63,99),radius=19)
text(1690,52,'2022 HISTORICAL SNAPSHOT',14,'SemiBold',P['pink'],anchor='lt')
line([(56,108),(1864,108)])
# hero
text(58,144,'THE BILLION-DOLLAR CLUB  /  GLOBAL',18,'Bold',P['pink'])
text(56,182,'Where did the unicorn boom',55,'ExtraBold')
text(56,246,'take shape?',60,'ExtraBold',P['amber'])
text(58,322,'Industry formation, global expansion and snapshot valuations. New unicorns in 2019–2021.',19,'Regular',P['muted'])
rr((1525,181,1860,279),fill=(29,39,68),outline=(70,75,116),radius=16)
text(1550,199,'RESEARCH WINDOW',14,'Bold',P['muted'])
text(1550,227,'2019 – 2021',29,'Bold',P['white'])
# KPI cards
w=433;gap=23;start=56; y1=383;y2=552
kpis=[('NEW UNICORNS', '732','ALL INDUSTRIES / 2019–2021',P['white']),('TOP 3 INDUSTRIES','400','FINTECH + SOFTWARE + E-COMMERCE',P['cyan']),('TOP 3 SHARE','54.6%','OF NEW UNICORNS IN THE PERIOD',P['amber']),('PEAK YEAR','2021','520 NEW UNICORNS / ALL INDUSTRIES',P['purple'])]
for n,(label,value,sub,color) in enumerate(kpis):
 x0=start+n*(w+gap);rr((x0,y1,x0+w,y2),fill=(22,34,61),outline=(49,64,95),radius=17)
 d.rounded_rectangle((x0+1,y1+1,x0+120,y1+5),radius=3,fill=color)
 text(x0+24,y1+23,label,16,'Bold',P['muted'])
 text(x0+22,y1+57,value,62,'ExtraBold',color)
 text(x0+24,y1+139,sub,12,'SemiBold',P['dim'])
# big analytic panels
pa=(56,573,1085,922);pb=(1105,573,1864,922)
for box in (pa,pb):rr(box,fill=(19,30,53),outline=(48,65,94),radius=19)
rr((82,598,122,633),fill=(56,41,68),outline=None,radius=8)
text(91,604,'01',18,'Bold',P['pink'])
text(141,600,'Most active industries',26,'Bold')
text(82,641,'New unicorn counts across the 2019–2021 window',15,'Regular',P['muted'])
sects=[('FINTECH',[20,15,138],173),('INTERNET SOFTWARE',[13,20,119],152),('E-COMMERCE',[12,16,47],75)]
for k,(lab,vals,total) in enumerate(sects):
 y0=693+k*67
 text(82,y0-2,lab,17,'SemiBold')
 text(1019,y0-2,str(total),23,'Bold',P['white'])
 xx=357;maxwidth=624
 rr((xx,y0,xx+maxwidth,y0+23),fill=(36,48,73),outline=None,radius=5)
 cur=xx
 for val,c in zip(vals,[P['pink'],P['amber'],P['cyan']]):
  dw=round(maxwidth*val/173)
  d.rectangle((cur,y0,cur+dw,y0+23),fill=c)
  cur+=dw
# legend
for x0,c,lab in [(82,P['pink'],'2019'),(202,P['amber'],'2020'),(319,P['cyan'],'2021')]:
 d.rounded_rectangle((x0,881,x0+12,893),radius=3,fill=c)
 text(x0+21,879,lab,16,'Regular',P['muted'])
# annual acceleration panel
rr((1131,598,1172,633),fill=(56,41,68),outline=None,radius=8)
text(1140,604,'02',18,'Bold',P['pink'])
text(1191,600,'The 2021 acceleration',26,'Bold')
text(1131,641,'Annual new unicorns: top three sectors + the rest',15,'Regular',P['muted'])
for ix,(year,total,top) in enumerate([(2019,104,45),(2020,108,51),(2021,520,304)]):
 yy=698+ix*65
 text(1131,yy-1,str(year),21,'SemiBold',P['muted'])
 rr((1229,yy,1750,yy+28),fill=(33,47,75),outline=None,radius=5)
 cursor=1229
 for amount,color in [(top,P['pink']),(total-top,P['inactive'])]:
  width=round(521*amount/520)
  d.rectangle((cursor,yy,cursor+width,yy+28),fill=color);cursor+=width
 text(1775,yy-1,str(total),25,'Bold')
# lower insights band
rr((56,943,1864,1033),fill=(35,29,51),outline=(85,60,83),radius=15)
text(84,955,'THE SIGNAL',16,'Bold',P['pink'])
text(84,978,'400 of 732 new unicorns originated in three industries.',28,'Bold',P['white'])
text(1262,955,'DATA NOTE',15,'Bold',P['amber'])
text(1262,977,'Cross-sectional 2022 snapshot, not',16,'Regular',P['muted'])
text(1262,997,'a current market or returns dataset.',16,'Regular',P['muted'])
# footer
text(60,1045,'SQL  /  PYTHON  /  POWER BI  •  EDUCATIONAL PORTFOLIO STUDY',13,'SemiBold',P['dim'])
img.save(ROOT/'charts/LinkedIn_Dashboard_Preview.png',optimize=True)
print('Saved',ROOT/'charts/LinkedIn_Dashboard_Preview.png',img.size)
