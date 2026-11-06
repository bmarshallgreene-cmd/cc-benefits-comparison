import csv, json, statistics as st
RATE=0.191+0.0145
ALIAS={'Sonoma':'Sonoma County','Pasadena':'Pasadena Area'}
site=[dict(code=int(c),name=n,ftef=float(f),adj=float(a),ib=float(i),hw=float(h)) for c,n,f,a,i,h in csv.reader(open('site_2024.csv'))]
pull={int(r['code']):r for r in csv.DictReader(open('pull_2025_26.csv'))}
fon={r['district']:r for r in csv.DictReader(open('fon_fall2025.csv'))}
rows=[]
for s in site:
    f=fon[ALIAS.get(s['name'],s['name'])]; p=pull.get(s['code'])
    ded=s['ftef']-s['adj']
    if p:
        ben=float(p['ben_colA']); tis=float(p['tis_colA']); ftef=float(f['ftef'])
        hw=ben-RATE*tis; adj=round(ftef-ded,1); yr='2025-26'
    else:  # not certified for 2025-26: carry 2024-25
        ben=s['ib']; hw=s['hw']; ftef=s['ftef']; adj=s['adj']; tis=None; yr='2024-25 (carried)'
    rows.append(dict(code=s['code'],district=s['name'],data_year=yr,ftef=ftef,adjFtef=adj,
        instrBenefits=round(ben),instrSalaries=round(tis) if tis else '',hw=round(hw,2),
        hw_per_ft=round(hw/adj),basic_per_ft=round(ben/ftef),
        prev_hw_per_ft=round(s['hw']/s['adj']),prev_basic_per_ft=round(s['ib']/s['ftef'])))
for key,rk,prk in [('hw_per_ft','rank','prev_rank')]:
    for r,i in zip(sorted(rows,key=lambda r:-r['hw_per_ft']),range(1,99)): r['rank']=i
    for r,i in zip(sorted(rows,key=lambda r:-r['prev_hw_per_ft']),range(1,99)): r['prev_rank']=i
for r in rows: r['change_pct']=round(100*(r['hw_per_ft']/r['prev_hw_per_ft']-1),1)
rows.sort(key=lambda r:r['rank'])
with open('results_2025_26.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
v=[r['hw_per_ft'] for r in rows]; pv=[r['prev_hw_per_ft'] for r in rows]
print('n',len(rows),'median',round(st.median(v)),'prev',round(st.median(pv)),'mean',round(st.mean(v)),'prev',round(st.mean(pv)))
y=[r for r in rows if r['district']=='Yosemite'][0]; print('Yosemite',y)
print('max',rows[0]['district'],rows[0]['hw_per_ft'],'min',rows[-1]['district'],rows[-1]['hw_per_ft'])
print('biggest moves:')
for r in sorted(rows,key=lambda r:-abs(r['change_pct']))[:8]: print(' ',r['district'],r['prev_hw_per_ft'],'->',r['hw_per_ft'],r['change_pct'],'%','rank',r['prev_rank'],'->',r['rank'])
