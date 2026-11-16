"""Allocated calculation: recompute allocHw and guardrail flags in index.html.

pool  = district-wide benefits (50% Law schedule, column B, object 3000)
        - STRS 19.1% x academic salaries
        - CalPERS x regular-status classified salaries (objects 2100 + 2200)
        - Social Security 6.2% x all classified salaries
        - Medicare 1.45% x all salaries
alloc = pool x instruction's share of salaries (column A / column B)
Guardrails: exclude if district-wide benefits moved >40% year over year or equal instruction-only
benefits; flag if Full and Allocated differ by >50%.
Usage: python3 build_alloc.py <pull.json> <index.html>
"""
import json, re, sys
P = json.load(open(sys.argv[1])); path = sys.argv[2]; h = open(path).read()
KEY = {"2025-26": "17", "2024-25": "16"}; PERS = {"2025-26": 0.2681, "2024-25": 0.2705}
STRS, MEDI, SS = 0.191, 0.0145, 0.062
def n(x):
    x = (x or "").replace(",", "").strip()
    return float(x) if x not in ("", "-") else 0.0
def calc(yr, code):
    v = P.get(f"{KEY[yr]}_{int(code):03d}")
    if not v or "Employee Benefits" not in v: return None
    t = lambda lab: (n(v[lab][0][2]), n(v[lab][0][3]))
    g = lambda c: n(v[c][3]) if c in v else 0.0
    benA, benB = n(v["Employee Benefits"][0][2]), n(v["Employee Benefits"][0][3])
    acadA, acadB = t("Total Academic Salaries"); clasA, clasB = t("Total Classified Salaries")
    salA, salB = acadA + clasA, acadB + clasB
    pool = benB - STRS*acadB - PERS[yr]*(g("2100") + g("2200")) - SS*clasB - MEDI*salB
    return dict(benA=benA, benB=benB, alloc=pool*salA/salB if salB else None)
log = []
for yr in ["2024-25", "2025-26"]:
    a = h.index(f'"{yr}": ['); b = h.index("],\n", a); out = []
    for line in h[a:b].split("\n"):
        m = re.search(r'name:"([^"]+)".*?adjFtef:([0-9.]+).*?hw:([0-9.]+),.*?code:"(\d+)",', line)
        if not m: out.append(line); continue
        name, adj, full, code = m.group(1), float(m.group(2)), float(m.group(3)), m.group(4)
        line = re.sub(r' allocHw:[^,]+,', '', line); line = re.sub(r' allocFlag:"[^"]*",', '', line); line = line.replace(' allocExcluded:true,', '')
        c = calc(yr, code); flags = []; excluded = False; val = None
        if c is None and yr == "2025-26":
            c = calc("2024-25", code)
            if c: flags.append("Allocated figure carried forward from 2024-25: the district’s 2025-26 CCFS-311 report has been reopened and shows as not certified.")
            carried = True
        else: carried = False
        if c is None: flags, excluded = ["No district-wide data available."], True
        elif c["benB"] <= c["benA"]*1.001:
            flags, excluded = ["District-wide benefits are reported as equal to instruction-only benefits, which indicates a reporting error."], True
        else:
            val = round(c["alloc"], 2)
            if yr == "2025-26" and not carried:
                p = calc("2024-25", code)
                if p and p["benB"] > p["benA"]*1.001 and abs(c["benB"]/p["benB"] - 1) > 0.40:
                    flags.append(f"District-wide benefits changed {c['benB']/p['benB']-1:+.0%} from 2024-25 (${p['benB']/1e6:,.1f}M → ${c['benB']/1e6:,.1f}M), likely a one-time charge outside instruction; the Allocated figure is probably distorted.")
                    excluded = True
            if not excluded and abs(val/full - 1) > 0.50:
                flags.append(f"Full and Allocated differ by {val/full-1:+.0%}: this district appears to code benefits unevenly across activities, so its Allocated figure is likely more reliable than its Full figure.")
        extra = f' allocHw:{json.dumps(val)},'
        if flags: extra += ' allocFlag:' + json.dumps(" ".join(flags), ensure_ascii=False) + ','
        if excluded: extra += ' allocExcluded:true,'
        line = line.replace(f'code:"{code}",', f'code:"{code}",' + extra, 1)
        out.append(line); log.append((yr, name, val/adj if val else None, " ".join(flags)[:50]))
    h = h[:a] + "\n".join(out) + h[b:]
open(path, "w").write(h)
for r in log:
    if r[3] or r[1] == "Yosemite": print(r)
