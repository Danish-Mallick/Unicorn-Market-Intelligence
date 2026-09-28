"""Generate a portable one-page Power BI Project (.pbip) with four Web CSV sources.
The native report has NOT been opened in Windows Power BI Desktop in this environment.
"""
from pathlib import Path
import json,uuid,hashlib
root=Path(__file__).resolve().parents[1]
base=root/'powerbi';name='Unicorn_Market_Intelligence'
md=base/(name+'.SemanticModel');rd=base/(name+'.Report');M=md/'definition';R=rd/'definition'
F='https://developer.microsoft.com/json-schemas/fabric/'
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')
def j(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def gid(t):return hashlib.sha1(t.encode()).hexdigest()[:20]
def plat(typ):return {'$schema':F+'gitIntegration/platformProperties/2.0.0/schema.json','metadata':{'type':typ,'displayName':'Unicorn Market Intelligence'},'config':{'version':'2.0','logicalId':str(uuid.uuid4())}}
j(base/(name+'.pbip'),{'$schema':F+'pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}], 'settings':{'enableAutoRecovery':True}})
j(rd/'.platform',plat('Report'));j(md/'.platform',plat('SemanticModel'))
j(rd/'definition.pbir',{'$schema':F+'item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}})
j(md/'definition.pbism',{'$schema':F+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'4.2','settings':{'qnaEnabled':True}})
write(M/'database.tmdl','database\n\tcompatibilityLevel: 1600\n')
write(M/'model.tmdl',"model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\nref table Unicorns\n\nannotation __PBI_TimeIntelligenceEnabled = 0\n")
cols={'Company_ID':'int64','Company':'string','City':'string','Country':'string','Continent':'string','Industry':'string','Date_Joined':'dateTime','Year_Joined':'int64','Year_Founded':'int64','Valuation_USD':'int64','Funding_USD':'int64','Valuation_Billions':'double','Time_To_Unicorn':'int64'}
s='table Unicorns\n\tlineageTag: '+str(uuid.uuid4())+'\n\n'
for k,t in cols.items():
 s+='\tcolumn '+k+'\n\t\tdataType: '+t+'\n\t\tlineageTag: '+str(uuid.uuid4())+'\n\t\tsummarizeBy: '+('none' if k in ('Company_ID','Year_Joined','Year_Founded','Time_To_Unicorn') or t=='string' else 'sum')+'\n\t\tsourceColumn: '+k+'\n\n'
measures={
 'Company Count':'DISTINCTCOUNT(Unicorns[Company_ID])',
 'New Unicorns 2019-21':'CALCULATE([Company Count], KEEPFILTERS(Unicorns[Year_Joined] >= 2019), KEEPFILTERS(Unicorns[Year_Joined] <= 2021))',
 'Top Three New Unicorns':'CALCULATE([New Unicorns 2019-21], KEEPFILTERS(Unicorns[Industry] IN {"Fintech", "Internet software & services", "E-commerce & direct-to-consumer"}))',
 'Top Three Share':'DIVIDE([Top Three New Unicorns], [New Unicorns 2019-21])',
 'Avg Snapshot Valuation ($B)':'AVERAGE(Unicorns[Valuation_Billions])',
 'Avg Top Three Snapshot Valuation ($B)':'CALCULATE([Avg Snapshot Valuation ($B)], KEEPFILTERS(Unicorns[Industry] IN {"Fintech", "Internet software & services", "E-commerce & direct-to-consumer"}), KEEPFILTERS(Unicorns[Year_Joined] >= 2019), KEEPFILTERS(Unicorns[Year_Joined] <= 2021))',
 'Total Historical Snapshot Valuation ($B)':'SUM(Unicorns[Valuation_Billions])',
 'Avg Years To Unicorn':'AVERAGEX(FILTER(Unicorns, Unicorns[Time_To_Unicorn] >= 0), Unicorns[Time_To_Unicorn])'
}
for n,e in measures.items():
 s+='\tmeasure \''+n.replace("'","''")+'\' = '+e+'\n\t\tlineageTag: '+str(uuid.uuid4())+'\n'
 s+='\t\tformatString: '+('0.0%' if 'Share' in n else ('#,0' if 'Count' in n or 'Unicorns' in n else '#,0.00'))+'\n\n'
# Data lives at the source; use four original, separate CSVs so it remains fully reproducible.
m='''let
    Base = "https://raw.githubusercontent.com/ShaikhBorhanUddin/Unicorn_Company_Analysis/main/Dataset/",
    SourceCSV = (filename as text) as table =>
        Table.PromoteHeaders(
            Csv.Document(Web.Contents(Base & filename),
                [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            [PromoteAllScalars=true]),
    Companies = Table.TransformColumnTypes(SourceCSV("companies.csv"),
        {{"company_id", Int64.Type}, {"company", type text}, {"city", type text}, {"country", type text}, {"continent", type text}}),
    Dates = Table.TransformColumnTypes(SourceCSV("dates.csv"),
        {{"company_id", Int64.Type}, {"date_joined", type text}, {"year_founded", Int64.Type}}),
    Funding = Table.TransformColumnTypes(SourceCSV("funding.csv"),
        {{"company_id", Int64.Type}, {"valuation", Int64.Type}, {"funding", Int64.Type}, {"select_investors", type text}}),
    Industries = Table.TransformColumnTypes(SourceCSV("industries.csv"),
        {{"company_id", Int64.Type}, {"industry", type text}}),
    JoinDates = Table.NestedJoin(Companies, {"company_id"}, Dates, {"company_id"}, "d", JoinKind.Inner),
    ExpandDates = Table.ExpandTableColumn(JoinDates, "d", {"date_joined", "year_founded"}),
    JoinFunding = Table.NestedJoin(ExpandDates, {"company_id"}, Funding, {"company_id"}, "f", JoinKind.Inner),
    ExpandFunding = Table.ExpandTableColumn(JoinFunding, "f", {"valuation", "funding"}),
    JoinIndustry = Table.NestedJoin(ExpandFunding, {"company_id"}, Industries, {"company_id"}, "i", JoinKind.Inner),
    ExpandIndustry = Table.ExpandTableColumn(JoinIndustry, "i", {"industry"}),
    CleanIndustry = Table.TransformColumns(ExpandIndustry, {{"industry", each Text.Replace(_, Character.FromNumber(34), ""), type text}}),
    AddDate = Table.AddColumn(CleanIndustry, "Date_Joined", each Date.FromText([date_joined], [Format="dd/MM/yyyy", Culture="en-GB"]), type date),
    AddYear = Table.AddColumn(AddDate, "Year_Joined", each Date.Year([Date_Joined]), Int64.Type),
    AddBillions = Table.AddColumn(AddYear, "Valuation_Billions", each [valuation] / 1000000000, type number),
    AddTenure = Table.AddColumn(AddBillions, "Time_To_Unicorn", each [Year_Joined] - [year_founded], Int64.Type),
    Rename = Table.RenameColumns(AddTenure, {{"company_id","Company_ID"},{"company","Company"},{"city","City"},{"country","Country"},{"continent","Continent"},{"industry","Industry"},{"year_founded","Year_Founded"},{"valuation","Valuation_USD"},{"funding","Funding_USD"}}),
    Final = Table.SelectColumns(Rename, {"Company_ID","Company","City","Country","Continent","Industry","Date_Joined","Year_Joined","Year_Founded","Valuation_USD","Funding_USD","Valuation_Billions","Time_To_Unicorn"})
in
    Final'''
s+='\tpartition Unicorns = m\n\t\tmode: import\n\t\tsource =\n'+'\n'.join('\t\t\t\t'+line for line in m.splitlines())+'\n\n\tannotation PBI_ResultType = Table\n'
write(M/'tables/Unicorns.tmdl',s)
write(base/'dax_measures.dax','\n\n'.join('-- '+n+'\n'+n+' = '+e for n,e in measures.items()))
PA={'bg':'#0B1223','panel':'#192840','white':'#F7F8FF','muted':'#A0B0CF','pink':'#FA7DAC','amber':'#FFC77B','cyan':'#5BDECE','purple':'#8D9BFA'}
theme={'name':'UnicornNoir','dataColors':[PA['pink'],PA['cyan'],PA['amber'],PA['purple'],'#6C7A9D'], 'foreground':PA['white'],'foregroundNeutralSecondary':PA['muted'],'background':PA['bg'],'backgroundLight':PA['panel'],'tableAccent':PA['pink'],'good':PA['cyan'],'neutral':PA['amber'],'bad':'#ED6080','textClasses':{'callout':{'fontSize':28,'fontFace':'Segoe UI Semibold','color':PA['white']},'title':{'fontSize':12,'fontFace':'Segoe UI Semibold','color':PA['white']},'header':{'fontSize':12,'fontFace':'Segoe UI Semibold','color':PA['white']},'label':{'fontSize':11,'fontFace':'Segoe UI','color':PA['muted']}}}
j(base/'power_bi_theme.json',theme);j(rd/'StaticResources/SharedResources/BaseThemes/UnicornNoir.json',theme)
SC=F+'item/report/definition/'
j(R/'version.json',{'$schema':SC+'versionMetadata/1.0.0/schema.json','version':'2.0.0'})
j(R/'report.json',{'$schema':SC+'report/3.2.0/schema.json','themeCollection':{'baseTheme':{'name':'UnicornNoir','reportVersionAtImport':{'visual':'2.6.0','report':'3.1.0','page':'2.3.0'},'type':'SharedResources'}},'resourcePackages':[{'name':'SharedResources','type':'SharedResources','items':[{'name':'UnicornNoir','path':'BaseThemes/UnicornNoir.json','type':'BaseTheme'}]}], 'settings':{'useStylableVisualContainerHeader':True,'exportDataMode':'AllowSummarized','defaultDrillFilterOtherVisuals':True}})
pg=gid('unicorn_dashboard_overview');j(R/'pages/pages.json',{'$schema':SC+'pagesMetadata/1.0.0/schema.json','pageOrder':[pg],'activePageName':pg})
def lit(x):return {'expr':{'Literal':{'Value':x}}}
def scol(c):return {'solid':{'color':lit("'"+c+"'")}}
j(R/f'pages/{pg}/page.json',{'$schema':SC+'page/2.1.0/schema.json','name':pg,'displayName':'Unicorn Growth Overview','displayOption':'FitToPage','width':1440,'height':850,'objects':{'background':[{'properties':{'color':scol(PA['bg']),'transparency':lit('0D')}}],'outspace':[{'properties':{'color':scol(PA['bg'])}}]}})
def C(k):return {'Column':{'Expression':{'SourceRef':{'Entity':'Unicorns'}},'Property':k}}
def ME(k):return {'Measure':{'Expression':{'SourceRef':{'Entity':'Unicorns'}},'Property':k}}
visual_ct=0
def draw(key,typ,x,y,w,h,roles=None,msg=None,size='13pt',bg=None,title=None,color=None):
 global visual_ct
 visual_ct+=1;vid=gid(pg+key);v={'visualType':typ,'drillFilterOtherVisuals':typ!='textbox'}
 if roles:v['query']={'queryState':{role:{'projections':[{'field':f,'queryRef':'Unicorns.'+(f.get('Column') or f.get('Measure'))['Property'],'nativeQueryRef':(f.get('Column') or f.get('Measure'))['Property']} for f in fields]} for role,fields in roles.items()}}
 if typ=='textbox':v['objects']={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':msg,'textStyle':{'fontFamily':'Segoe UI','fontSize':size,'fontWeight':'bold' if title else 'normal','color':color or PA['white']}}],'horizontalTextAlignment':'left'}]}}]}
 if typ!='textbox':
  v['visualContainerObjects']={'background':[{'properties':{'show':lit('true'),'color':scol(bg or PA['panel']),'transparency':lit('0D')}}],'visualHeader':[{'properties':{'show':lit('false')}}]}
  if title:v['visualContainerObjects']['title']=[{'properties':{'show':lit('true'),'text':lit("'"+title.replace("'","''")+"'"),'fontColor':scol(PA['white'])}}]
 j(R/f'pages/{pg}/visuals/{vid}/visual.json',{'$schema':SC+'visualContainer/2.7.0/schema.json','name':vid,'position':{'x':x,'y':y,'width':w,'height':h,'z':1000+visual_ct,'tabOrder':1000+visual_ct},'visual':v})
# Designed Power BI page: restrained one-page editorial visual hierarchy.
draw('eyebrow','textbox',42,14,880,28,msg='THE BILLION-DOLLAR CLUB  /  HISTORICAL MARKET INTELLIGENCE',size='11pt',color=PA['pink'],title=True)
draw('title','textbox',42,46,1280,57,msg='Where did the unicorn boom take shape?',size='29pt',title=True)
draw('subtitle','textbox',42,113,1314,41,msg='Industry emergence, geography and snapshot valuations  •  Educational analysis; historical ~2022 dataset',size='11pt',color=PA['muted'])
for ix,(measure,label) in enumerate([('New Unicorns 2019-21','NEW UNICORNS'),('Top Three New Unicorns','TOP THREE INDUSTRIES'),('Top Three Share','TOP-THREE SHARE'),('Avg Top Three Snapshot Valuation ($B)','AVG SNAPSHOT VALUE ($B)')]):
 x=42+ix*351
 draw('lbl'+str(ix),'textbox',x,177,290,25,msg=label,size='10pt',color=PA['muted'],title=True)
 draw('kpi'+str(ix),'cardVisual',x,203,317,99,roles={'Data':[ME(measure)]})
draw('sect_title','textbox',42,332,710,39,msg='01  Top industries by new unicorns',size='18pt',title=True)
draw('sector','barChart',42,374,671,322,roles={'Category':[C('Industry')],'Y':[ME('Top Three New Unicorns')]},title='2019–2021 · companies reaching $1B')
draw('years_title','textbox',742,332,640,39,msg='02  New unicorns by year',size='18pt',title=True)
draw('annual','columnChart',742,374,650,322,roles={'Category':[C('Year_Joined')],'Y':[ME('New Unicorns 2019-21')]},title='Annual new unicorns · all industries')
draw('location','slicer',42,722,355,98,roles={'Values':[C('Continent')]})
draw('industry','slicer',420,722,355,98,roles={'Values':[C('Industry')]})
draw('note','textbox',812,720,585,108,msg='Data interpretation: valuations are from the approximate 2022 source snapshot. Historical counts are not investment returns; no 2026 market claims.',size='11pt',color=PA['muted'])
print('Generated PBIP pages=1 visuals=',visual_ct)
