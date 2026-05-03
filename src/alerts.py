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

def get_status(pollutant, value):

    if pollutant == "PM25":
        if value >= 150:
            return "critical"
        elif value >= 100:
            return "very_bad"
        elif value >= 50:
            return "bad"

    if pollutant == "PM10":
        if value >= 200:
            return "critical"
        elif value >= 100:
            return "bad"

    if pollutant in ["NO2", "SO2", "O3", "CO"]:
        if value >= 100:
            return "bad"

    return "ok"

def evaluate(stations):
    alerts = []

    for s in stations:
        for pollutant, value in s.get("pollutants", {}).items():

            if value is None:
                continue

            status = get_status(pollutant, value)

            if status in ["bad", "very_bad", "critical"]:
                alerts.append({
                    "name": s["name"],
                    "pollutant": pollutant,
                    "value": value,
                    "status": status,
                    "source": s.get("source", {})
                })

    return alerts
