import numpy as np


def analyze_timeseries(ndvi, rainfall, temperature):

    ndvi_arr = np.array(ndvi)
    rain_arr = np.array(rainfall)
    temp_arr = np.array(temperature)

    # -------------------------
    # 📈 TREND (SLOPE)
    # -------------------------
    slope = np.polyfit(range(len(ndvi_arr)), ndvi_arr, 1)[0]

    # -------------------------
    # 📊 VOLATILITY
    # -------------------------
    volatility = np.std(ndvi_arr)

    # -------------------------
    # 📉 ANOMALY
    # -------------------------
    avg_ndvi = np.mean(ndvi_arr)
    current_ndvi = ndvi_arr[-1]
    anomaly = current_ndvi - avg_ndvi

    # -------------------------
    # 🎯 SCORE (0–100)
    # -------------------------
    score = (avg_ndvi + 1) / 2 * 100

    # -------------------------
    # ⚠️ RISK LOGIC
    # -------------------------
    risks = []

    if slope < -0.02:
        risks.append("Vegetation declining")

    if volatility > 0.15:
        risks.append("High environmental instability")

    if np.mean(rain_arr) < 10:
        risks.append("Drought risk")

    if np.mean(temp_arr) > 35:
        risks.append("Heat stress")

    if not risks:
        risks.append("Stable ecosystem")

    return {
        "score": round(score, 2),
        "slope": round(slope, 4),
        "volatility": round(volatility, 3),
        "anomaly": round(anomaly, 3),
        "current_ndvi": round(current_ndvi, 3),
        "risks": risks
    }