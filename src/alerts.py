import json
import os
from config import THRESHOLDS

STATE_FILE = "data/state.json"


# =========================
# STATUS GENERAL (ESCALABLE)
# =========================
def get_status_generic(value, limit):
    ratio = value / limit

    if ratio >= 3:
        return "critical"
    elif ratio >= 2:
        return "very_bad"
    elif ratio >= 1:
        return "bad"
    else:
        return "ok"


# =========================
# STATE (MEMORIA ALERTAS)
# =========================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# =========================
# CORE EVALUATION
# =========================
def evaluate(stations):
    alerts = []

    for s in stations:
        pollutants = s.get("pollutants", {})

        for pollutant, value in pollutants.items():

            if value is None:
                continue

            limit = THRESHOLDS.get(pollutant)

            # si no hay regla definida, ignorar
            if not limit:
                continue

            status = get_status_generic(value, limit)

            if status in ["bad", "very_bad", "critical"]:
                alerts.append({
                    "name": s["name"],
                    "pollutant": pollutant,
                    "value": value,
                    "limit": limit,
                    "status": status,
                    "source": s.get("source", {})
                })

    # opcional: ordenar por severidad
    priority = {"critical": 3, "very_bad": 2, "bad": 1, "ok": 0}

    alerts.sort(key=lambda a: (priority[a["status"]], a["value"]), reverse=True)

    return alerts
