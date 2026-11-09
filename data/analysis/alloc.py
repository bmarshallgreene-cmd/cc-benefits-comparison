"""Coding-pattern check and allocated-method prototypes from 50% Law pulls.

Input: pull JSON {"17_590": {...rows keyed by label/object code...}, ...}
Positional row layout: [label, code, colA, colB, colX, total] for object rows;
total rows: [label, colA, colB, colX, total].
"""
import json, sys, csv, statistics as st

YEAR = {"17": "2025-26", "16": "2024-25"}
PERS = {"17": 0.2681, "16": 0.2705}
STRS, MEDI, SS = 0.191, 0.0145, 0.062

def n(x):
    x = (x or "").replace(",", "").replace("$", "").strip()
    if x.startswith("(") and x.endswith(")"): x = "-" + x[1:-1]
    return float(x) if x not in ("", "-") else 0.0

def obj(rows, code):
    r = rows.get(code)
    if not r: return (0.0, 0.0)
    return n(r[2]), n(r[3])  # colA, colB

def tot(rows, label, i=0):
    r = rows.get(label)
    if not r: return None
    r = r[i]
    return n(r[2]), n(r[3])

pull = json.load(open(sys.argv[1]))
site = json.load(open(sys.argv[2]))  # {year: {code: {name, ftef, adjFtef, hw, instrBenefits, excluded}}}
out = []
for key, rows in pull.items():
    yr, code = key.split("_")
    if "Employee Benefits" not in rows: continue
    ben = rows["Employee Benefits"][0]
    benA, benB = n(ben[2]), n(ben[3])
    instrA, _ = tot(rows, "Total Instructional Salaries")
    acadA, acadB = tot(rows, "Total Academic Salaries")
    aidesA, _ = tot(rows, "Total Instructional Aides")
    clasA, clasB = tot(rows, "Total Classified Salaries")
    salA = acadA + clasA
    salB = acadB + clasB
    nonA_sal = salB - salA
    r_instr = benA / salA if salA else None
    r_non = (benB - benA) / nonA_sal if nonA_sal else None
    r_all = benB / salB if salB else None
    a1100, b1100 = obj(rows, "1100")
    _, b1200 = obj(rows, "1200")
    _, b2100 = obj(rows, "2100")
    _, b2200 = obj(rows, "2200")
    regB = b1100 + b1200 + b2100 + b2200
    # pension/Medicare/SS netted pool, district-wide (col B)
    pool = benB - STRS * acadB - (PERS[yr] + SS) * clasB - MEDI * salB
    s = site.get(YEAR[yr], {}).get(str(int(code)))
    rec = dict(year=YEAR[yr], code=int(code), name=(s or {}).get("name", code),
               benA=benA, benB=benB, salA=salA, salB=salB,
               ratio_instr=r_instr, ratio_non=r_non, ratio_all=r_all,
               skew=(r_non / r_instr) if r_instr else None,
               adjFtef=(s or {}).get("adjFtef"), excluded=(s or {}).get("excluded", False),
               current=((s or {}).get("hw", 0) / s["adjFtef"]) if s and s.get("adjFtef") else None)
    if s and s.get("adjFtef"):
        adj = s["adjFtef"]
        # A: total benefits allocated by salary share, then STRS/Medicare off as now
        allocA = benB * (salA / salB) - (STRS + MEDI) * instrA
        rec["optA"] = allocA / adj
        # B: netted pool allocated by instructional salary share
        rec["optB"] = pool * (salA / salB) / adj
        # C: netted pool allocated by regular (contract) salary share; FT faculty = 1100 col A
        rec["optC"] = (pool * (a1100 / regB) / adj) if regB else None
    out.append(rec)

json.dump(out, open("alloc_results.json", "w"), indent=1)
with open("alloc_results.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out), "rows")
