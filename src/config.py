import os

SINCA_URL = "https://sinca.mma.gob.cl/index.php/json/listadomapa2k19"

THRESHOLDS = {
    "PM25": 50,
    "PM10": 100,
    "NO2": 200,
    "SO2": 125,
    "CO": 10
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
