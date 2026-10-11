# Climate data cleaning and transformation project

This repository provides a reproducible, modular workflow for the climate files in `datasets/` (or, in a clean checkout, `data/raw/`). Raw inputs are never modified.

## Resolution limitation

The delivered NASA/POWER files are monthly and annual summaries for 2000–2025, not daily observations. A truthful city-day table cannot be generated from them. The pipeline therefore writes `data/processed/daily_climate.csv` with the exact required schema and zero observation rows. It preserves the available information at city-month grain in `data/processed/city_monthly.csv` and the convenience file `climate_monthly.csv`; monthly values are not expanded into fabricated daily records.

## Where to see the merged city data

The pipeline keeps the original point-level monthly records in `data/interim/point_monthly_wide.csv`. It then averages the available measurement-point values for each city and month, producing **one row per city per month**. Open `data/processed/by_city/ahmedabad_monthly.csv` (or another `*_monthly.csv` file in that folder) to see one city's merged time series. The all-city result is `data/processed/city_monthly.csv`; it contains those same city-month rows for every city. Thus, each point file is not one output row: each city file contains a row for every month in the source period.

## Repository layout

- `data/raw/`: location for original files; ignored by Git and never written by pipeline.
- `data/interim/`: cleaned point-month long/wide tables and annual summaries.
- `data/processed/`: combined city-month product, one monthly file per city under `by_city/`, and schema-only daily deliverable.
- `src/`: reusable ingestion, profiling, cleaning, transformation, aggregation, validation, and utility modules.
- `notebooks/`: five staged discovery, profiling, cleaning, transformation, and validation notebooks.
- `reports/`: data dictionary, inventories, quality summaries, cleaning/data-quality reports, and a presentation guide.
- `tests/`: tests for stable IDs, filename parsing, cleaning, and output validation.

## Setup and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Execute the five notebooks in order or run the pipeline from the repository root:

```powershell
python -c "import sys; sys.path.insert(0, 'src'); from climate_pipeline import run_pipeline; run_pipeline()"
```

Run the project checks with `pytest`. See `reports/cleaning_report.md`, `reports/data_quality_report.md`, and `reports/data_dictionary.csv` for processing decisions, limitations, field meanings, and coverage.
