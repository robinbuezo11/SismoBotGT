import requests

def obtener_sismos_recientes():
  url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
  data = requests.get(url).json()
  sismos = []

  for sismo in data["features"]:
    props = sismo["properties"]
    coords = sismo["geometry"]["coordinates"]
    lugar = props["place"]
    if "Guatemala" in lugar:
      sismos.append({
        "magnitud": props["mag"],
        "lugar": lugar,
        "hora": props["time"],
        "profundidad": coords[2]
      })
  return sismos if sismos else "No se reportan sismos recientes en Guatemala."