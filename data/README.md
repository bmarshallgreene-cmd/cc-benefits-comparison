# Source data for the CCFS-311 tab

Each year folder holds the raw inputs used to build that year's dataset in `CCFS_YEARS` in `index.html`.

## 2025-26 (pulled Nov 6, 2026)
- `ccfs311_50pct_law_colA.csv`: CCCCO Fiscal Portal, "Analysis of compliance with the 50 Percent Law (ECS 84362)", FY 2025-26, Column A (ECS 84362 A, instructional). It holds Object 3000 employee benefits and Total Instructional Salaries. 69 districts were pulled Nov 6; Compton, Desert, and San Joaquin Delta were added Nov 16 after they certified. The full report (all columns, both years) is in `analysis/`.
- `fon_fall2025.csv`: CCCCO Fall 2025 FON Compliance Report, with the obligation, FT FTEF, and PT FTEF for each district.
- `results.csv`: computed output from the Nov 6 pull, with the 2024-25 comparison alongside. It is a snapshot and predates the aide deduction, the revised counselor/librarian counts, and the Nov 16 pull of Compton, Desert, and San Joaquin Delta; `index.html` holds the current figures.

## Method (Full)
- H&W = Object 3000 − 20.55% × instructional salaries (STRS 19.1% + Medicare 1.45%) − estimated aide costs (CalPERS + Social Security + Medicare on Object 2200; Social Security + Medicare on Object 2400). See `aide_deduction.py`.
- Denominator = FT FTEF − counselor/librarian deduction. The deduction comes from Fall 2025 staffing data and the same deduction is applied in every year.

## To add a year
1. Pull the 50% Law report for every district from fiscalportal.cccco.edu. Use Column A: Object 3000 and Total Instructional Salaries.
2. Get that fall's FON compliance report for FT FTEF.
3. Run `compute.py` (it expects `site_2024.csv` with the prior-year rows as code,name,ftef,adjFtef,instrBenefits,hw).
4. Add the new dataset to `CCFS_YEARS` and `CCFS_YEAR_META` in `index.html`.

## Counselor/librarian deductions (manual districts)
Updated Nov 9, 2026 for Antelope Valley, Citrus, Gavilan, Lake Tahoe, Solano, Copper Mountain, and Palo Verde, using 2024 calendar-year payroll (State Controller data via Transparent California): employees with counselor or librarian titles and full-year faculty pay and benefits, excluding temporary/non-tenure-track, administrators, adjuncts, classified, and mental-health or outreach counselors. Redwoods uses its Fall 2024 seniority list. See the methodology list in index.html for the counts.

## Open items (as of Nov 16, 2026)
- State Controller tab added Nov 16 (calendar 2024, 41 districts). To do: title rules for Mt. San Antonio, Riverside, San Luis Obispo, San Mateo, Solano; refresh with the 2025 file once more districts (including Yosemite) have reported.
- Compton, Desert, and San Joaquin Delta: 2025-26 figures pulled Nov 16 after they certified (done).
- Merced and San Bernardino show as not certified for 2025-26 as of Nov 16 (both reopened). Site figures are from the Nov 6 / Nov 9 pulls; re-pull once certified. Merced's Allocated figure and aide deduction use 2024-25 data.
- Fall 2026 FON report not yet posted (checked Nov 16). Lassen stays excluded from 2025-26; Imperial, Rio Hondo, Santa Monica, and Copper Mountain flagged. Weekly scheduled task checks for it.
- Full and Allocated both apply the CalPERS rate to regular-status classified pay only (aide_deduction.py, analysis/build_alloc.py).
- Step 21 salaries: 2025-26 uses the CFT 2025-26 study (Oct 16, 2026); 2024-25 uses the 2024-25 study.
- Allocated is the default calculation as of Nov 16, 2026 (it agrees best with the ACCCA and YFA surveys); the Cross-Method tab uses it.
- Possible backfill of 2019-20 through 2023-24 (must keep all 50% Law columns).
- Monthly scheduled task (10th) checks for a new ACCCA survey.
