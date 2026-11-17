import sys, io, contextlib, csv, json, re, statistics as st
sys.path.insert(0,'/home/claude/cc-benefits-comparison/data/analysis/sco'); sys.argv=['x']
import os; os.chdir('/home/claude/cc-benefits-comparison/data/analysis/sco')
with contextlib.redirect_stdout(io.StringIO()):
    import build_sco as B
from load import load
D=load('2023')
FON={r['district']:float(r['ft_ftef']) for r in csv.DictReader(open('../../fon/fon_fall2023.csv'))}
A2={'Butte-Glenn':'Butte','Pasadena Area':'Pasadena','Sonoma County':'Sonoma','South Orange County':'South Orange','Foothill-De Anza':'Foothill-DeAnza'}
FON={A2.get(k,k):v for k,v in FON.items()}
ALIAS=dict(B.ALIAS); ALIAS.update({'Butte-Glenn':'Butte','Pasadena Area':'Pasadena','Peralta':'Peralta','Siskiyous':'Siskiyou','Siskiyou Joint':'Siskiyou','San Francisco':'San Francisco','Mendocino-Lake':'Mendocino-Lake','Monterey Peninsula':'Monterey Peninsula','Napa Valley':'Napa Valley','Long Beach':'Long Beach','Sierra Joint':'Sierra'})
s=open('/home/claude/cc-benefits-comparison/index.html').read()
cur={d['name']:d for d in json.loads('['+re.search(r'const SCO_DATA = \[\n([\s\S]*?)\n\];',s).group(1).rstrip().rstrip(',')+']')}
out={}
print(f"{'district (2023 file)':28}{'site name':20}{'n':>5}{'FTEF23':>7}{'ratio':>6}{'mean23':>8}{'med23':>8}{'zero':>6} | {'2024 site':>9} {'meth':6}{'chg':>7}")
for k,v in sorted(D.items()):
    name=ALIAS.get(k,k)
    ftef=FON.get(name)
    if not ftef: print('  no FON match:',k); continue
    try: fac,m=B.select(k,v,ftef)
    except Exception as e: print('  err',k,e); continue
    allh=[r['HealthDentalVision'] for r in fac]; h=sorted(x for x in allh if x>0)
    if not h: print(f"{k[:28]:28}{name[:20]:20}{len(fac):>5}{ftef:>7.0f}  no nonzero health"); out[name]=dict(n=len(fac),zeroall=True); continue
    mean=st.mean(h); c=cur.get(name)
    chg=(c['mean']/mean-1) if c else None
    out[name]=dict(n=len(fac),ftef=ftef,ratio=len(fac)/ftef,mean=round(mean),median=round(st.median(h)),family=round(h[int(len(h)*.9)]),zero=round(1-len(h)/len(allh),3),method=m)
    print(f"{k[:28]:28}{name[:20]:20}{len(fac):>5}{ftef:>7.0f}{len(fac)/ftef:>6.2f}{mean:>8,.0f}{st.median(h):>8,.0f}{1-len(h)/len(allh):>6.2f} | {c['mean'] if c else '-':>9} {(c['method'] if c else ''):6}{'' if chg is None else f'{chg*100:+.1f}%':>7}")
json.dump(out,open('/tmp/claude-0/-home-claude/85f4a401-00ee-59f3-bc18-be80bc7096e4/scratchpad/y2023.json','w'),indent=1)
print('districts in 2023 file:',len(D)); print('site districts not in 2023 file:',sorted(set(cur)-set(out)))
