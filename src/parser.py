import requests
from config import SINCA_URL

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        pm25 = 0.0

        # recorrer mediciones reales
        for r in s.get("realtime", []):
            code = r.get("code", "").upper()

            if code == "PM25":
                pm25 = float(r.get("value", 0))

        stations.append({
            "name": s.get("nombre"),
            "pm25": pm25
        })

    return stations

