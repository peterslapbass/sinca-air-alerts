import requests
import unicodedata
from config import SINCA_URL


# =========================
# NORMALIZACIÓN TEXTO
# =========================
def normalize(text):
    if not text:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text.lower()


# =========================
# DETECCIÓN CONTAMINANTES (ESTILO FRONTEND)
# =========================
def get_pollutant(name):
    n = normalize(name)

    # MP
    if "mp-2" in n or "pm25" in n or "pm2" in n:
        return "PM25"
    if "mp-10" in n or "pm10" in n:
        return "PM10"

    # NO2
    if "dioxido de nitrogeno" in n or "no2" in n:
        return "NO2"

    # SO2
    if "dioxido de azufre" in n or "so2" in n:
        return "SO2"

    # O3
    if "ozono" in n or "o3" in n:
        return "O3"

    # CO
    if "monoxido de carbono" in n or n.strip() == "co":
        return "CO"

    return None


# =========================
# FETCH
# =========================
def fetch_data():
    response = requests.get(SINCA_URL, timeout=10)
    return response.json()


# =========================
# PARSER PRINCIPAL
# =========================
def parse_data(raw):
    stations = []

    for s in raw:
        pollutants = {}

        for r in s.get("realtime", []):
            print(r.get("code"), r.get("name"))
            # 🔥 usar TODOS los posibles campos
            raw_name = (
                r.get("name")
                or r.get("parameter")
                or r.get("code")
                or ""
            )

            code = get_pollutant(raw_name)

            # si no se reconoce contaminante → ignorar
            if not code:
                continue

            value = None

            # ✅ valor directo (mejor caso)
            if r.get("tableRow"):
                value = r["tableRow"].get("value")

            # ⚠️ fallback (por si SINCA cambia formato)
            if value is None and r.get("value") is not None:
                value = r.get("value")

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