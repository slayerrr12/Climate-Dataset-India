"""Reusable raw and cleaned data profiling helpers."""
import pandas as pd


def profile_frame(frame, name="data"):
    """Return a compact structural, missingness, and numeric profile."""
    summary = {"dataset":name,"rows":len(frame),"columns":len(frame.columns),
               "exact_duplicate_rows":int(frame.duplicated().sum())}
    fields = pd.DataFrame({"column":frame.columns,"dtype":[str(frame[c].dtype) for c in frame],
                           "missing_count":[int(frame[c].isna().sum()) for c in frame],
                           "missing_pct":[round(float(frame[c].isna().mean()*100),2) for c in frame],
                           "unique_values":[int(frame[c].nunique(dropna=True)) for c in frame]})
    return summary, fields


def profile_files(inventory):
    """Summarize discovered file counts, schemas, row counts and date spans."""
    return inventory.groupby("city",as_index=False).agg(
        files=("source_file","nunique"),measurement_points=("measurement_point_id","nunique"),
        rows=("number_of_rows","sum"),minimum_date=("date_min","min"),maximum_date=("date_max","max"),
        unique_schemas=("schema_signature","nunique"))
