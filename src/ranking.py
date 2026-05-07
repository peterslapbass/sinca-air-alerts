from config import THRESHOLDS

def build_ranking(stations, pollutant):

    ranking = []

    limit = THRESHOLDS.get(pollutant)

    if not limit:
        return []

    for s in stations:

        value = s.get("pollutants", {}).get(pollutant)

        if value is None:
            continue

        ratio = value / limit

        ranking.append({
            "name": s["name"],
            "pollutant": pollutant,
            "value": value,
            "ratio": ratio,
            "source": s.get("source", {})
        })

    ranking.sort(key=lambda x: x["ratio"], reverse=True)

    return ranking
