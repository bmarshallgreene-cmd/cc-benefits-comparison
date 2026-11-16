import sys; sys.path.insert(0,'/home/claude/work/sco')
from load import load
import collections,statistics as st,re,json,csv,subprocess
D=load('2024')
js=subprocess.run(['node','-e',r"""
const h=require('fs').readFileSync('/home/claude/cc-benefits-comparison/index.html','utf8');const g=re=>h.match(re)[0];
eval(g(/const CCFS_YEARS = \{[\s\S]*?\n\};/).replace('const CCFS_YEARS','global.Y'));
eval(g(/const ACCCA_DATA = \[[\s\S]*?\n\];/).replace('const ACCCA_DATA','global.A'));
eval(g(/const YFA_RAW = \[[\s\S]*?\n\];/).replace('const YFA_RAW','global.R'));
eval(g(/const YFA_TO_CCFS = \{[\s\S]*?\};/).replace('const YFA_TO_CCFS','global.M'));
console.log(JSON.stringify({Y:Y['2024-25'],A,R,M}))"""],capture_output=True,text=True).stdout
S=json.loads(js)
site={d['name']:d for d in S['Y']}
yfa={S['M'].get(r[0],r[0]):r for r in S['R']}
acc={a['ccfs']:a for a in S['A']}
ALIAS={'Gavilan':'Gavilan Joint','San Mateo County':'San Mateo','Sonoma County Junior College District':'Sonoma','Sonoma County':'Sonoma','South Orange County':'South Orange','Ventura County':'Ventura','Foothill-De Anza':'Foothill-DeAnza','San Luis Obispo County':'San Luis Obispo','Siskiyous':'Siskiyou','Sierra':'Sierra','Pasadena Area':'Pasadena','Butte-Glenn':'Butte','North Orange County':'North Orange County','Napa Valley':'Napa Valley','West Valley-Mission':'West Valley-Mission','Monterey Peninsula':'Monterey Peninsula'}
FAC=re.compile(r'instructor|faculty|professor|counselor|librarian|teacher|academic|\binstr\b|\bAFT F/T',re.I)
NOT=re.compile(r'adjunct|\badj\b|part[- ]?time|\bpt\b|p/t|hourly|stipend|release time|department c|substitute|overload|temp|community ed|non-?credit hourly|summer|intersession|stipend|assistant to|dean|director|manager|aide|technician|specialist|coordinator, class',re.I)
out=[]
for k,v in sorted(D.items()):
    name=ALIAS.get(k,k); s=site.get(name)
    if not s: print('NO SITE MATCH',k); continue
    fac=[r for r in v if FAC.search(r['Position']) and not NOT.search(r['Position']) and r['TotalWages']>=65000]
    method='titles'
    if len(fac)/s['ftef']<0.8:
        # Some districts title faculty by discipline. Use the faculty salary-schedule range instead:
        # any range shared by 3+ title-matched rows marks faculty; take all rows in those ranges.
        rng=collections.Counter((r['MinPositionSalary'],r['MaxPositionSalary']) for r in fac)
        fr={k2 for k2,c in rng.items() if c>=3 and k2[1]>0}
        if not fr:
            rng=collections.Counter((r['MinPositionSalary'],r['MaxPositionSalary']) for r in v if r['TotalWages']>=65000 and re.search(r'^(English|Math|Mathematics|Biology|History|Chemistry|Psychology)\b',r['Position']))
            fr={k2 for k2,c in rng.items() if c>=3 and k2[1]>0}
        ext=[r for r in v if (r['MinPositionSalary'],r['MaxPositionSalary']) in fr and r['TotalWages']>=65000 and not NOT.search(r['Position'])]
        if len(ext)>len(fac): fac=ext; method='salary range'
    if not fac: out.append(dict(name=name,n=0)); continue
    h=[r['HealthDentalVision'] for r in fac]; pos=[x for x in h if x>0]
    mode=collections.Counter(round(x) for x in pos).most_common(1)[0] if pos else (0,0)
    out.append(dict(name=name,method=method,n=len(fac),ftef=s['ftef'],ratio=len(fac)/s['ftef'],mean=st.mean(h),median=st.median(h),zeros=sum(x==0 for x in h)/len(h),
        mode=mode[0],modeshare=mode[1]/len(h),distinct=len(set(round(x) for x in pos)),
        full=s['hw']/s['adjFtef'],alloc=(s['allocHw']/s['adjFtef']) if s.get('allocHw') and not s.get('allocExcluded') else None,
        yfa=(yfa.get(name) or [None,None])[1], yfamax=(yfa.get(name) or [None,None,None])[2], accca=(acc.get(name) or {}).get('y25'),
        distHDV=sum(r['HealthDentalVision'] for r in v)))
json.dump(out,open('sco_test.json','w'),indent=1)
print(f"{'district':22}{'n':>5}{'FTEF':>7}{'n/FTEF':>7}{'mean':>8}{'median':>8}{'zero%':>6}{'distinct':>9}{'modeshr':>8} |{'YFA avg':>8}{'YFAmax':>8}{'ACCCA':>7}{'Alloc':>8}{'Full':>8}")
f=lambda x,w=8: f"{x:>{w},.0f}" if x is not None else ' '*(w-1)+'-'
for o in out:
    if o['n']==0: print(f"{o['name']:22}    0  (no faculty titles matched)"); continue
    print(f"{o['name']:22}{o['method'][:6]:7}{o['n']:>5}{o['ftef']:>7.0f}{o['ratio']:>7.2f}{f(o['mean'])}{f(o['median'])}{o['zeros']*100:>6.0f}{o['distinct']:>9}{o['modeshare']:>8.2f} |{f(o['yfa'])}{f(o['yfamax'])}{f(o['accca'],7)}{f(o['alloc'])}{f(o['full'])}")
