# Transparent California estimates (Nov 17, 2026)

Fills in the State Controller tab for districts missing from the State Controller's 2024 file (25 did not report; San Mateo and Ventura reported unusable figures).

- Source: transparentcalifornia.com 2024 salary pages, scraped in-browser Nov 17, 2026. `raw/<district>.json` keeps, for every record with total pay of at least $60,000: job title, base pay, other pay, total benefits, total pay (no names).
- Transparent California's "Total Benefits" = employer pension + health (equals the State Controller's DefinedBenefitPlanContribution + HealthDentalVision for Yosemite, which is in both).
- Estimate per faculty member: total benefits - 0.191 x total pay. On the 44 State Controller districts where the truth is known this gives a median error of 2.5% (33 of 44 within 5%); fitting a district-specific slope is much worse (12.6%) because higher-paid faculty more often carry family coverage.
- Faculty: titles in `est.py` (instructor, faculty, professor, counselor, librarian, "Contract", department head/chair, "Instr"), excluding part-time, adjunct, administrators, etc.; total pay >= $65,000. Santa Barbara also drops the bare "Instructor"/"Counselor" titles, which are part-time there.
- Covered = estimate >= $3,000. Figures are mean, median and 90th percentile among covered faculty, as for the State Controller districts.
- `build_tc.py` prints the rows added to SCO_DATA (method "tc"). Excluded: Peralta (benefits ~$4,500, no pension), Butte (benefits ~50% of pay), Yuba (pension missing for half). Lower confidence (flagged on the site): San Francisco, Lake Tahoe, Siskiyou, Copper Mountain, San Mateo.
- Cross-checks: Antelope Valley $17,500 = ACCCA $17,500; Napa Valley $14,070 vs YFA $14,026; Santa Barbara tiers $10.6k/$20.5k/$28.5k vs its 2025 State Controller tiers $11,227/$21,565/$30,074; San Diego median $25,442 vs ACCCA $24,961; Lassen $20,929 vs ACCCA $22,641 / YFA $23,496.

## Nov 17 follow-up: district HR sites and contracts
- Corroborated: San Francisco (2024 SFHSS rates for City College faculty: Kaiser $10,028 / $17,148 / $19,693 a year), Siskiyou (contract caps before 2025-26: $9,391 / $15,200 / $22,220 including dental and vision), Copper Mountain (contract: full premium up to $820 / $1,320 / $1,770 a month; HMO members pay at most $75 / $150 / $200 above), San Mateo (published 2024 medical contributions $12,257 / $21,572 / $28,044; the ~$1,500 group matches dental and vision only).
- Lake Tahoe: Transparent California estimate dropped; faculty cap $18,456 through 2023-24 (FA CBA 2022-25), $21,030 for other groups in 2024-25; site uses ~$19,743 for calendar 2024.
- Rate-sheet estimates added for Peralta (Kaiser fully paid, 2024-25 benefit guide; average = 71% of family level, the median ratio among 46 tiered districts), Butte (flat contribution, BCEA 2024-27 Art. 12.5 COLA formula backed out from $1,881.81/month in 2026-27), Yuba (2024-25 certificated plan rates; Premier plan shown).
