# app/utils/geo.py

import json
import unicodedata

from typing import Dict, List

with open("app/data/country_bounds.json", "r", encoding="utf-8") as f:
    raw_bounds = json.load(f)

COUNTRY_BOUNDS: Dict[str, List[float]] = {}
COUNTRY_ALIASES: Dict[str, str] = {}


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

for iso_code, data in raw_bounds.items():
    country_name = data[0]
    bounds = data[1]

    norm_name = normalize_text(country_name)
    
    COUNTRY_BOUNDS[norm_name] = bounds
    COUNTRY_ALIASES[normalize_text(iso_code)] = norm_name
    COUNTRY_ALIASES[norm_name] = norm_name

CUSTOM_ALIASES = {
    "gt": "guatemala",
    "guate": "guatemala",

    "usa": "united states",
    "eeuu": "united states",
    "estados unidos": "united states",

    "uk": "united kingdom",
    "reino unido": "united kingdom",

    "corea del sur": "south korea",
    "corea del norte": "north korea",

    "rusia": "russia",

    "mexico": "mexico",
}

for alias, norm in CUSTOM_ALIASES.items():
    COUNTRY_ALIASES[normalize_text(alias)] = normalize_text(norm)

def normalize_country(name: str) -> str:
    norm_name = normalize_text(name)
    return COUNTRY_ALIASES.get(norm_name, norm_name)

def is_in_country(lat: float, lon: float, country: str) -> bool:
    country = normalize_country(country)

    bounds = COUNTRY_BOUNDS.get(country)

    if not bounds:
        return False

    min_lon, min_lat, max_lon, max_lat = bounds

    return (
        min_lat <= lat <= max_lat
        and
        min_lon <= lon <= max_lon
    )