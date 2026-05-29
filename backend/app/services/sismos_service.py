# app/services/sismos_service.py
import requests

from datetime import datetime, timezone
from typing import Union, List, Dict

from app.utils.cache import get_cache, set_cache
from app.utils.geo import is_in_country, normalize_country

from app.core.config import settings


USGS_API_URL = settings.USGS_URL

def obtener_sismos_recientes_usgs(pais: str = "Guatemala") -> Union[Dict, List[Dict]]:
    pais = normalize_country(pais)
    cache_key = f"sismos_usgs_{pais.lower()}"

    cached_data = get_cache(cache_key)
    
    if cached_data:
        cached_data["source"] = "cache"
        return cached_data

    try:
        resp = requests.get(USGS_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        cached_data = get_cache(cache_key)

        if cached_data:
            cached_data["source"] = "cache"
            return cached_data

        return {"error": f"Error al consultar USGS: {e}"}

    eventos = []
    for feat in data.get("features", []):
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates", [None, None, None])

        if len(coords) < 2:
            continue

        lon = coords[0]
        lat = coords[1]

        if lat is None or lon is None:
            continue

        if not is_in_country(lat, lon, pais):
            continue

        timestamp = props.get("time")
        if timestamp:
            dt = datetime.fromtimestamp(timestamp/1000, tz=timezone.utc)
            hora_iso = dt.isoformat()
        else:
            hora_iso = None

        eventos.append({
            "magnitud": props.get("mag"),
            "lugar": props.get("place", ""),
            "pais": pais.title(),
            "latitud": lat,
            "longitud": lon,
            "hora": hora_iso,
            "profundidad_km": coords[2] if len(coords) > 2 else None,
            "url_detalle": props.get("url")
        })

    eventos.sort(key=lambda x: x["magnitud"] or 0, reverse=True)

    if not eventos:
        return {
            "pais": pais.title(),
            "cantidad": 0,
            "sismos": [],
            "mensaje": f"No se encontraron sismos recientes en {pais.title()}."
        }

    resultado = {
        "source": "api",
        "pais": pais.title(),
        "cantidad": len(eventos),
        "sismos": eventos
    }

    set_cache(cache_key, resultado)

    return resultado
