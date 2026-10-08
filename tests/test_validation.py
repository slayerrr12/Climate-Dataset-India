import pandas as pd

from climate_pipeline.config import FINAL_DAILY_COLUMNS
from climate_pipeline.validation import validate_daily_schema


def empty_daily_frame():
    return pd.DataFrame({c:pd.Series(dtype=("datetime64[ns]" if c=="date" else
        "object" if c in {"location_id","district","state","source","data_quality_flag"} else "float64"))
        for c in FINAL_DAILY_COLUMNS})


def test_daily_schema_accepts_exact_required_empty_schema():
    result = validate_daily_schema(empty_daily_frame())
    assert result.passed.all()


def test_daily_schema_rejects_wrong_column_order():
    frame = empty_daily_frame()[list(reversed(FINAL_DAILY_COLUMNS))]
    result = validate_daily_schema(frame)
    assert not result.loc[result.check.eq("required columns and order"),"passed"].iloc[0]


def test_daily_validation_catches_invalid_coordinates_humidity_and_temperature_order():
    row = {c:None for c in FINAL_DAILY_COLUMNS}
    row.update({"location_id":"IN-KA-BLR","date":pd.Timestamp("2020-01-01"),
        "latitude":95.0,"longitude":77.5,"rainfall_mm":1.0,"humidity_pct":105.0,
        "min_temp_c":25.0,"avg_temp_c":20.0,"max_temp_c":30.0})
    result = validate_daily_schema(pd.DataFrame([row]))
    failures = set(result.loc[~result.passed,"check"])
    assert {"coordinates in range","humidity within bounds","temperature ordering"} <= failures
