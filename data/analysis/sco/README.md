# State Controller pay data test (Nov 16, 2026)

Source: publicpay.ca.gov raw export, Community College Districts, calendar year 2024 (47 of 72 districts reported; the 2025 file had 37 so far and no Yosemite). The raw files are not stored here (39 MB).

Used by the State Controller tab in index.html (SCO_DATA): 41 districts where matched rows are 75%–130% of Fall 2024 FT FTEF; Ventura dropped as implausible.

Method: rows whose Position looks like full-time faculty (instructor, faculty, professor, counselor, librarian; excluding adjunct, part-time, hourly, and similar) with TotalWages of at least $65,000. Where titles match under 80% of FT FTEF, faculty are matched by salary-schedule range (Min/Max position salary) instead. For each district: mean and median of the HealthDentalVision field (employer contribution).

`rows_per_ftef` compares the matched rows with Fall 2024 FT FTEF; values far from 1 mean the title rules did not fit that district. Ventura's values are implausibly low and should not be used.

Scripts expect the raw CSVs under /home/claude/work/sco/<year>/.

## Validation (Nov 16, 2026)
- Year to year: 34 districts in both the 2024 and 2025 files; median change in faculty median +5.6%.
- Faculty vs other full-time staff in the same district: median gap +1%; 32 of 45 within 15%. Large gaps: San Jose-Evergreen, Santa Clarita, Rio Hondo, Cerritos, Shasta-Tehama-Trinity.
- Published figures (18 districts, none contradicted). Close matches to a per-employee rate or cap: Barstow, Coast, Desert, El Camino, State Center, Chabot-Las Positas, Palo Verde, South Orange, Marin, West Valley-Mission. Consistent: Compton, Contra Costa, Grossmont-Cuyamaca, Santa Monica, Mt. San Jacinto (low, still a question). District-wide SCO total agrees with the district's budget object 3400: Allan Hancock ($4.81M vs $5.22M 2023-24 actual), Chaffey ($14.56M vs $13.77M), Kern ($28.07M vs $23.4-25.5M unrestricted). Searched, no usable figures: San Jose-Evergreen, Foothill-De Anza, Gavilan, Glendale, Imperial (district pays employee-only at Basic plan level; no dollar amount), Los Angeles, Los Rios, Merced, North Orange County, Palomar, Rancho Santiago, Redwoods, Rio Hondo, Santa Clarita, Sequoias, Sonoma, West Kern. Shasta-Tehama-Trinity posts a 2024-25 faculty rate sheet that could not be opened from this session. Not yet searched: Cerritos (one attempt), Feather River, Ohlone, Yosemite (own contract). The budget-total check (district object 3400 vs summed SCO contributions) can be extended to any district with a posted budget book.
- YFA survey answers for Mt. San Jacinto ($21,188) and Compton ($17,000) equal a family-tier or cap figure, not an average, which explains their gap from the Controller medians.
