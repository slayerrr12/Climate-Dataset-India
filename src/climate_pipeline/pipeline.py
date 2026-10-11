"""End-to-end orchestration and output generation."""
import json
from pathlib import Path
import pandas as pd

from .config import RAW_DIR, PROJECT_DIR, FINAL_DAILY_COLUMNS
from .ingest import discover_files, read_all_points
from .transform import point_monthly_wide, build_city_monthly, build_data_dictionary
from .validation import validate_city_monthly, validate_daily_schema


def run_pipeline(raw_dir=RAW_DIR, output_root=None):
    """Discover, profile, clean, transform, validate, report, and export source data."""
    root = Path(output_root or PROJECT_DIR)
    interim, processed = root / "data/interim", root / "data/processed"
    reports = root / "reports"
    for folder in (interim, processed, reports):
        folder.mkdir(parents=True, exist_ok=True)

    inventory = discover_files(raw_dir)
    point_long, annual = read_all_points(inventory, raw_dir)
    duplicate_key = ["city_key", "measurement_point_id", "date", "PARAMETER"]
    exact_duplicates = int(point_long.duplicated().sum())
    duplicate_key_rows = int(point_long.duplicated(duplicate_key, keep=False).sum())
    point_long = point_long.drop_duplicates(duplicate_key)
    annual = annual.drop_duplicates(duplicate_key)
    point_wide = point_monthly_wide(point_long)
    city = build_city_monthly(point_wide, inventory)
    dictionary = build_data_dictionary(point_long, city)
    validation = validate_city_monthly(city)
    if not validation.passed.all():
        failed = validation.loc[~validation.passed, "check"].tolist()
        raise ValueError(f"City-month validation failed: {failed}")

    point_summary = inventory.groupby(["city_key", "city"], as_index=False).agg(
        number_of_points=("measurement_point_id", "nunique"),
        number_of_files=("source_file", "nunique"),
        latitude_min=("latitude", "min"), latitude_max=("latitude", "max"),
        longitude_min=("longitude", "min"), longitude_max=("longitude", "max"))
    parameter_summary = point_long.groupby(["PARAMETER", "summary_period"], as_index=False).agg(
        rows=("value", "size"), missing_values=("value", lambda s: int(s.isna().sum())),
        valid_values=("value", "count"), minimum=("value", "min"), maximum=("value", "max"))
    coverage = city.groupby(["city_key", "city"], as_index=False).agg(
        city_month_rows=("date", "count"), first_month=("date", "min"), last_month=("date", "max"),
        mean_available_points=("measurement_points_available", "mean"),
        expected_points=("expected_points", "max"))
    missingness = pd.DataFrame({
        "column": city.columns,
        "missing_count": [int(city[c].isna().sum()) for c in city.columns],
        "missing_pct": [round(float(city[c].isna().mean() * 100), 2) for c in city.columns]})
    summary = {
        "raw_files": int(len(inventory)), "cities": int(inventory.city.nunique()),
        "measurement_points": int(inventory.measurement_point_id.count()),
        "raw_rows": int(inventory.number_of_rows.sum()),
        "cleaned_point_parameter_month_rows": int(len(point_long)),
        "annual_summary_rows": int(len(annual)), "point_month_rows": int(len(point_wide)),
        "city_month_rows": int(len(city)), "exact_duplicate_rows_detected": exact_duplicates,
        "duplicate_key_rows_detected": duplicate_key_rows, "invalid_value_records_removed": 0,
        "date_start": str(city.date.min().date()), "date_end": str(city.date.max().date()),
        "derived_fields": ["location_id", "representative coordinates", "rainfall_anomaly_mm", "temperature_anomaly_c"],
        "unavailable_fields": ["daily observation grain", "district", "humidity_pct", "aqi", "pm25", "ndvi"]}

    inventory.to_csv(reports / "raw_file_inventory.csv", index=False, date_format="%Y-%m-%d")
    point_summary.to_csv(reports / "city_measurement_point_summary.csv", index=False)
    parameter_summary.to_csv(reports / "source_parameter_summary.csv", index=False)
    dictionary.to_csv(reports / "data_dictionary.csv", index=False)
    coverage.to_csv(reports / "city_month_coverage_summary.csv", index=False, date_format="%Y-%m-%d")
    validation.to_csv(reports / "validation_checks.csv", index=False)
    missingness.to_csv(reports / "city_month_missingness.csv", index=False)
    (reports / "pipeline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    point_long.to_csv(interim / "point_monthly_long.csv", index=False, date_format="%Y-%m-%d")
    annual.to_csv(interim / "point_annual_summary_long.csv", index=False, date_format="%Y-%m-%d")
    point_wide.to_csv(interim / "point_monthly_wide.csv", index=False, date_format="%Y-%m-%d")
    city.to_csv(processed / "city_monthly.csv", index=False, date_format="%Y-%m-%d")
    city.to_csv(root / "climate_monthly.csv", index=False, date_format="%Y-%m-%d")

    daily = pd.DataFrame({c: pd.Series(dtype=("datetime64[ns]" if c == "date" else
        "object" if c in {"location_id", "district", "state", "source", "data_quality_flag"} else "float64"))
        for c in FINAL_DAILY_COLUMNS})
    daily_validation = validate_daily_schema(daily)
    if not daily_validation.passed.all():
        raise ValueError("The schema-only daily dataset failed structural validation")
    daily.to_csv(processed / "daily_climate.csv", index=False)
    daily.to_csv(root / "daily_climate.csv", index=False)

    cleaning_report = f"""# Cleaning and transformation report

## Raw data

- Files discovered: {summary['raw_files']} across {summary['cities']} cities and {summary['measurement_points']} measurement-point files.
- Source raw rows (parameter by year): {summary['raw_rows']:,}; monthly coverage: {summary['date_start']} to {summary['date_end']}.
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
"""
    (reports / "cleaning_report.md").write_text(cleaning_report, encoding="utf-8")
    quality_report = f"""# Data quality report

- Raw files: {summary['raw_files']}; cities: {summary['cities']}; measurement points: {summary['measurement_points']}.
- Raw parameter-year rows: {summary['raw_rows']:,}; cleaned point-parameter-month rows: {summary['cleaned_point_parameter_month_rows']:,}.
- Point-month rows: {summary['point_month_rows']:,}; city-month rows: {summary['city_month_rows']:,}; daily rows: {len(daily)} (source resolution is monthly).
- Duplicate records detected: {summary['exact_duplicate_rows_detected']} exact and {summary['duplicate_key_rows_detected']} duplicate-key rows before key-level deduplication.
- Invalid-value records removed: 0. Confirmed sentinel -999 is converted to null; extremes are preserved.
- Monthly coverage: {summary['date_start']} through {summary['date_end']}.
- Derived fields: {', '.join(summary['derived_fields'])}.
- Unavailable fields: {', '.join(summary['unavailable_fields'])}.

See `raw_file_inventory.csv`, `city_measurement_point_summary.csv`, `source_parameter_summary.csv`, `city_month_coverage_summary.csv`, `city_month_missingness.csv`, and `validation_checks.csv` for detail.
"""
    (reports / "data_quality_report.md").write_text(quality_report, encoding="utf-8")
    return {"inventory": inventory, "point_long": point_long, "annual": annual,
        "point_wide": point_wide, "city_monthly": city, "daily_climate": daily,
        "dictionary": dictionary, "point_summary": point_summary,
        "parameter_summary": parameter_summary, "quality_summary": coverage,
        "validation": validation, "missingness": missingness, "summary": summary}
