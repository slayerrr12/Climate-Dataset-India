"""Stable identifiers and small normalization utilities."""
import re
from .config import CITY_METADATA


def make_location_id(city_key):
    metadata = CITY_METADATA.get(city_key, {})
    state_code = metadata.get("state_code", "UNK")
    city_code = metadata.get("city_code", re.sub("[^A-Z]", "", city_key.upper())[:3])
    return f"IN-{state_code}-{city_code}"
