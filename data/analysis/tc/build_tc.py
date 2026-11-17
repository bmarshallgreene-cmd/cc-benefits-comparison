"""State Controller tab rows for districts missing from the State Controller file, estimated from
Transparent California 2024 payroll (scraped Nov 17, 2026; compact copies in raw/: title, base pay, other pay,
total benefits, total pay for every record with total pay >= $60,000).

Transparent California's "Total Benefits" equals the State Controller's pension + health fields for districts
in both sources (checked on Yosemite). Health is estimated per person as total benefits - 19.1% x total pay
(the CalSTRS employer rate). Tested on the 44 State Controller districts where the true answer is known:
median error 2.5%, 33 of 44 within 5% (data/analysis/sco, Nov 17).

Faculty: titles as in est.py, total pay >= $65,000. "Covered" = estimate >= $3,000 (below that is estimation
noise or dental/vision only). Figures: mean, median, family-level (90th percentile) among covered faculty.
Run: python3 build_tc.py   (prints the JS rows)
"""
import re, json, statistics as st, est
est.FON['Pasadena'] = est.FON['Pasadena Area']
est.FON.setdefault('Butte', est.FON.get('Butte-Glenn'))
EXCLUDE = {  # benefits field is not pension + health
    'Peralta': 'Transparent California benefits average about $4,500 and leave out pension and most health.',
    'Butte': 'Transparent California benefits run about 50% of pay, so they include costs other than pension and health.',
    'Yuba': 'Transparent California benefits leave out pension for half of faculty, so health cannot be separated out.'}
LOWCONF = {
    'San Francisco': 'Family-level estimate is well below the ACCCA survey figure; treat as approximate.',
    'Lake Tahoe': 'Small district and 11% of faculty records do not fit the pension-plus-health pattern; treat as approximate.',
    'Siskiyou': 'Small district with no clear tier pattern; well below the ACCCA survey figure; treat as approximate.',
    'Copper Mountain': 'Only 26 faculty and no clear tier pattern; treat as approximate.',
    'San Mateo': 'About a quarter of full-time faculty show only about $1,500 (dental and vision); they are treated as having declined medical coverage.'}
EXTRA_NOT = {'Santa Barbara': re.compile(r'^Instructor$|^Counselor$')}  # part-time faculty titles there
NAMES = ['San Diego','Long Beach','Hartnell','Monterey Peninsula','San Joaquin Delta','Cabrillo','Santa Barbara','San Francisco','Peralta','Butte',
         'Southwestern','West Hills','Copper Mountain','Citrus','Mendocino-Lake','San Mateo','Victor Valley','Siskiyou','Sierra','Lassen',
         'Lake Tahoe','Napa Valley','Yuba','Ventura','San Bernardino','Antelope Valley','Pasadena']
out = []
for n in NAMES:
    if n in EXCLUDE: continue
    R = est.rows(n)
    if n in EXTRA_NOT: R = [r for r in R if not EXTRA_NOT[n].search(r[0])]
    e = [r[5] for r in R]; h = sorted(x for x in e if x >= 3000)
    p90 = h[int(len(h) * 0.9)]
    flat = sum(abs(x - p90) <= 0.10 * p90 for x in h) / len(h) >= 0.70
    d = dict(name=n, n=len(R), ftef=est.FON[n], mean=round(st.mean(h)), median=round(st.median(h)), family=round(p90),
             zero=round(1 - len(h) / len(e), 3), covered=len(h), structure='flat' if flat else 'tiered', method='tc')
    if n in LOWCONF: d['caution'] = LOWCONF[n]
    out.append(d)
if __name__ == '__main__':
    for d in sorted(out, key=lambda d: -d['mean']): print('  ' + json.dumps(d) + ',')
    print('// excluded:', json.dumps(EXCLUDE))
