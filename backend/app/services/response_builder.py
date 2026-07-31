from datetime import datetime, timedelta
from typing import Dict

def eliminar_duplicados(lista):
    vistos = set()
    resultado = []

    for s in lista:
        clave = (
            s.get("hora"),
            s.get("magnitud"),
            s.get("latitud"),
            s.get("longitud"),
        )

        if clave not in vistos:
            vistos.add(clave)
            resultado.append(s)

    return resultado


def convertir_fecha(fecha):
    if not fecha:
        return None

    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    for formato in formatos:
        try:
            return datetime.strptime(fecha, formato)
        except ValueError:
            pass

    try:
        return datetime.fromisoformat(
            fecha.replace("Z", "+00:00")
        ).replace(tzinfo=None)
    except Exception:
        return None


def filtrar_sismos_por_fecha(sismos, fecha_inicio, fecha_fin):

    fecha_inicio = convertir_fecha(fecha_inicio)
    fecha_fin = convertir_fecha(fecha_fin)

    resultado = []

    for sismo in sismos:

        hora = convertir_fecha(sismo.get("hora"))

        if hora is None:
            continue

        if fecha_inicio <= hora <= fecha_fin:
            resultado.append(sismo)

    return resultado


def construir_contexto_sismico(usgs_data: Dict, insivumeh_data: Dict | None = None) -> str:
    contexto = "Información sísmica reciente:\n\n"

    if usgs_data.get("sismos"):
        contexto += "USGS:\n"

        sismos_usgs = eliminar_duplicados(usgs_data["sismos"])

        for sismo in sismos_usgs[:10]:
            maps_url = (
                f"https://www.google.com/maps/search/?api=1&query={sismo['latitud']},{sismo['longitud']}"
            )
            
            linea = (
                f"- Fuente: USGS\n"
                f"  Magnitud: {sismo.get('magnitud', 'N/A')}\n"
                f"  Lugar: {sismo.get('lugar', 'N/A')}\n"
                f"  Hora: {sismo.get('hora', 'N/A')}\n"
                f"  Profundidad: {sismo.get('profundidad_km', 'N/A')} km\n"
                f"  Coordenadas: ({sismo.get('latitud', 'N/A')}, {sismo.get('longitud', 'N/A')})\n"
                f"  Google Maps: [Ver en Google Maps]({maps_url})\n"
                f"  Detalle: [Ver detalles]({sismo.get('url_detalle', 'N/A')})\n"
            )

            contexto += linea + "\n"

    if insivumeh_data and insivumeh_data.get("sismos_insivumeh"):

        contexto += "\nINSIVUMEH:\n"

        sismos_insivumeh = eliminar_duplicados(insivumeh_data["sismos_insivumeh"])

        for sismo in sismos_insivumeh[:10]:
            maps_url = (
                f"https://www.google.com/maps/search/?api=1&query={sismo['latitud']},{sismo['longitud']}"
            )

            linea = (
                f"- Fuente: INSIVUMEH\n"
                f"  Magnitud: {sismo.get('magnitud', 'N/A')}\n"
                f"  Hora: {sismo.get('hora', 'N/A')}\n"
                f"  Profundidad: {sismo.get('profundidad_km', 'N/A')} km\n"
                f"  Coordenadas: ({sismo.get('latitud', 'N/A')}, {sismo.get('longitud', 'N/A')})\n"
                f"  Google Maps: [Ver en Google Maps]({maps_url})\n"
            )

            contexto += linea + "\n"

    return contexto


def construir_eventos_sismicos(usgs_data: Dict, insivumeh_data: Dict | None = None) -> list:
    eventos = []

    if usgs_data.get("sismos"):
        for s in filtrar_sismos_por_fecha(eliminar_duplicados(usgs_data["sismos"]), 
                                          fecha_inicio=(datetime.utcnow() - timedelta(days=1)).isoformat() + "Z", 
                                          fecha_fin=datetime.utcnow().isoformat() + "Z"):
            eventos.append({
                "id": s.get("url_detalle").split("/")[-1] if s.get("url_detalle") else None,
                "source": "USGS",
                "magnitude": s.get("magnitud"),
                "place": s.get("lugar"),
                "depth": s.get("profundidad_km"),
                "time": s.get("hora"),
                "latitude": s.get("latitud"),
                "longitude": s.get("longitud"),
                "maps_url": (
                    f"https://www.google.com/maps/search/?api=1&query={s.get('latitud')},{s.get('longitud')}"
                ) if s.get("latitud") and s.get("longitud") else None,
                "detail_url": s.get("url_detalle")
            })

    if insivumeh_data and insivumeh_data.get("sismos_insivumeh"):
        for s in filtrar_sismos_por_fecha(eliminar_duplicados(insivumeh_data["sismos_insivumeh"]), 
                                          fecha_inicio=(datetime.utcnow() - timedelta(days=1)).isoformat() + "Z", 
                                          fecha_fin=datetime.utcnow().isoformat() + "Z"):
            eventos.append({
                "id": s.get("id"),
                "source": "INSIVUMEH",
                "magnitude": s.get("magnitud"),
                "place": s.get("lugar", "Guatemala"),
                "depth": s.get("profundidad_km"),
                "time": s.get("hora"),
                "latitude": s.get("latitud"),
                "longitude": s.get("longitud"),
                "maps_url": (
                    f"https://www.google.com/maps/search/?api=1&query={s.get('latitud')},{s.get('longitud')}"
                ) if s.get("latitud") and s.get("longitud") else None,
                "detail_url": None
            })

    eventos.sort(
        key=lambda e: e.get("magnitude") if e.get("magnitude") is not None else 0,
        reverse=True
    )

    return eventos