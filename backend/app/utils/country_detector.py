import re

from app.utils.geo import COUNTRY_ALIASES, normalize_text, normalize_country

def detect_country(text: str) -> str:
    normalized_text = normalize_text(text)

    for alias in COUNTRY_ALIASES.keys():
        pattern = rf"\b{re.escape(alias)}\b"

        if re.search(pattern, normalized_text):
            return normalize_country(alias)

    return "guatemala"