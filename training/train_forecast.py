import pandas as pd
import numpy as np
import joblib
import os

from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor


# -----------------------------
# CREATE LAG FEATURES
# -----------------------------
def create_lag_features(df, lags=3):
    for i in range(1, lags + 1):
        df[f"lag_{i}"] = df.groupby("City")["aqi_proxy_pm25"].shift(i)
    return df


def train_forecast(csv_path="data_files/all-state-aqi.csv"):
    print("📂 Loading dataset...")

    df = pd.read_csv(csv_path)

    # -----------------------------
    # SORT BY CITY + TIME
    # -----------------------------
    df = df.sort_values(["City", "Year", "week"])

    # -----------------------------
    # CREATE LAG FEATURES
    # -----------------------------
    df = create_lag_features(df, lags=3)

    # Drop missing (from lag creation)
    df = df.dropna()

    # -----------------------------
    # ENCODE CITY
    # -----------------------------
    df["City"] = df["City"].astype("category").cat.codes

    # -----------------------------
    # FEATURES & TARGET
    # -----------------------------
    X = df[
        [
            "lag_1", "lag_2", "lag_3",
            "temp_mean", "precip_sum",
            "City"
        ]
    ]

    y = df["aqi_proxy_pm25"]

    print("📊 Features used:", X.columns)
    print("📈 Total samples:", len(df))

    # -----------------------------
    # TRAIN / TEST SPLIT (TIME SAFE)
    # -----------------------------
    split = int(len(df) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # -----------------------------
    # MODEL
    # -----------------------------
    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05
    )

    print("🚀 Training Forecast Model...")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print(f"Forecast Model → RMSE: {rmse:.2f}, R2: {r2:.3f}")

    # -----------------------------
    # SAVE MODEL
    # -----------------------------
    os.makedirs("saved_models", exist_ok=True)

    joblib.dump(model, "saved_models/forecast_model.pkl")

    print("✅ Forecast model saved!")


if __name__ == "__main__":
    train_forecast()
