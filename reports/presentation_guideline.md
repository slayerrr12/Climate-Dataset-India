# Climate Dataset India — 10-slide presentation

**Audience:** general audience or introductory data-science class
**Style:** use the slide text as written, explain one idea at a time, and use the speaker notes as a short script. The suggested visuals are simple process diagrams or tables.

## Slide 1 — Climate Dataset India

### Put on the slide

**How we organized and prepared climate data for Indian cities**

- Data source: NASA/POWER files
- Work covered: discovery, profiling, cleaning, transformation, aggregation, and validation
- Project result: a documented, reusable city-level dataset

### Say

“This presentation explains how we took many source files and organized the information into a consistent dataset, while keeping the source meaning intact.”

### Simple visual

One arrow: `Source files → Clean data → City-month dataset`

## Slide 2 — The question we started with

### Put on the slide

- The source was split across many files.
- Each city had multiple measurement points.
- We needed consistent city names, dates, locations, and climate fields.
- We needed to know what the files could reliably support.

### Say

“Our first task was to understand how the files fit together. We then built a repeatable process to clean and combine them.”

### Simple visual

Show several file icons grouped into one city folder.

## Slide 3 — What was in the source collection?

### Put on the slide

- 89 CSV files
- 8 cities
- 89 measurement-point files
- Source years: 2000–2025
- 15 NASA/POWER climate parameters

| City | Points |
|---|---:|
| Ahmedabad | 9 |
| Bengaluru | 10 |
| Bhopal | 10 |
| Bhubaneswar | 10 |
| Chandigarh | 10 |
| Chennai | 10 |
| Coimbatore | 10 |
| Delhi | 20 |

### Say

“A file represents a measurement point, not a separate city. The number of points differs by city, so the process detects the counts from the actual filenames.”

### Simple visual

Use the table above; highlight that Delhi has 20 points and Ahmedabad has 9.

## Slide 4 — Data profiling: understand the files first

### Put on the slide

- Files share a NASA/POWER header and parameter table.
- Rows identify a climate parameter and a year.
- `JAN` through `DEC` contain monthly summaries.
- `ANN` contains a separate annual summary.
- Headers provide measurement-point latitude and longitude.
- `-999` is the documented missing-value code.

### Say

“Profiling means examining the structure and values before changing anything. It showed that these files contain monthly and annual summaries.”

### Simple visual

Show a small mock row: `T2M | 2020 | JAN | FEB | … | DEC | ANN` and label it “monthly and annual summary.”

## Slide 5 — Data cleaning: make records consistent

### Put on the slide

- Standardized parameter labels and numeric fields.
- Converted year and month labels into usable dates.
- Changed documented `-999` values into missing values.
- Corrected known filename spellings: `ahemdabad` → Ahmedabad and `bhubhaneswar` → Bhubaneswar.
- Checked for duplicate point-period-parameter records; none were found.
- Did not fill missing climate values or remove extremes.

### Say

“We changed only what the source definitions supported. Missing values stayed missing, and unusual climate values were kept because they may be real.”

### Simple visual

Show a before-and-after pair: `-999 → blank / missing`.

## Slide 6 — Data transformation: prepare useful tables

### Put on the slide

- **Long table:** one row for one point, month, and parameter.
- **Wide table:** one row for one point and month, with parameters in columns.
- **Annual table:** annual summaries kept separate from monthly records.
- Each record keeps city, point number, date, source filename, coordinates, and source.

### Say

“We kept intermediate tables so every step can be inspected. Annual values are stored separately so they cannot be accidentally mixed with monthly values.”

### Simple visual

Show three labeled boxes: `Point-month long` → `Point-month wide` → `City-month` and a separate `Annual summaries` box.

## Slide 7 — Combining measurement points into city records

### Put on the slide

- Match records by city and month.
- Average comparable NASA/POWER point values for the city-month summary.
- Keep the number of contributing points and expected points.
- Calculate representative coordinates as the mean of point coordinates.
- Result: **2,496 city-month rows for 8 cities**.

### Say

“We combined comparable measurements for the same city and month. Coverage counts show how many measurement points contributed to each result.”

### Simple visual

Show three point values flowing into one city-month summary, with “points contributing” shown below.

## Slide 8 — Standard fields and derived information

### Put on the slide

- City and state names are standardized; location IDs are stable.
- `T2M` maps to average temperature.
- `T2M_MAX` and `T2M_MIN` map to monthly summaries of daily maximum and minimum temperature.
- `PRECTOTCORR` is a monthly mean daily precipitation rate, in **mm/day**.
- Monthly anomalies use each city’s calendar-month average over 2000–2025, when at least 10 years are available.
- District, relative humidity, AQI, PM2.5, and NDVI are unavailable.

### Say

“We kept source units and meanings clear. In particular, the precipitation field is a monthly average rate, not a daily reading or a monthly total.”

### Simple visual

Use a two-column table: “Available or derived” and “Unavailable from these files.”

## Slide 9 — Data validation: check the result

### Put on the slide

- One row per location and month.
- City and state fields are populated.
- Coordinates fall within valid latitude and longitude ranges.
- Dates are valid month keys.
- Precipitation is not negative.
- Minimum, average, and maximum temperature summaries are in order.
- All 8 city-month validation checks passed.

### Say

“Validation checks that the finished table has the expected structure and that its values follow the rules we defined.”

### Simple visual

Show a short checklist with all items marked complete.

## Slide 10 — What we delivered and what is needed next

### Put on the slide

- Reusable Python modules and five step-by-step notebooks.
- Cleaned point-level intermediate tables and annual summaries.
- A populated city-month dataset and field dictionary.
- Quality, cleaning, coverage, and validation reports.
- The required daily file has the correct columns but **zero rows**.
- Daily-resolution source files are needed to create real city-day records.

### Say

“The source data is monthly, so it cannot provide genuine daily observations. We delivered the data at the finest reliable time level available and left the daily file empty rather than inventing values.”

### Simple visual

Show the result as `2,496 city-month rows` and a separate note: `Daily data needed for a populated daily file`.

## Closing sentence

“The key result is a reproducible and traceable city-month dataset that preserves the information the source actually contains.”
