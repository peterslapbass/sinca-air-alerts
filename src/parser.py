import requests
from config import SINCA_URL

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        pm25 = None

        for r in s.get("realtime", []):
            if r.get("code", "").upper() != "PM25":
                continue

            value = (
                r.get("info", {})
                 .get("tableRow", {})
                 .get("value")
            )

            try:
                value = float(value)
            except:
                continue

            # ignorar basura
            if value <= 0:
                continue

            pm25 = value  # guardar último válido

        stations.append({
            "name": s.get("nombre"),
            "pm25": pm25 if pm25 is not None else 0
        })

    return stations

