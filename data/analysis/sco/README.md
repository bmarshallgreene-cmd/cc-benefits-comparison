# State Controller pay data test (Nov 16, 2026)

Source: publicpay.ca.gov raw export, Community College Districts, calendar year 2024 (47 of 72 districts reported; the 2025 file had 37 so far and no Yosemite). The raw files are not stored here (39 MB).

Used by the State Controller tab in index.html (SCO_DATA): 41 districts where matched rows are 75%–130% of Fall 2024 FT FTEF; Ventura dropped as implausible.

Method: rows whose Position looks like full-time faculty (instructor, faculty, professor, counselor, librarian; excluding adjunct, part-time, hourly, and similar) with TotalWages of at least $65,000. Where titles match under 80% of FT FTEF, faculty are matched by salary-schedule range (Min/Max position salary) instead. For each district: mean and median of the HealthDentalVision field (employer contribution).

`rows_per_ftef` compares the matched rows with Fall 2024 FT FTEF; values far from 1 mean the title rules did not fit that district. Ventura's values are implausibly low and should not be used.

Scripts expect the raw CSVs under /home/claude/work/sco/<year>/.
