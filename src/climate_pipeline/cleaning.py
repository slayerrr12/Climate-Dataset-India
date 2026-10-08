"""Small, explicit source-cleaning operations used during ingestion."""
import numpy as np
import pandas as pd


def standardize_source_columns(columns):
    """Trim and uppercase source identifiers while preserving their meaning."""
    return [str(c).strip().upper() for c in columns]


def clean_source_values(frame):
    """Convert documented source sentinels and numeric text without imputation."""
    out = frame.copy()
    out.columns = standardize_source_columns(out.columns)
    if "PARAMETER" in out:
        out["PARAMETER"] = out["PARAMETER"].astype("string").str.strip()
    if "YEAR" in out:
        out["YEAR"] = pd.to_numeric(out["YEAR"], errors="coerce").astype("Int64")
    value_columns = [c for c in out if c in {"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","ANN"}]
    for column in value_columns:
        out[column] = pd.to_numeric(out[column], errors="coerce").replace(-999, np.nan)
    return out
