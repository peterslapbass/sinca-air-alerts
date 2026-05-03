import requests
from config import SINCA_URL

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        stations.append({
            "name": s.get("nombre", "N/A"),
            "pm25": float(s.get("pm25") or 0)
        })

    return stations