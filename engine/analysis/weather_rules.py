def calculate_weather_score(data):

    rain = data["rainfall"]
    temp = data["temperature"]
    humidity = data["humidity"]
    anomaly = data["anomaly"]

    # -------------------------
    # 🌡️ HEAT INDEX
    # -------------------------
    heat_index = temp + (0.33 * humidity) - 4

    # -------------------------
    # 📊 SCORES
    # -------------------------
    rain_score = min(100, (rain / 100) * 100)
    temp_score = max(0, 100 - abs(temp - 25) * 3)
    humidity_score = humidity

    anomaly_penalty = abs(anomaly) * 2

    final_score = (
        rain_score * 0.4 +
        temp_score * 0.3 +
        humidity_score * 0.2 -
        anomaly_penalty * 0.1
    )

    final_score = max(0, min(100, final_score))

    # -------------------------
    # 🏷️ LABEL
    # -------------------------
    if final_score > 75:
        label = "🟢 Good Climate"
    elif final_score > 50:
        label = "🟡 Moderate"
    else:
        label = "🔴 Risky"

    return {
        "score": round(final_score, 2),
        "label": label,
        "heat_index": round(heat_index, 2)
    }