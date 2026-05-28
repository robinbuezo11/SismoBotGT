from typing import Dict

def construir_contexto_sismico(usgs_data: Dict, insivumeh_data: Dict | None = None) -> str:
    contexto = "Información sísmica reciente:\n\n"
    
    if usgs_data.get("sismos"):
        contexto += "Sismos reportados por USGS:\n"
        for sismo in usgs_data["sismos"][:10]:
            contexto += (
                f"- Magnitud {sismo.get('magnitud')} "
                f"en: {sismo.get('lugar')} "
                f"el: {sismo.get('hora')} "
                f"con profunidad de "
                f"{sismo.get('profundidad_km')} km\n"
            )

    if insivumeh_data and insivumeh_data.get("sismos_insivumeh"):
        contexto += "\nSismos reportados por INSIVUMEH:\n"
        for sismo in insivumeh_data["sismos_insivumeh"][:10]:
            contexto += (
                f"- Magnitud {sismo.get('magnitud')} "
                f"registrado el {sismo.get('hora')} "
                f"con profunidad de "
                f"{sismo.get('profundidad_km')} km"
                f"en coordenadas ({sismo.get('latitud')}, {sismo.get('longitud')})\n"
            )

    return contexto