import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import shap
import joblib
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models/li_model.pkl")

model = joblib.load(MODEL_PATH)

explainer = None

FEATURE_COLUMNS = [
    "ndvi","ndwi","ndbi",
    "no2","so2","co",
    "temperature","dewpoint",
    "rainfall","lst_ndvi"
]


def explain(features):

    global explainer

    if explainer is None:
        explainer = shap.Explainer(model)

    df = pd.DataFrame([features])

    df = df[FEATURE_COLUMNS]   # 🔥 FIX

    shap_values = explainer(df)

    return dict(zip(FEATURE_COLUMNS, shap_values.values[0]))