# Climate data cleaning and analysis project

This repository provides a reproducible, modular workflow for the climate files in `datasets/` (or, in a clean checkout, `data/raw/`). Raw inputs are never modified.

## Resolution limitation

The delivered NASA/POWER files are monthly and annual summaries for 2000–2025, not daily observations. A truthful city-day table cannot be generated from them. The pipeline therefore writes `data/processed/daily_climate.csv` with the exact required schema and zero observation rows. It preserves the available information at city-month grain in `data/processed/city_monthly.csv` and the convenience file `climate_monthly.csv`; monthly values are not expanded into fabricated daily records.

## Repository layout

- `data/raw/`: location for original files; ignored by Git and never written by pipeline.
- `data/interim/`: cleaned point-month long/wide tables and annual summaries.
- `data/processed/`: city-month product and schema-only daily deliverable.
- `src/`: reusable ingestion, profiling, cleaning, transformation, aggregation, validation, and utility modules.
- `notebooks/`: six staged discovery, profiling, cleaning, transformation, validation, and EDA notebooks.
- `reports/`: data dictionary, inventories, quality summaries, and cleaning/data-quality reports.
- `tests/`: tests for stable IDs, filename parsing, cleaning, and output validation.

## Setup and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Execute the six notebooks in order or run the pipeline from the repository root:

```powershell
python -c "import sys; sys.path.insert(0, 'src'); from climate_pipeline import run_pipeline; run_pipeline()"
```

Run the project checks with `pytest`. See `reports/cleaning_report.md`, `reports/data_quality_report.md`, and `reports/data_dictionary.csv` for processing decisions, limitations, field meanings, and coverage.
