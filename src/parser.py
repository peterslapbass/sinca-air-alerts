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
            code = r.get("code", "").upper()

            info = r.get("info", {})
            rows = info.get("rows", [])

            if not rows:
                continue

            last_row = rows[-1]
            cols = last_row.get("c", [])

            if len(cols) > 1:
                value = cols[1].get("v", 0)

                try:
                    pollutants[code] = float(value)
                except:
                    pollutants[code] = None

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
