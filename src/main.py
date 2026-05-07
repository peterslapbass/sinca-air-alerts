from parser import fetch_data, parse_data
from alerts import evaluate
from ranking import build_ranking
from messages import (
    format_alert_message,
    format_ranking_message
)

import requests
from config import TELEGRAM_TOKEN, CHAT_ID


POLLUTANTS = [
    "PM25",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3"
]


def send_telegram(message):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


def main():

    raw = fetch_data()

    stations = parse_data(raw)

    # Rankings automáticos
    for pollutant in POLLUTANTS:

        ranking = build_ranking(stations, pollutant)

        # si no hay datos para ese contaminante
        if not ranking:
            continue

        ranking_msg = format_ranking_message(
            ranking,
            pollutant=pollutant,
            top=5
        )

        print(ranking_msg)

        send_telegram(ranking_msg)

    # Alertas
    alerts = evaluate(stations)

    if alerts:

        alert_msg = format_alert_message(alerts)

        print(alert_msg)

        send_telegram(alert_msg)

    else:
        print("Sin nuevas alertas")


if __name__ == "__main__":
    main()
