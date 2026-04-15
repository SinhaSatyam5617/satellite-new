import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from engine.models.ml_models import get_models


def train_models(csv_path="data_files/all-state-aqi.csv"):
    print("📂 Loading dataset...")

    df = pd.read_csv(csv_path)

    # -----------------------------
    # REMOVE LEAKAGE COLUMNS
    # -----------------------------
    df = df.drop(columns=[
        "AQI Category",
        "CO AQI Category",
        "Ozone AQI Category",
        "NO2 AQI Category",
        "PM2.5 AQI Value",       # ❌ leakage
        "PM2.5 AQI Category"
    ], errors="ignore")

    # -----------------------------
    # FEATURE ENGINEERING 🔥
    # -----------------------------
    df["pollution_sum"] = (
        df["CO AQI Value"] +
        df["Ozone AQI Value"] +
        df["NO2 AQI Value"]
    )

    df["pollution_mean"] = df["pollution_sum"] / 3

    df["pollution_max"] = df[
        ["CO AQI Value", "Ozone AQI Value", "NO2 AQI Value"]
    ].max(axis=1)

    df["pollution_min"] = df[
        ["CO AQI Value", "Ozone AQI Value", "NO2 AQI Value"]
    ].min(axis=1)

    # Log transforms (non-linear boost)
    df["log_CO"] = np.log1p(df["CO AQI Value"])
    df["log_NO2"] = np.log1p(df["NO2 AQI Value"])
    df["log_O3"] = np.log1p(df["Ozone AQI Value"])

    # Interaction features 🔥
    df["CO_NO2"] = df["CO AQI Value"] * df["NO2 AQI Value"]
    df["O3_NO2"] = df["Ozone AQI Value"] * df["NO2 AQI Value"]
    df["CO_O3"] = df["CO AQI Value"] * df["Ozone AQI Value"]

    # Ratio features 🔥
    df["CO_ratio"] = df["CO AQI Value"] / (df["pollution_sum"] + 1)
    df["NO2_ratio"] = df["NO2 AQI Value"] / (df["pollution_sum"] + 1)
    df["O3_ratio"] = df["Ozone AQI Value"] / (df["pollution_sum"] + 1)

    # -----------------------------
    # FEATURES & TARGET
    # -----------------------------
    X = df[
        [
            "CO AQI Value",
            "Ozone AQI Value",
            "NO2 AQI Value",
            "pollution_sum",
            "pollution_mean",
            "pollution_max",
            "pollution_min",
            "log_CO",
            "log_NO2",
            "log_O3",
            "CO_NO2",
            "O3_NO2",
            "CO_O3",
            "CO_ratio",
            "NO2_ratio",
            "O3_ratio"
        ]
    ]

    y = df["AQI Value"]

    print("📊 Features used:", X.columns)

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    # Remove extreme AQI values
    df = df[(y > 0) & (y < 500)]
    X = X.loc[df.index]
    y = y.loc[df.index]

    # -----------------------------
    # TRAIN TEST SPLIT
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # LOAD MODELS
    # -----------------------------
    models = get_models()

    best_model = None
    best_score = -np.inf
    best_name = ""

    # -----------------------------
    # TRAIN LOOP
    # -----------------------------
    for name, model in models.items():
        print(f"\n🚀 Training {name}...")

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        print(f"{name} → RMSE: {rmse:.2f}, R2: {r2:.3f}")

        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name

    # -----------------------------
    # SAVE MODEL
    # -----------------------------
    print(f"\n🏆 Best Model: {best_name}")

    os.makedirs("saved_models", exist_ok=True)

    joblib.dump(best_model, "saved_models/best_model.pkl")
    joblib.dump(X.columns.tolist(), "saved_models/features.pkl")

    print("✅ Model saved in saved_models/")


if __name__ == "__main__":
    train_models()