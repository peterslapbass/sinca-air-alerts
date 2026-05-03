import requests
from config import SINCA_URL

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        pollutants = {}

        for r in s.get("realtime", []):
            code = (r.get("code") or "").upper()
            value = None

            # caso simple
            if r.get("tableRow"):
                value = r["tableRow"].get("value")

            # fallback
            if value is None:
                continue

            try:
                value = float(value)
            except:
                continue

            pollutants[code] = value

        stations.append({
            "name": s.get("nombre"),
            "pollutants": pollutants,
            "source": {
                "red": s.get("red"),
                "empresa": s.get("empresa"),
                "region": s.get("region"),
                "comuna": s.get("comuna"),
                "key": s.get("key")
            }
        })

    return stations
