import pandas as pd
from .config import FINAL_DAILY_COLUMNS

def validate_city_monthly(data):
    checks = {
        "city field populated": bool(data.city.notna().all() and data.city.str.strip().ne("").all()),
        "state field populated": bool(data.state.notna().all() and data.state.str.strip().ne("").all()),
        "one row per location-month": not bool(data.duplicated(["location_id", "date"]).any()),
        "valid latitude": bool(data.latitude.dropna().between(-90,90).all()),
        "valid longitude": bool(data.longitude.dropna().between(-180,180).all()),
        "date is datetime": pd.api.types.is_datetime64_any_dtype(data.date),
        "no negative precipitation": not bool((data.rainfall_mm.dropna()<0).any()),
        "temperature ordering": not bool((data[["min_temp_c","avg_temp_c","max_temp_c"]].notna().all(axis=1) &
            ~((data.min_temp_c <= data.avg_temp_c) & (data.avg_temp_c <= data.max_temp_c))).any()),
    }
    return pd.DataFrame([{"check":k,"passed":v} for k,v in checks.items()])


def validate_daily_schema(data):
    checks = {
        "required columns and order": list(data.columns) == FINAL_DAILY_COLUMNS,
        # An empty CSV has no values from which pandas can infer datetime;
        # accept its object dtype only for a zero-row schema-only export.
        "date dtype is datetime compatible": (pd.api.types.is_datetime64_any_dtype(data["date"])
                                               or (data.empty and data["date"].dtype == object)),
        "daily key unique": not bool(data.duplicated(["location_id", "date"]).any()),
        "coordinates in range": bool(data.latitude.dropna().between(-90,90).all() and
                                      data.longitude.dropna().between(-180,180).all()),
        "rainfall non-negative": not bool((data.rainfall_mm.dropna() < 0).any()),
        "humidity within bounds": bool(data.humidity_pct.dropna().between(0,100).all()),
        "temperature ordering": not bool((data[["min_temp_c","avg_temp_c","max_temp_c"]].notna().all(axis=1) &
            ~((data.min_temp_c <= data.avg_temp_c) & (data.avg_temp_c <= data.max_temp_c))).any()),
    }
    return pd.DataFrame([{"check":k,"passed":v} for k,v in checks.items()])
