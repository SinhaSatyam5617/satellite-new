import sys
import os

# 🔥 FIX IMPORT PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import joblib
import numpy as np

from engine.dataset.builder import build_feature_row


# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load("saved_models/best_model.pkl")


def predict_aqi(lat, lon, start_date, end_date):

    # -----------------------------
    # FETCH SATELLITE DATA
    # -----------------------------
    row = build_feature_row(lat, lon, start_date, end_date)

    print("📡 Satellite row:", row)  # DEBUG

    # -----------------------------
    # ERROR CHECK
    # -----------------------------
    if "error" in row:
        return row

    # -----------------------------
    # SAFE EXTRACTION (IMPORTANT)
    # -----------------------------
    co = row.get("CO") or 0
    no2 = row.get("NO2") or 0
    o3 = row.get("O3") or 0

    # If ALL missing → stop
    if co == 0 and no2 == 0 and o3 == 0:
        return {"error": "No satellite pollution data available for this date/location"}

    # -----------------------------
    # FEATURE ENGINEERING
    # -----------------------------
    pollution_sum = co + no2 + o3
    pollution_mean = pollution_sum / 3
    pollution_max = max(co, no2, o3)
    pollution_min = min(co, no2, o3)

    log_CO = np.log1p(co)
    log_NO2 = np.log1p(no2)
    log_O3 = np.log1p(o3)

    CO_NO2 = co * no2
    O3_NO2 = o3 * no2
    CO_O3 = co * o3

    CO_ratio = co / (pollution_sum + 1)
    NO2_ratio = no2 / (pollution_sum + 1)
    O3_ratio = o3 / (pollution_sum + 1)

    # -----------------------------
    # MODEL INPUT
    # -----------------------------
    input_data = np.array([[
        co,
        o3,
        no2,
        pollution_sum,
        pollution_mean,
        pollution_max,
        pollution_min,
        log_CO,
        log_NO2,
        log_O3,
        CO_NO2,
        O3_NO2,
        CO_O3,
        CO_ratio,
        NO2_ratio,
        O3_ratio
    ]])

    # -----------------------------
    # PREDICT
    # -----------------------------
    prediction = model.predict(input_data)[0]

    return {
        "aqi": float(prediction),
        "features": row
    }