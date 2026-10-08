# Cleaning and transformation report

## Raw data

- Files discovered: 89 across 8 cities and 89 measurement-point files.
- Source raw rows (parameter by year): 34,710; monthly coverage: 2000-01-01 to 2025-12-01.
- NASA/POWER files share the parameter/year/month schema plus annual `ANN` values.

## Cleaning decisions

- Filename city and point identifiers are parsed dynamically. Source spellings `ahemdabad` → `Ahmedabad` and `bhubhaneswar` → `Bhubaneswar` are normalized.
- Parameter labels are trimmed and uppercased; month and year values are converted to numeric and datetime types.
- The documented missing sentinel `-999` becomes null. No imputation or statistical outlier deletion is performed.
- Duplicate records are counted and deduplicated at city + point + period + parameter keys. Conflicting values are not silently selected.
- Source units are preserved; no speculative conversions are performed. `PRECTOTCORR` is a monthly mean daily precipitation rate (mm/day), not a daily observation or monthly accumulation.

## Transformation and aggregation

- Point-month parameters are retained in long and wide forms; annual summaries are stored separately.
- Comparable monthly gridded values are averaged across available points. Representative coordinates are arithmetic means of point coordinates.
- `city` is the standardized city label, `state` is mapped from recognized city metadata, and `district` is null because the source does not contain district data.
- Temperature anomalies compare `T2M` with the city's calendar-month mean for 2000–2025. Precipitation anomalies use the same city/calendar-month baseline and retain mm/day rate units. At least 10 valid years are required.

## Validation and limitations

- Key uniqueness, populated city/state, coordinate bounds, datetime type, and non-negative precipitation are checked.
- Detailed missingness and measurement-point coverage are saved in adjacent reports.
- Input files contain monthly and annual summaries, not daily records. Therefore `data/processed/daily_climate.csv` has the exact requested schema but zero observations. Monthly summaries are not expanded into fabricated daily values.
- The populated city-month result is `data/processed/city_monthly.csv`; humidity, AQI, PM2.5, NDVI, and district remain unavailable.
