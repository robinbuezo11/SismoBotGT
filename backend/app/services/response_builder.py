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


def construir_contexto_sismico(usgs_data: Dict, insivumeh_data: Dict | None = None) -> str:
    contexto = "Información sísmica reciente:\n\n"

    if usgs_data.get("sismos"):
        contexto += "USGS:\n"

        sismos_usgs = eliminar_duplicados(usgs_data["sismos"])

        for sismo in sismos_usgs[:10]:
            linea = f"- "

            if sismo.get("magnitud") is not None:
                linea += f"Magnitud {sismo['magnitud']} "
            if sismo.get("lugar"):
                linea += f"en {sismo['lugar']} "
            if sismo.get("hora"):
                linea += f"el {sismo['hora']} "
            if sismo.get("profundidad_km") is not None:
                linea += f"profundidad {sismo['profundidad_km']} km"
            contexto += linea.strip() + "\n"

    if insivumeh_data and insivumeh_data.get("sismos_insivumeh"):

        contexto += "\nINSIVUMEH:\n"

        sismos_insivumeh = eliminar_duplicados(insivumeh_data["sismos_insivumeh"])

        for sismo in sismos_insivumeh[:10]:
            linea = "- "

            if sismo.get("magnitud") is not None:
                linea += f"Magnitud {sismo['magnitud']} "
            if sismo.get("hora"):
                linea += f"el {sismo['hora']} "
            if (
                sismo.get("latitud") is not None
                and sismo.get("longitud") is not None
            ):
                linea += (
                    f"coordenadas "
                    f"({sismo['latitud']}, {sismo['longitud']}) "
                )
            if sismo.get("profundidad_km") is not None:
                linea += (
                    f"profundidad "
                    f"{sismo['profundidad_km']} km"
                )

            contexto += linea.strip() + "\n"

    return contexto