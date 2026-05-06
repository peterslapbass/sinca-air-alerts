import requests
import html
from config import SINCA_URL


def normalize_code(code):
    c = html.unescape((code or "").strip().upper())

    mapping = {
        # códigos numéricos SINCA
        "0001": "SO2",
        "0003": "NO2",
        "0004": "CO",
        "0008": "O3",

        # nombres largos
        "DIOXIDO DE NITROGENO": "NO2",
        "DIÓXIDO DE NITRÓGENO": "NO2",

        "DIOXIDO DE AZUFRE": "SO2",
        "DIÓXIDO DE AZUFRE": "SO2",

        "MONOXIDO DE CARBONO": "CO",
        "MONÓXIDO DE CARBONO": "CO",

        "OZONO": "O3",

        # MP
        "MP-2,5": "PM25",
        "MP2,5": "PM25",
        "PM25": "PM25",

        "MP-10": "PM10",
        "PM10": "PM10",
    }

    return mapping.get(c, c)


def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()


def extract_value(r):
    """
    Intenta sacar el valor desde distintas estructuras posibles
    """
    # 1. estructura común
    if r.get("tableRow") and r["tableRow"].get("value") is not None:
        return r["tableRow"]["value"]

    # 2. algunas veces viene directo
    if r.get("value") is not None:
        return r["value"]

    # 3. fallback raro (por si cambia API)
    if isinstance(r.get("tableRow"), dict):
        return r["tableRow"].get("valor")

    return None


def parse_data(raw):
    stations = []

    for s in raw:
        pollutants = {}

        for r in s.get("realtime", []):

            raw_code = r.get("code") or r.get("name") or ""
            code = normalize_code(raw_code)

            value = extract_value(r)

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