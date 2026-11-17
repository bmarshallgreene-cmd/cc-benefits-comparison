# State Controller pay data test (Nov 16, 2026)

Source: publicpay.ca.gov raw export, Community College Districts, calendar year 2024 (47 of 72 districts reported; the 2025 file had 37 so far and no Yosemite). The raw files are not stored here (39 MB).

Used by the State Controller tab in index.html (SCO_DATA): 41 districts where matched rows are 75%–130% of Fall 2024 FT FTEF; Ventura dropped as implausible.

Method: rows whose Position looks like full-time faculty (instructor, faculty, professor, counselor, librarian; excluding adjunct, part-time, hourly, and similar) with TotalWages of at least $65,000. Where titles match under 80% of FT FTEF, faculty are matched by salary-schedule range (Min/Max position salary) instead. For each district: mean and median of the HealthDentalVision field (employer contribution).

`rows_per_ftef` compares the matched rows with Fall 2024 FT FTEF; values far from 1 mean the title rules did not fit that district. Ventura's values are implausibly low and should not be used.

Scripts expect the raw CSVs under /home/claude/work/sco/<year>/.

## Validation (Nov 16, 2026)
- Year to year: 34 districts in both the 2024 and 2025 files; median change in faculty median +5.6%.
- Faculty vs other full-time staff in the same district: median gap +1%; 32 of 45 within 15%. Large gaps: San Jose-Evergreen, Santa Clarita, Rio Hondo, Cerritos, Shasta-Tehama-Trinity.
- Published figures: all 41 districts searched; usable figures for 27, none contradicted. Close matches to a per-employee rate or cap (12): Barstow, Coast, Desert, El Camino, State Center, Chabot-Las Positas, Palo Verde, South Orange, Marin, West Valley-Mission, Yosemite ($2,200/month budget maximum = $26,400 vs median $25,546), Sequoias ($19,617 medical+dental contribution from Oct 2024 vs $19,847). Consistent (6): Compton, Contra Costa, Grossmont-Cuyamaca, Santa Monica, Mt. San Jacinto (low, still a question), Rancho Santiago (2025 HMO $818/$1,717/$2,453 a month; median $25,341). District-wide SCO total vs the district's budget health line (9): Allan Hancock ($4.81M vs $5.22M 2023-24 actual), Chaffey ($14.56M vs $13.77M), Kern ($28.07M vs $23.4-25.5M unrestricted), San Jose-Evergreen ($19.66M vs Fund 10 object 534 $16.35M 2023-24 / $20.43M 2024-25 budget), Palomar ($16.76M vs ~$16.36M actives 2023-24 / ~$17.57M 2024-25), Merced ($14.09M vs $15.10M 2023-24 / $16.26M budget), West Kern ($4.34M vs $3.96M 2023-24 / $4.22M 2024-25, general fund), Gavilan ($4.47M vs $3.72M unrestricted only; partial), Shasta-Tehama-Trinity ($4.85M vs medical/dental/vision/life $3.33M Fund 11 in 2023-24 and $5.99M Funds 11+12 in 2024-25; rough).
- No usable public figures (14): Cerritos, Feather River, Foothill-De Anza, Glendale, Imperial, Los Rios, MiraCosta, North Orange County, Ohlone, Redwoods (budget blocked to automated access), Santa Clarita, Sonoma (budgets show total benefits only); Los Angeles (object 340000 unrestricted $131.5M / $139.1M appears to include retirees; SCO $101.05M) and Rio Hondo (object 3400 $20.04M vs SCO $10.27M; line includes more than active-employee health). These would need a request to the district.
- YFA survey answers for Mt. San Jacinto ($21,188) and Compton ($17,000) equal a family-tier or cap figure, not an average, which explains their gap from the Controller medians.
