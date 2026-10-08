import re
import numpy as np
import pandas as pd
from .config import CITY_METADATA
from .utils import make_location_id

PARAMETER_TARGETS = {"PRECTOTCORR":"rainfall_mm","T2M":"avg_temp_c","T2M_MAX":"max_temp_c","T2M_MIN":"min_temp_c"}

def point_monthly_wide(point_long):
    data = point_long[point_long.summary_period.eq("monthly")].copy()
    key = ["city_key","city","measurement_point_id","source_file","date","latitude","longitude","source"]
    wide = data.pivot_table(index=key, columns="PARAMETER", values="value", aggfunc="first").reset_index()
    wide.columns.name = None
    return wide

def build_city_monthly(point_wide, inventory):
    parameter_cols = [c for c in point_wide.columns if c not in {"city_key","city","measurement_point_id","source_file","date","latitude","longitude","source"}]
    aggregation = {c:"mean" for c in parameter_cols}
    city = point_wide.groupby(["city_key","city","date"], as_index=False).agg(aggregation)
    counts = point_wide.groupby(["city_key","date"]).measurement_point_id.nunique().rename("measurement_points_available").reset_index()
    counts = counts.merge(inventory.groupby("city_key").measurement_point_id.nunique().rename("expected_points"), on="city_key", how="left")
    coordinates = inventory.groupby(["city_key","city"], as_index=False).agg(latitude=("latitude","mean"), longitude=("longitude","mean"))
    city = city.merge(counts,on=["city_key","date"],how="left").merge(coordinates,on=["city_key","city"],how="left")
    city["state"] = city.city_key.map(lambda k:CITY_METADATA.get(k,{}).get("state"))
    city["state_code"] = city.city_key.map(lambda k:CITY_METADATA.get(k,{}).get("state_code","UNK"))
    city["city_code"] = city.city_key.map(lambda k:CITY_METADATA.get(k,{}).get("city_code",re.sub("[^A-Z]","",k.upper())[:3]))
    city["location_id"] = city.city_key.map(make_location_id)
    city["district"] = pd.NA
    for parameter, target in PARAMETER_TARGETS.items():
        city[target] = city[parameter] if parameter in city else np.nan
    for target in ["humidity_pct","aqi","pm25","ndvi"]: city[target] = np.nan
    city["source"] = "NASA/POWER (monthly summary)"
    city["data_quality_flag"] = np.where(city.measurement_points_available >= 0.8*city.expected_points,"monthly_aggregated","monthly_low_coverage")
    for value, anomaly in [("rainfall_mm","rainfall_anomaly_mm"),("avg_temp_c","temperature_anomaly_c")]:
        months = city.date.dt.month
        grouped = city.groupby(["city_key",months])[value]
        baseline = grouped.transform("mean")
        years = grouped.transform("count")
        city[anomaly] = (city[value]-baseline).where(years>=10)
    return city

def build_data_dictionary(point_long, city_monthly):
    definitions = {
        "city":"Standardized city name parsed from filename; spelling variants normalized.",
        "state":"State/territory mapped from the recognized city. This field is not in source headers.",
        "district":"Unavailable in source; intentionally null.",
        "date":"Month-start timestamp identifying the monthly summary period, not a daily observation.",
        "rainfall_mm":"PRECTOTCORR monthly mean daily precipitation rate; unit is mm/day.",
        "avg_temp_c":"T2M monthly average 2 m temperature, °C.",
        "max_temp_c":"T2M_MAX monthly mean of daily maximum temperature, °C.",
        "min_temp_c":"T2M_MIN monthly mean of daily minimum temperature, °C.",
        "humidity_pct":"Unavailable. QV2M is specific humidity and is not treated as relative humidity.",
        "aqi":"Unavailable in NASA/POWER files.","pm25":"Unavailable in NASA/POWER files.","ndvi":"Unavailable in NASA/POWER files.",
        "rainfall_anomaly_mm":"PRECTOTCORR minus city and calendar-month 2000–2025 mean, only with at least 10 available years; retains mm/day rate units.",
        "temperature_anomaly_c":"T2M minus city and calendar-month 2000–2025 mean, only with at least 10 available years.",
        "latitude":"Mean latitude of measurement-point coordinates from file headers.",
        "longitude":"Mean longitude of measurement-point coordinates from file headers.",
        "location_id":"Stable IN-{state code}-{city code} identifier.",
        "measurement_points_available":"Number of point files with at least one mapped climate parameter for the city-month.",
        "expected_points":"Number of discovered measurement-point files for the city.",
        "data_quality_flag":"monthly_aggregated when >=80% of expected points contribute; otherwise monthly_low_coverage.",
        "source":"NASA/POWER attribution and source temporal resolution.",
    }
    rows=[]
    for name, definition in definitions.items():
        if name in city_monthly:
            dtype=str(city_monthly[name].dtype)
        elif name in point_long:
            dtype=str(point_long[name].dtype)
        else: dtype="not applicable"
        rows.append({"field":name,"dtype":dtype,"definition_and_handling":definition})
    raw_parameters=sorted(point_long.PARAMETER.dropna().unique())
    source_descriptions = {
        "ALLSKY_SFC_SW_DIFF":"All-sky surface shortwave diffuse irradiance (kWh/m²/day)",
        "ALLSKY_SFC_SW_DNI":"All-sky surface shortwave direct normal irradiance (kWh/m²/day)",
        "ALLSKY_SFC_UV_INDEX":"All-sky surface UV index (source-scaled index)",
        "ALLSKY_SRF_ALB":"All-sky surface albedo (dimensionless)",
        "CLOUD_AMT":"Cloud amount (%)", "CLRSKY_SFC_SW_DWN":"Clear-sky surface shortwave downward irradiance (kWh/m²/day)",
        "IMERG_PRECTOT":"IMERG total precipitation (mm/day)", "PRECTOTCORR":"MERRA-2 corrected total precipitation (mm/day)",
        "PS":"Surface pressure (kPa)", "QV2M":"Specific humidity at 2 m (g/kg)",
        "T2M":"Temperature at 2 m (°C)", "T2M_MAX":"Temperature at 2 m maximum (°C)",
        "T2M_MIN":"Temperature at 2 m minimum (°C)", "TS":"Earth skin temperature (°C)",
        "WS10M":"Wind speed at 10 m (m/s)"}
    for parameter in raw_parameters:
        rows.append({"field":parameter,"dtype":"float64","definition_and_handling":source_descriptions.get(parameter,"NASA/POWER parameter retained under its original identifier; consult source header for definition and units.")})
    return pd.DataFrame(rows)
