"""Builds the SCO_DATA rows for the State Controller tab (calendar 2024).
Faculty selection = general rules (titles, else salary-schedule range) or the district rule in overrides.RULES.
Per district: mean (headline), median, family (90th percentile, about the family-tier amount),
structure (flat if 70%+ of nonzero contributions are within 10% of the 90th percentile, else tiered),
share with no contribution. North Orange County: adds the $3,646 fringe benefit allowance it pays as
compensation (OtherPay in the file) to every figure.
Run: python3 build_sco.py   (prints JS rows; pass --check to compare with the rows now in index.html)
"""
import sys, re, csv, json, collections, statistics as st, io, contextlib
from load import load
with contextlib.redirect_stdout(io.StringIO()):
    import overrides
D = load('2024')
ALIAS = {'Gavilan': 'Gavilan Joint', 'San Mateo County': 'San Mateo', 'Sonoma County Junior College District': 'Sonoma', 'Sonoma County': 'Sonoma',
         'South Orange County': 'South Orange', 'Ventura County': 'Ventura', 'Foothill-De Anza': 'Foothill-DeAnza', 'San Luis Obispo County': 'San Luis Obispo'}
FAC = re.compile(r'instructor|faculty|professor|counselor|librarian|teacher|academic|\binstr\b|\bAFT F/T', re.I)
NOT = re.compile(r'adjunct|\badj\b|part[- ]?time|\bpt\b|p/t|hourly|stipend|release time|department c|substitute|overload|temp|community ed|non-?credit hourly|summer|intersession|stipend|assistant to|dean|director|manager|aide|technician|specialist|coordinator, class', re.I)
FTEF = {r['district']: float(r['fall2024_ft_ftef']) for r in csv.DictReader(open('sco_2024_ft_faculty_health.csv'))}
SKIP = {'San Mateo', 'Ventura'}
ALLOWANCE = {'North Orange County': 3646}

def select(k, v, ftef):
    if k in overrides.RULES:
        _, method, pred = overrides.RULES[k]
        return [r for r in v if pred(r)], method
    fac = [r for r in v if FAC.search(r['Position']) and not NOT.search(r['Position']) and r['TotalWages'] >= 65000]
    method = 'titles'
    if len(fac) / ftef < 0.8:
        rng = collections.Counter((r['MinPositionSalary'], r['MaxPositionSalary']) for r in fac)
        fr = {k2 for k2, c in rng.items() if c >= 3 and k2[1] > 0}
        if not fr:
            rng = collections.Counter((r['MinPositionSalary'], r['MaxPositionSalary']) for r in v if r['TotalWages'] >= 65000 and re.search(r'^(English|Math|Mathematics|Biology|History|Chemistry|Psychology)\b', r['Position']))
            fr = {k2 for k2, c in rng.items() if c >= 3 and k2[1] > 0}
        ext = [r for r in v if (r['MinPositionSalary'], r['MaxPositionSalary']) in fr and r['TotalWages'] >= 65000 and not NOT.search(r['Position'])]
        if len(ext) > len(fac): fac, method = ext, 'salary range'
    return fac, method

out = []
for k, v in sorted(D.items()):
    name = ALIAS.get(k, k)
    if name in SKIP or name not in FTEF: continue
    ftef = FTEF[name]
    fac, method = select(k, v, ftef)
    if not fac: continue
    ratio = len(fac) / ftef
    if k not in overrides.RULES and not (0.75 <= ratio <= 1.30): continue
    add = ALLOWANCE.get(name, 0)
    h = sorted(r['HealthDentalVision'] + add for r in fac)
    nz = [x for x in h if x > add]
    p90 = h[int(len(h) * 0.9)]
    flat = sum(abs(x - p90) <= 0.10 * p90 for x in nz) / len(nz) >= 0.70
    out.append(dict(name=name, n=len(fac), ftef=ftef, mean=round(st.mean(h)), median=round(st.median(h)), family=round(p90),
                    zero=round(sum(x <= add for x in h) / len(h), 3), structure='flat' if flat else 'tiered', method=method,
                    **({'allowance': add} if add else {})))
if '--check' in sys.argv:
    s = open('/home/claude/cc-benefits-comparison/index.html').read()
    cur = {d['name']: d for d in json.loads('[' + re.search(r'const SCO_DATA = \[\n([\s\S]*?)\n\];', s).group(1).rstrip(',') + ']')}
    new = {d['name']: d for d in out}
    print('only in site:', sorted(set(cur) - set(new)), '| only in build:', sorted(set(new) - set(cur)))
    for n_, d in new.items():
        c = cur.get(n_)
        if c and (c['n'], c['median'], c['mean']) != (d['n'], d['median'] - d.get('allowance', 0), d['mean'] - d.get('allowance', 0)): print('DIFF', n_, c, d)
for d in sorted(out, key=lambda d: -d['mean']): print('  ' + json.dumps(d) + ',')
