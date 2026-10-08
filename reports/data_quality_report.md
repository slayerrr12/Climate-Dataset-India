# Data quality report

- Raw files: 89; cities: 8; measurement points: 89.
- Raw parameter-year rows: 34,710; cleaned point-parameter-month rows: 416,520.
- Point-month rows: 27,768; city-month rows: 2,496; daily rows: 0 (source resolution is monthly).
- Duplicate records detected: 0 exact and 0 duplicate-key rows before key-level deduplication.
- Invalid-value records removed: 0. Confirmed sentinel -999 is converted to null; extremes are preserved.
- Monthly coverage: 2000-01-01 through 2025-12-01.
- Derived fields: location_id, representative coordinates, rainfall_anomaly_mm, temperature_anomaly_c.
- Unavailable fields: daily observation grain, district, humidity_pct, aqi, pm25, ndvi.

See `raw_file_inventory.csv`, `city_measurement_point_summary.csv`, `source_parameter_summary.csv`, `city_month_coverage_summary.csv`, `city_month_missingness.csv`, and `validation_checks.csv` for detail.
