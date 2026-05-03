import requests
from config import SINCA_URL

def normalize_code(code):
    c = (code or "").upper()

    mapping = {
        "DIOXIDO DE NITROGENO": "NO2",
        "NO2": "NO2",

        "DIOXIDO DE AZUFRE": "SO2",
        "SO2": "SO2",

        "MONOXIDO DE CARBONO": "CO",
        "CO": "CO",

        "OZONO": "O3",
        "O3": "O3",

        "MP-2,5": "PM25",
        "PM25": "PM25",

        "MP-10": "PM10",
        "PM10": "PM10"
    }

    return mapping.get(c, c)

def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()

def parse_data(raw):
    stations = []

    for s in raw:
        pollutants = {}

        for r in s.get("realtime", []):
            code = normalize_code(r.get("code") or r.get("name") or "")
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
