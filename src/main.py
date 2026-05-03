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
        lines.append(f"{emoji} {a['name']}: {a['pm25']} µg/m³")

    return "\n".join(lines)

def main():
    raw = fetch_data()
    stations = parse_data(raw)
    alerts = evaluate(stations)

    if alerts:
        msg = format_message(alerts)
        print(msg)
        send_telegram(msg)
    else:
        print("Sin nuevas alertas")

if __name__ == "__main__":
    main()