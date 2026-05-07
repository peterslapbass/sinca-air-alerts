def format_alert_message(alerts):
    lines = ["🚨 Alertas de calidad del aire:\n"]

    for a in alerts:
        emoji = "🚨" if a["status"] == "critical" else "⚠️"

        pollutant = a["pollutant"]
        value = a["value"]

        source = a.get("source", {})
        red = source.get("red", "")
        region = source.get("region", "").strip()

        lines.append(
            f"{emoji} {a['name']} ({pollutant}): {value} µg/m³\n"
            f"📡 {red} · {region}"
        )

    return "\n".join(lines)


def format_ranking_message(ranking, pollutant="PM25", top=5):

    title_map = {
        "PM25": "🏆 Top PM2.5 Chile",
        "PM10": "🏆 Top PM10 Chile",
        "NO2": "🏆 Top NO₂ Chile",
        "SO2": "🏆 Top SO₂ Chile",
        "CO": "🏆 Top CO Chile",
        "O3": "🏆 Top O₃ Chile"
    }

    message = f"{title_map.get(pollutant, pollutant)}\n\n"

    for i, r in enumerate(ranking[:top], 1):

        region = r["source"].get("region", "").strip()

        message += (
            f"{i}. {r['name']} — "
            f"{r['value']} µg/m³ "
            f"({r['ratio']:.2f}x)\n"
            f"📍 {region}\n\n"
        )

    return message
