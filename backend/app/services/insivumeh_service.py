# app/services/insivumeh_service.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import Union, List, Dict

INSIVUMEH_URL = "https://insivumeh.gob.gt/?p=6863"

def obtener_sismos_recientes_insivumeh() -> Union[Dict, List[Dict]]:
    try:
        resp = requests.get(INSIVUMEH_URL, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except requests.RequestException as e:
        return {"error": f"Error al consultar INSIVUMEH: {e}"}

    soup = BeautifulSoup(html, "html.parser")
    # Aquí debes inspeccionar la estructura real del HTML para extraer lista de eventos
    eventos = []
    # Ejemplo ficticio de crawling: supongamos cada evento está en <div class="evento">
    for div in soup.select("div.evento"):
        magnitud = div.select_one(".magnitud").text.strip()
        lugar = div.select_one(".lugar").text.strip()
        hora_text = div.select_one(".hora").text.strip()
        # parsear hora_text a datetime
        # extraer profundidad si aparece
        eventos.append({
            "magnitud": float(magnitud),
            "lugar": lugar,
            "hora": hora_text,
            "profundidad_km": None
        })

    if not eventos:
        return {"mensaje": "No se encontraron eventos recientes en INSIVUMEH."}

    return {"sismos_insivumeh": eventos}
