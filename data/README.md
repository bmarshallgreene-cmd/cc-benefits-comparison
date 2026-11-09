# Source data for the CCFS-311 tab

Each year folder holds the raw inputs used to build that year's dataset in `CCFS_YEARS` in `index.html`.

## 2025-26 (pulled Nov 6, 2026)
- `ccfs311_50pct_law_colA.csv`: CCCCO Fiscal Portal, "Analysis of compliance with the 50 Percent Law (ECS 84362)", FY 2025-26, Column A (ECS 84362 A, instructional). It holds Object 3000 employee benefits and Total Instructional Salaries for the 69 certified districts. Compton, Desert, and San Joaquin Delta had not certified yet, so their 2024-25 figures are carried forward.
- `fon_fall2025.csv`: CCCCO Fall 2025 FON Compliance Report, with the obligation, FT FTEF, and PT FTEF for each district.
- `results.csv`: computed output, with the 2024-25 comparison alongside.

## Method (Full)
- H&W = Object 3000 − 20.55% × instructional salaries (STRS 19.1% + Medicare 1.45%).
- Denominator = FT FTEF − counselor/librarian deduction. The deduction comes from Fall 2025 staffing data and the same deduction is applied in every year.

## To add a year
1. Pull the 50% Law report for every district from fiscalportal.cccco.edu. Use Column A: Object 3000 and Total Instructional Salaries.
2. Get that fall's FON compliance report for FT FTEF.
3. Run `compute.py` (it expects `site_2024.csv` with the prior-year rows as code,name,ftef,adjFtef,instrBenefits,hw).
4. Add the new dataset to `CCFS_YEARS` and `CCFS_YEAR_META` in `index.html`.

## Counselor/librarian deductions (manual districts)
Updated Nov 9, 2026 for Antelope Valley, Citrus, Gavilan, Lake Tahoe, Solano, Copper Mountain, and Palo Verde, using 2024 calendar-year payroll (State Controller data via Transparent California): employees with counselor or librarian titles and full-year faculty pay and benefits, excluding temporary/non-tenure-track, administrators, adjuncts, classified, and mental-health or outreach counselors. Redwoods uses its Fall 2024 seniority list. See the methodology list in index.html for the counts.

## Open items (as of Nov 9, 2026)
- When Compton, Desert, and San Joaquin Delta certify their 2025-26 reports, re-pull those three and replace their carried-forward rows.
- Lassen is excluded from 2025-26 (district says the reported 18.6 FT FTEF is an error). Imperial, Rio Hondo, and Copper Mountain are flagged for unverified FTEF swings. A weekly scheduled task checks for the Fall 2026 FON report.
- Possible backfill of 2019-20 through 2023-24. Basic is exact for those years; Full would reuse the Fall 2025 counselor/librarian deductions.
