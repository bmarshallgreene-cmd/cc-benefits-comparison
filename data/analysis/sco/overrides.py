"""District-specific rules for districts the general title/salary-range rules in analyze.py could not fit.
Run: python3 overrides.py   (prints the rows added to SCO_DATA in index.html)
"""
from load import load
import re, statistics as st, json
D = load('2024')
ADM = re.compile(r'dean|director|manager|president|chancellor|supervisor|chief|provost|analyst|controller', re.I)
FACISH = re.compile(r'facul|instr|counsel|librar|^ol-|overload|coach', re.I)
RULES = {
 # Full-time faculty are listed under hourly/overload/adjunct titles; true adjuncts above $65k have no benefits.
 # Faculty-type titles with total pay of $90,000 or more gives 442 rows against 443 FT FTEF.
 'Mt. San Antonio': (443.0, 'titles + pay', lambda r: FACISH.search(r['Position']) and r['TotalWages'] >= 90000 and not ADM.search(r['Position'])),
 # Faculty are titled by discipline; the two faculty salary-schedule ranges identify them.
 'Riverside': (497.7, 'salary range', lambda r: (r['MinPositionSalary'], r['MaxPositionSalary']) in {(80825.0, 173355.0), (85417.0, 183205.0)}
               and r['TotalWages'] >= 65000 and not ADM.search(r['Position']) and 'Part-Time' not in r['Position']),
 # Titles are "Faculty Full Time" / "Faculty Part Time"; many full-timers carry the part-time title.
 'San Luis Obispo County': (137.3, 'titles', lambda r: r['Position'].startswith('Faculty') and r['TotalWages'] >= 65000),
 # Faculty are titled by discipline; STRS members on faculty-schedule ranges. Matches only 63% of FT FTEF.
 'Solano': (134.0, 'salary range', lambda r: 60000 <= r['MinPositionSalary'] <= 75000 and 118000 <= r['MaxPositionSalary'] <= 160000
            and r['TotalWages'] >= 65000 and r['PensionFormula'] in ('2@60', '2@62') and not ADM.search(r['Position'])),
}
NAME = {'San Luis Obispo County': 'San Luis Obispo'}
for k, (ftef, method, pred) in RULES.items():
    h = [r['HealthDentalVision'] for r in D[k] if pred(r)]
    print(json.dumps(dict(name=NAME.get(k, k), n=len(h), ftef=ftef, median=round(st.median(h)), mean=round(st.mean(h)),
                          zero=round(sum(x == 0 for x in h) / len(h), 3), method=method)) + ',')
