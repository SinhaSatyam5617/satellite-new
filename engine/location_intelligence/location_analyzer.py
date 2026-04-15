import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from engine.location_intelligence.data_merger import get_location_features
from engine.li_models.feature_builder_li import build_features
from engine.li_models.predict_li import predict
from engine.li_models.shap_explainer import explain
from engine.location_intelligence.risk_engine import calculate_risk, get_risk_label
from engine.location_intelligence.insight_engine import generate_insights


def analyze_location(lat, lon, date):

    # STEP 1: Satellite data
    raw_data = get_location_features(lat, lon, date)

    if "error" in raw_data:
        return raw_data

    # STEP 2: Build ML features
    features = build_features(raw_data)

    # STEP 3: ML Prediction
    prediction = predict(features)

    # STEP 4: SHAP (IMPORTANT → BEFORE adding AQI)
    shap_values = explain(features)

    # STEP 5: Add AQI after SHAP
    features["aqi"] = prediction

    # STEP 6: Risk
    score = calculate_risk(features)
    risk = get_risk_label(score)

    # STEP 7: Insights
    insights = generate_insights(features, risk)

    return {
        "prediction": prediction,
        "risk": risk,
        "score": score,
        "features": features,
        "shap": shap_values,
        "insights": insights
    }