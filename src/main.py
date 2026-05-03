from parser import fetch_data, parse_data
from alerts import evaluate
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

def format_message(alerts):
    lines = ["🚨 Alertas de calidad del aire:\n"]

    for a in alerts:
        emoji = "🚨" if a["status"] == "critical" else "⚠️"

        source = a.get("source", {})
        red = source.get("red", "Desconocida")
        region = source.get("region", "")

        pollutant = a.get("pollutant", "PM25")

        lines.append(
            f"{emoji} {a['name']} ({pollutant}): {a['pm25']} µg/m³\n"
            f"📡 {red} · {region}"
        )

    return "\n".join(lines)

def main():
    raw = fetch_data()
    print("RAW TYPE:", type(raw))
    print("RAW SAMPLE:", str(raw)[:300])
    stations = parse_data(raw)
    print("STATIONS COUNT:", len(stations))
    print("STATIONS SAMPLE:", stations[:5])
    alerts = evaluate(stations)
    print("ALERTS:", alerts)

    if alerts:
        msg = format_message(alerts)
        print(msg)
        send_telegram(msg)
    else:
        print("Sin nuevas alertas")

if __name__ == "__main__":
    main()
