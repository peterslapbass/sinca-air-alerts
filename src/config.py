import os

SINCA_URL = "https://sinca.mma.gob.cl/index.php/json/listadomapa2k19"

PM25_WARNING = 50
PM25_CRITICAL = 100

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
