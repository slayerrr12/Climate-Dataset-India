# 10-slide presentation guide: Climate Dataset India

**Audience:** general or introductory data-science audience  
**Style:** one main idea per slide, short bullets, plain language; use the speaker prompts as simple explanations.  
**Scope:** describe the work performed on the data. This presentation does not include exploratory data analysis.

## Slide 1 — Project goal

**On the slide**

- Organize climate files from multiple locations in India.
- Clean and combine measurement-point data by city.
- Preserve what the source actually provides.

**Say:** “We wanted one reliable, understandable dataset for each city, while keeping the original information honest.”

## Slide 2 — What data did we receive?

**On the slide**

- NASA/POWER source files.
- 89 CSV files covering 8 cities.
- Each file represents a measurement point.
- Data spans 2000–2025.

**Say:** “The filename tells us which city and measurement point a file belongs to.”

## Slide 3 — Data discovery: grouping the files

**On the slide**

- City names and point numbers were detected from filenames automatically.
- Example: `delhi.csv`, `delhi_2.csv`, …, `delhi_20.csv` are all Delhi.
- Point counts vary: Ahmedabad 9, most cities 10, Delhi 20.

**Say:** “We grouped files by city instead of treating every file as a separate city.”

## Slide 4 — Data profiling: understand before changing

**On the slide**

- Files contain 15 climate parameters.
- Each parameter has monthly values and an annual summary.
- The shared source layout stores one row per parameter and year.
- Missing values use the documented code `-999`.

**Say:** “Profiling showed us the file structure, date coverage, variables, and missing-value code before cleaning.”

## Slide 5 — Data cleaning: keep changes evidence-based

**On the slide**

- Standardized parameter names and numeric/date types.
- Converted documented `-999` values to missing values.
- Standardized known city spelling variants.
- Checked duplicates; none were found in this collection.
- Kept unusual values; did not fill missing climate measurements.

**Say:** “We corrected only what the source made clear. We did not guess missing weather values or delete extremes just because they looked unusual.”

## Slide 6 — Data transformation: make the records usable

**On the slide**

- Reshaped source data into a long point-month table.
- Created a wide point-month table with one column per parameter.
- Kept annual summaries separate from monthly values.
- Preserved city, point, date, coordinates, and source filename.

**Say:** “These intermediate tables make it possible to check each step and trace a value back to its source file.”

## Slide 7 — Combining measurement points

**On the slide**

- Aligned all measurement points by city and month.
- Averaged comparable NASA/POWER values across available points.
- Recorded available and expected point counts.
- Calculated representative coordinates from point coordinates.

**Say:** “The final populated dataset has one row per city per month, with coverage counts showing how many points contributed.”

## Slide 8 — Standardized fields and derived values

**On the slide**

- Added consistent city and state names and stable location IDs.
- Mapped `T2M`, `T2M_MAX`, and `T2M_MIN` to temperature fields.
- Used `PRECTOTCORR` for the available precipitation measure.
- Calculated monthly anomalies against each city’s calendar-month average when at least 10 years were available.

**Say:** “The precipitation field is a monthly mean daily rate in mm/day, not a daily observation or a monthly total. We documented that distinction.”

## Slide 9 — Data validation

**On the slide**

- Checked city-month key uniqueness.
- Checked city/state fields and coordinate ranges.
- Checked dates, negative precipitation, and temperature ordering.
- All 8 validation checks passed.

**Say:** “Validation confirms that the populated city-month table is structurally consistent and passes the checks we defined.”

## Slide 10 — Deliverables and key limitation

**On the slide**

- 2,496 city-month records for 8 cities.
- Cleaned long, wide, and annual intermediate datasets are retained.
- Reports include the data dictionary, coverage, missingness, and cleaning decisions.
- The required daily CSV has the correct schema but zero rows.
- Daily-resolution source files are needed to create real city-day records.

**Say:** “The source is monthly, so we did not invent daily values. The monthly dataset is complete at the resolution the files support; daily data requires a daily source.”

## Optional closing line

“The main result is a reproducible, traceable city-month dataset, with a clear explanation of what the current source can—and cannot—support.”
