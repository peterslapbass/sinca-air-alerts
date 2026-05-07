from parser import fetch_data, parse_data
from alerts import evaluate
from ranking import build_ranking

import requests

from config import TELEGRAM_TOKEN, CHAT_ID


def send_telegram(message):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


def format_alerts(alerts):

    lines = ["🚨 Alertas de calidad del aire:\n"]

    for a in alerts:

        emoji = "🚨" if a["status"] == "critical" else "⚠️"

        pollutant = a["pollutant"]
        value = a["value"]

        source = a.get("source", {})
        red = source.get("red", "")
        region = source.get("region", "")

        lines.append(
            f"{emoji} {a['name']} ({pollutant}): "
            f"{value} µg/m³\n"
            f"📡 {red} · {region}"
        )

    return "\n\n".join(lines)


def format_ranking(stations, pollutant="PM25", top=5):

    ranking = build_ranking(stations, pollutant)

    if not ranking:
        return None

    lines = [f"🏆 Top {pollutant} Chile\n"]

    for i, r in enumerate(ranking[:top], 1):

        lines.append(
            f"{i}. {r['name']} — "
            f"{r['value']} µg/m³ "
            f"({r['ratio']:.2f}x)"
        )

    return "\n".join(lines)


def main():

    raw = fetch_data()

    stations = parse_data(raw)

    print("STATIONS COUNT:", len(stations))

    # =========================
    # RANKING
    # =========================

    ranking_msg = format_ranking(stations, "PM25")

    if ranking_msg:
        print(ranking_msg)
        send_telegram(ranking_msg)

    # =========================
    # ALERTS
    # =========================

    alerts = evaluate(stations)

    print("ALERTS:", alerts)

    if alerts:

        alerts_msg = format_alerts(alerts)

        print(alerts_msg)

        send_telegram(alerts_msg)

    else:
        print("Sin nuevas alertas")


if __name__ == "__main__":
    main()
