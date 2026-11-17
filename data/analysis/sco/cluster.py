import sys; sys.path.insert(0,'/home/claude/cc-benefits-comparison/data/analysis/sco')
from load import load
import collections,re,statistics as st,json
D=load('2024')
FAC=re.compile(r'instructor|faculty|professor|counselor|librarian|teacher|academic|\binstr\b|\bAFT F/T',re.I)
NOT=re.compile(r'adjunct|\badj\b|part[- ]?time|\bpt\b|p/t|hourly|stipend|release time|department c|substitute|overload|temp|community ed|non-?credit hourly|summer|intersession|assistant to|dean|director|manager|aide|technician|specialist|coordinator, class',re.I)
T=['Cerritos','Feather River','Foothill','Glendale','Imperial','Los Angeles','Los Rios','MiraCosta','North Orange County','Ohlone','Redwoods','Rio Hondo','Santa Clarita','Sonoma County']
res={}
for k,v in sorted(D.items()):
    if not any(k.startswith(t) for t in T): continue
    fac=[r for r in v if FAC.search(r['Position']) and not NOT.search(r['Position']) and r['TotalWages']>=65000]
    allft=[r for r in v if r['TotalWages']>=50000]
    for lab,rows in (('fac',fac),('allFT',allft)):
        h=[round(r['HealthDentalVision']) for r in rows if r['HealthDentalVision']>0]
        if not h: print(k,lab,'none'); continue
        c=collections.Counter(h); top=c.most_common(6)
        # tolerance clusters: within $25
        t5=sum(n for _,n in c.most_common(5))/len(h)
        print(f"{k:22}{lab:6} n={len(h):4} distinct={len(c):4} top5share={t5:.2f} med={st.median(h):,.0f}  top: "+', '.join(f"{a:,}x{n}" for a,n in top))
        res[k+'|'+lab]=dict(n=len(h),distinct=len(c),top5=t5,top=top)
json.dump(res,open('cluster.json','w'))  # run from a scratch directory
