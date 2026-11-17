import json,sys,re,collections,statistics as st,csv
FON={r['district']:float(r['ft_ftef']) for r in csv.DictReader(open(''+__import__('os').path.join(__import__('os').path.dirname(__file__),'..','..','fon','fon_fall2024.csv')+''))}
FAC=re.compile(r'instructor|faculty|professor|counselor|librarian|\bcontract\b|department head|coach|department chair|\binstr\b',re.I)
NOT=re.compile(r'adjunct|\badj\b|part[- ]?time|\bpt\b|p/t|hourly|stipend|substitute|overload|temp|dean|director|manager|aide|assistant(?! ?professor)|associate faculty|equal pay|technician|specialist|coordinator|supervisor|mental health|child dev|\bce\b',re.I)
def rows(n, fac=FAC, notre=NOT, minpay=65000):
    d=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'raw',n+'.json'))); T=d['T']
    return [(T[ti],base,oth,ben,tot,ben-0.191*tot) for ti,base,oth,ben,tot in d['R'] if fac.search(T[ti]) and not notre.search(T[ti]) and tot>=minpay]
def report(n, R, fon=None):
    fon=fon or FON.get(n)
    e=sorted(r[5] for r in R)
    pos=[x for x in e if x>=1000]
    print(f"\n== {n}: n={len(R)} FT FTEF={fon} ratio={len(R)/fon:.2f}" if fon else f"\n== {n}: n={len(R)}")
    if not pos: return
    print('  est deciles',[round(e[int(len(e)*q/10)]) for q in range(10)],'max',round(e[-1]))
    print(f"  mean(est>=1000) {st.mean(pos):,.0f} median {st.median(pos):,.0f} p90 {pos[int(len(pos)*.9)]:,.0f} share<1000 {1-len(pos)/len(e):.2f}")
    b=collections.Counter(round(x/500)*500 for x in pos).most_common(8); print('  clusters ($500 bins):',b)
    print('  titles',collections.Counter(r[0] for r in R).most_common(8))
if __name__=='__main__':
    for n in sys.argv[1:]: report(n, rows(n))
