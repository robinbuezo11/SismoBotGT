import re
import requests
import urllib3

from datetime import datetime
from typing import Union, List, Dict

from app.utils.cache import get_cache, set_cache

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

INSIVUMEH_MAP_URL = "https://geo.insivumeh.gob.gt/MAPA_SISMOS/"


def obtener_sismos_recientes_insivumeh() -> Union[Dict, List[Dict]]:
    cache_key = "sismos_insivumeh_gt"
    cached_data = get_cache(cache_key)

    if cached_data:
        cached_data["source"] = "cache"
        return cached_data
    
    try:
        resp = requests.get(
            INSIVUMEH_MAP_URL,
            timeout=15,
            verify=False
        )

        resp.raise_for_status()

        html = resp.text

    except requests.RequestException as e:
        cached_data = get_cache(cache_key)
        if cached_data:
            cached_data["source"] = "cache"
            return cached_data

        return {
            "error": f"Error al consultar INSIVUMEH: {e}"
        }

    eventos = []

    pattern = re.compile(
        r'L\.circleMarker\(\s*'
        r'\[\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\].*?'
        r'Magnitud:\s*</b>\s*([0-9\.]+).*?'
        r'Tiempo de Origen:\s*</b>\s*([0-9:\-\s]+).*?'
        r'Profundidad:\s*</b>\s*([0-9\.]+)\s*km.*?'
        r'ID:\s*</b>\s*([a-zA-Z0-9]+)',
        re.DOTALL
    )

    matches = pattern.findall(html)

    for lat, lon, magnitud, tiempo, profundidad, event_id in matches:

        try:
            evento = {
                "id": event_id.strip(),
                "magnitud": float(magnitud),
                "hora": tiempo.strip(),
                "profundidad_km": float(profundidad),
                "latitud": float(lat),
                "longitud": float(lon),
                "lugar": "Guatemala",
                "fuente": "INSIVUMEH"
            }

            eventos.append(evento)

        except Exception:
            continue

    def parse_fecha(event):
        try:
            return datetime.strptime(
                event["hora"],
                "%Y-%m-%d %H:%M:%S"
            )
        except:
            return datetime.min

    eventos.sort(
        key=parse_fecha,
        reverse=True
    )

    if not eventos:
        resultado = {
            "source": "api",
            "pais": "Guatemala",
            "cantidad": 0,
            "sismos_insivumeh": [],
            "mensaje": (
                "No se encontraron sismos "
                "recientes reportados por INSIVUMEH."
            )
        }

        set_cache(cache_key, resultado)

        return resultado

    resultado = {
        "source": "api",
        "pais": "Guatemala",
        "cantidad": len(eventos),
        "sismos_insivumeh": eventos,
        "mensaje": (
            "Sismos recientes reportados "
            "por INSIVUMEH."
        )
    }

    set_cache(cache_key, resultado)

    return resultado