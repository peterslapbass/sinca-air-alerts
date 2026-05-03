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

def evaluate(stations):
    prev_state = load_state()
    new_state = {}
    alerts = []

    for s in stations:
        name = s["name"]
        pm25 = s["pm25"]

        status = "normal"
        if pm25 >= PM25_CRITICAL:
            status = "critical"
        elif pm25 >= PM25_WARNING:
            status = "warning"

        if prev_state.get(name) != status and status != "normal":
            alerts.append({
                "name": name,
                "pm25": pm25,
                "status": status
            })

        new_state[name] = status

    save_state(new_state)
    return alerts
