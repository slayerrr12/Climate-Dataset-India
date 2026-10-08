import re
from pathlib import Path
import numpy as np
import pandas as pd
from .config import RAW_DIR, CITY_METADATA, MONTHS
from .cleaning import clean_source_values

FILENAME_RE = re.compile(r"^(?P<city>.+?)(?:[_ ](?P<point>\d+))?$", re.I)

def parse_filename(path):
    match = FILENAME_RE.match(Path(path).stem)
    if not match:
        raise ValueError(f"Cannot parse city and point from {Path(path).name}")
    key = re.sub(r"[_ ]+", " ", match.group("city")).strip().lower()
    key = {"ahemdabad":"ahmedabad", "bhubhaneswar":"bhubaneswar"}.get(key, key)
    return key, int(match.group("point") or 1)

def discover_files(raw_dir=RAW_DIR):
    files = sorted(Path(raw_dir).glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files in {raw_dir}")
    rows = []
    for path in files:
        city_key, point = parse_filename(path)
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        coord = re.search(r"Location:\s*Latitude\s+([-+\d.]+)\s+Longitude\s+([-+\d.]+)", text)
        if not coord:
            raise ValueError(f"Coordinates missing in {path.name}")
        metadata = CITY_METADATA.get(city_key, {})
        end = _header_end(text.splitlines(), path.name)
        source_table = pd.read_csv(path, skiprows=end + 1)
        source_table = clean_source_values(source_table)
        years = pd.to_numeric(source_table.get("YEAR"), errors="coerce").dropna()
        rows.append({"source_file":path.name,"city_key":city_key,"city":metadata.get("city",city_key.title()),
                     "measurement_point_id":point,"latitude":float(coord.group(1)),"longitude":float(coord.group(2)),
                     "number_of_rows":len(source_table),"number_of_columns":len(source_table.columns),
                     "date_min":pd.Timestamp(int(years.min()),1,1) if len(years) else pd.NaT,
                     "date_max":pd.Timestamp(int(years.max()),12,31) if len(years) else pd.NaT,
                     "schema_signature":"|".join(source_table.columns),
                     "file_bytes":path.stat().st_size,"source":"NASA/POWER"})
    inventory = pd.DataFrame(rows)
    if inventory.duplicated(["city_key","measurement_point_id"]).any():
        raise ValueError("Duplicate measurement point identifiers detected within a city")
    return inventory

def _header_end(lines, filename):
    for i, line in enumerate(lines):
        if line.strip() == "-END HEADER-":
            return i
    raise ValueError(f"Missing -END HEADER- in {filename}")

def read_point_file(path, inventory_row):
    path = Path(path)
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines()
    end = _header_end(lines, path.name)
    raw = pd.read_csv(path, skiprows=end + 1)
    raw = clean_source_values(raw)
    id_cols = ["PARAMETER","YEAR"]
    month_long = raw.melt(id_vars=id_cols, value_vars=[m for m in MONTHS if m in raw], var_name="month_name", value_name="value")
    month_long["date"] = pd.to_datetime(month_long["YEAR"].astype("string") + "-" + month_long["month_name"], format="%Y-%b", errors="coerce")
    annual = raw[["PARAMETER","YEAR","ANN"]].rename(columns={"ANN":"value"})
    annual["date"] = pd.to_datetime(annual["YEAR"].astype("string") + "-12-31", errors="coerce")
    annual["summary_period"] = "annual"
    month_long["summary_period"] = "monthly"
    common = {"source_file":inventory_row.name,"city_key":inventory_row["city_key"],"city":inventory_row["city"],
              "measurement_point_id":int(inventory_row["measurement_point_id"]),"latitude":float(inventory_row["latitude"]),
              "longitude":float(inventory_row["longitude"]),"source":"NASA/POWER"}
    for frame in (month_long, annual):
        for key, value in common.items(): frame[key] = value
    month_long = month_long.dropna(subset=["date"])
    annual = annual.dropna(subset=["date"])
    keep = ["city_key","city","measurement_point_id","source_file","date","PARAMETER","value","latitude","longitude","summary_period","source"]
    return month_long[keep], annual[keep]

def read_all_points(inventory, raw_dir=RAW_DIR):
    monthly, annual = [], []
    lookup = inventory.set_index("source_file")
    for filename in inventory.source_file:
        m, a = read_point_file(Path(raw_dir)/filename, lookup.loc[filename])
        monthly.append(m); annual.append(a)
    return pd.concat(monthly, ignore_index=True), pd.concat(annual, ignore_index=True)
