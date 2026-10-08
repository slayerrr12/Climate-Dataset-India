import numpy as np
import pandas as pd

from climate_pipeline.cleaning import clean_source_values


def test_clean_source_values_standardizes_headers_and_documented_sentinel():
    raw = pd.DataFrame({" PARAMETER ":["T2M"],"YEAR":["2020"],"JAN":["-999"],"FEB":["22.5"]})
    cleaned = clean_source_values(raw)
    assert list(cleaned.columns) == ["PARAMETER", "YEAR", "JAN", "FEB"]
    assert pd.isna(cleaned.loc[0, "JAN"])
    assert cleaned.loc[0, "FEB"] == 22.5
    assert cleaned.loc[0, "YEAR"] == 2020
