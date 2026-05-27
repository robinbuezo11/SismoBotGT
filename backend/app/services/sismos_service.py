# app/services/sismos_service.py
import requests

from datetime import datetime, timezone
from typing import Union, List, Dict
from app.utils.cache import get_cache, set_cache

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
        lugar = props.get("place", "")

        if pais.lower() in lugar.lower():
            # convertir hora
            timestamp = props.get("time")
            if timestamp:
                dt = datetime.fromtimestamp(timestamp/1000, tz=timezone.utc)
                hora_iso = dt.isoformat()
            else:
                hora_iso = None

            eventos.append({
                "magnitud": props.get("mag"),
                "lugar": lugar,
                "hora": hora_iso,
                "profundidad_km": coords[2] if len(coords) > 2 else None,
                "url_detalle": props.get("url")
            })

    if not eventos:
        return {"mensaje": f"No se reportan sismos recientes en {pais}."}

    resultado = {"sismos": eventos}

    set_cache(cache_key, resultado)

    return resultado
