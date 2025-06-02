import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")


def geocode_location(location_name):
    """
    Utiliza la API de Mapbox para obtener latitud y longitud de una ubicación textual.
    Retorna (lat, lng) si encuentra, o None si no encuentra resultados.
    """
    if not MAPBOX_API_KEY:
        raise ValueError("MAPBOX_API_KEY no está definido en el entorno o .env")
    url = (
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/"
        f"{requests.utils.quote(location_name)}.json?access_token={MAPBOX_API_KEY}&limit=1&language=es"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Error en la petición a Mapbox: {resp.status_code} {resp.text}")
    data = resp.json()
    features = data.get("features", [])
    if not features:
        return None
    coords = features[0]["center"]  # [lng, lat]
    return coords[1], coords[0]


if __name__ == "__main__":
    # Prueba rápida
    lugar = input("Ubicación a buscar: ")
    coords = geocode_location(lugar)
    if coords:
        print(f"Lat/Lng: {coords}")
    else:
        print("No encontrado")
