# app/services/sismos_service.py
import requests

from datetime import datetime, timezone
from typing import Union, List, Dict

from app.utils.cache import get_cache, set_cache
from app.utils.geo import is_in_country


USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


def obtener_sismos_recientes_usgs(pais: str = "Guatemala") -> Union[Dict, List[Dict]]:
    cache_key = f"sismos_usgs_{pais.lower()}"

    cached_data = get_cache(cache_key)
    
    if cached_data:
        return cached_data

    try:
        resp = requests.get(USGS_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        cached_data = get_cache(cache_key)

        if cached_data:
            return {
                "source": "cache",
                "data": cached_data
            }

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
            "pais": pais,
            "latitud": lat,
            "longitud": lon,
            "hora": hora_iso,
            "profundidad_km": coords[2] if len(coords) > 2 else None,
            "url_detalle": props.get("url")
        })

    eventos.sort(key=lambda x: x["magnitud"] or 0, reverse=True)

    if not eventos:
        return {"mensaje": f"No se reportan sismos recientes en {pais}."}

    resultado = {
        "pais": pais,
        "cantidad": len(eventos),
        "sismos": eventos
    }

    set_cache(cache_key, resultado)

    return resultado
