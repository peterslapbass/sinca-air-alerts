import json
import os
from config import PM25_WARNING, PM25_CRITICAL

STATE_FILE = "data/state.json"

def load_state():
    if not os.path.exists("data/state.json"):
        return {}

    try:
        with open("data/state.json") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_status(pm25):
    if pm25 >= 150:
        return "critical"
    elif pm25 >= 100:
        return "very_bad"
    elif pm25 >= 50:
        return "bad"
    else:
        return "ok"

def evaluate(stations):
    alerts = []

    for s in stations:
        for pollutant, value in s.get("pollutants", {}).items():

            if value is None:
                continue

            if value >= 50:  # tu regla base (puedes mejorarla después)
                alerts.append({
                    "name": s["name"],
                    "pollutant": pollutant,
                    "value": value,
                    "status": get_status(value),
                    "source": s.get("source", {})
                })

    return alerts
