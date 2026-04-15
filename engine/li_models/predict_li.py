import sys, os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)

import ee
try:
    ee.Initialize(project='satellite-new-489422')
except:
    ee.Authenticate()
    ee.Initialize(project='satellite-new-489422')

import joblib
from datetime import datetime

from engine.li_models.feature_builder_li import build_feature_row_range
from engine.location_intelligence.risk_engine import classify_risks

MODEL_PATH = os.path.join(ROOT_DIR, "li_models", "xgb_multi_model.pkl")
model = joblib.load(MODEL_PATH)


def predict_location_range(lat, lon, start_date_str, end_date_str):

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # -----------------------------
        # BUILD FEATURES (MULTI-DAY)
        # -----------------------------
        features, raw = build_feature_row_range(lat, lon, start_date, end_date)

        missing = [k for k, v in raw.items() if v is None or v == 0]

        # -----------------------------
        # MODEL PREDICTION
        # -----------------------------
        pred = model.predict([features])[0]

        # 🔥 CLAMP VALUES
        heat = max(0, min(100, float(pred[0])))
        flood = max(0, min(100, float(pred[1])))
        veg = max(0, min(100, float(pred[2])))

        predictions = {
            "heat_score": round(heat, 2),
            "flood_score": round(flood, 2),
            "veg_score": round(veg, 2),
        }

        insights = classify_risks(predictions)

        return {
            "location": {
                "lat": lat,
                "lon": lon,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "mode": "multi-day mean"
            },
            "environment": raw,
            "missing": missing,
            "predictions": predictions,
            "insights": insights
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print(predict_location_range(13.08, 80.27, "2023-12-01", "2023-12-07"))