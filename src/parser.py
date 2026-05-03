import requests
from config import SINCA_URL

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        pm25 = 0.0

        for r in s.get("realtime", []):
            code = r.get("code", "").upper()

            if code == "PM25":
                info = r.get("info", {})
                rows = info.get("rows", [])

                if rows:
                    # tomar el último valor disponible
                    last_row = rows[-1]
                    cols = last_row.get("c", [])

                    if len(cols) > 1:
                        value = cols[1].get("v", 0)
                        pm25 = float(value)

        stations.append({
            "name": s.get("nombre"),
            "pm25": pm25
        })

    return stations

