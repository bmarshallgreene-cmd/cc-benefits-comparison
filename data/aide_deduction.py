"""Full Methodology aide correction.
Instruction benefits (50% Law schedule, column A, object 3000) include employer pension and
payroll taxes for instructional aides. Estimated and removed here:
  regular-status aides (object 2200): CalPERS + Social Security 6.2% + Medicare 1.45%
  other/hourly aides   (object 2400): Social Security 6.2% + Medicare 1.45% (assumed not CalPERS members)
Aide health benefits cannot be separated and remain in the figure.
Prints JSON {year: {code: {aideDed, src}}}.
"""
import json, sys
P = json.load(open(sys.argv[1]))
PERS = {"2025-26": 0.2681, "2024-25": 0.2705}; KEY = {"2025-26": "17", "2024-25": "16"}
SS, MEDI = 0.062, 0.0145
def n(x):
    x = (x or "").replace(",", "").strip()
    return float(x) if x not in ("", "-") else 0.0
def aides(yr, code):
    v = P.get(f"{KEY[yr]}_{int(code):03d}")
    if not v or "Employee Benefits" not in v: return None
    g = lambda c: n(v[c][2]) if c in v else 0.0
    return g("2200"), g("2400")
out = {}
for yr in PERS:
    out[yr] = {}
    for code in sorted({k.split("_")[1] for k in P}):
        a = aides(yr, code); src = yr
        if a is None and yr == "2025-26": a = aides("2024-25", code); src = "2024-25"
        if a is None: continue
        out[yr][str(int(code))] = dict(aideDed=round(a[0]*(PERS[yr]+SS+MEDI) + a[1]*(SS+MEDI), 2), src=src)
print(json.dumps(out))
