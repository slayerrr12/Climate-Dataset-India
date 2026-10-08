from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
if not list(RAW_DIR.glob("*.csv")):
    RAW_DIR = ROOT / "datasets"
PROJECT_DIR = ROOT
INTERIM_DIR = ROOT / "data" / "interim"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"

CITY_METADATA = {
    "ahmedabad": {"city": "Ahmedabad", "state": "Gujarat", "state_code": "GJ", "city_code": "AMD"},
    "bengaluru": {"city": "Bengaluru", "state": "Karnataka", "state_code": "KA", "city_code": "BLR"},
    "bhopal": {"city": "Bhopal", "state": "Madhya Pradesh", "state_code": "MP", "city_code": "BHO"},
    "bhubaneswar": {"city": "Bhubaneswar", "state": "Odisha", "state_code": "OD", "city_code": "BBS"},
    "chandigarh": {"city": "Chandigarh", "state": "Chandigarh (Union Territory)", "state_code": "CH", "city_code": "IXC"},
    "chennai": {"city": "Chennai", "state": "Tamil Nadu", "state_code": "TN", "city_code": "MAA"},
    "coimbatore": {"city": "Coimbatore", "state": "Tamil Nadu", "state_code": "TN", "city_code": "CJB"},
    "delhi": {"city": "Delhi", "state": "Delhi (National Capital Territory)", "state_code": "DL", "city_code": "DEL"},
}
MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
FINAL_DAILY_COLUMNS = ["location_id","district","state","date","latitude","longitude","rainfall_mm","avg_temp_c","max_temp_c","min_temp_c","humidity_pct","aqi","pm25","ndvi","rainfall_anomaly_mm","temperature_anomaly_c","source","data_quality_flag"]
