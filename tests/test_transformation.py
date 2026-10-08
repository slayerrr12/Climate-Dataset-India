from pathlib import Path
import pandas as pd

from climate_pipeline.ingest import parse_filename
from climate_pipeline.transform import build_city_monthly
from climate_pipeline.utils import make_location_id


def test_filename_parser_handles_base_suffix_and_space_suffix():
    assert parse_filename(Path("delhi.csv")) == ("delhi", 1)
    assert parse_filename(Path("delhi_20.csv")) == ("delhi", 20)
    assert parse_filename(Path("bengaluru 3.csv")) == ("bengaluru", 3)


def test_location_id_is_deterministic_and_unique_for_known_cities():
    assert make_location_id("delhi") == "IN-DL-DEL"
    assert make_location_id("delhi") == make_location_id("delhi")
    assert make_location_id("delhi") != make_location_id("chennai")


def test_point_aggregation_produces_one_city_month_and_spatial_means():
    date = pd.Timestamp("2020-01-01")
    points = pd.DataFrame([
        {"city_key":"bengaluru","city":"Bengaluru","measurement_point_id":1,"source_file":"bengaluru.csv",
         "date":date,"latitude":12.9,"longitude":77.5,"source":"NASA/POWER",
         "PRECTOTCORR":1.0,"T2M":19.0,"T2M_MAX":29.0,"T2M_MIN":9.0},
        {"city_key":"bengaluru","city":"Bengaluru","measurement_point_id":2,"source_file":"bengaluru_2.csv",
         "date":date,"latitude":13.0,"longitude":77.6,"source":"NASA/POWER",
         "PRECTOTCORR":3.0,"T2M":21.0,"T2M_MAX":31.0,"T2M_MIN":11.0},
    ])
    inventory = pd.DataFrame([
        {"city_key":"bengaluru","city":"Bengaluru","measurement_point_id":1,"latitude":12.9,"longitude":77.5},
        {"city_key":"bengaluru","city":"Bengaluru","measurement_point_id":2,"latitude":13.0,"longitude":77.6},
    ])
    city = build_city_monthly(points, inventory)
    assert len(city) == 1
    assert not city.duplicated(["location_id", "date"]).any()
    assert city.loc[0, "avg_temp_c"] == 20.0
    assert city.loc[0, "rainfall_mm"] == 2.0
    assert city.loc[0, "measurement_points_available"] == 2
