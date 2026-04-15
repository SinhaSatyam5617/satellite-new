import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_squared_error

from xgboost import XGBRegressor

# 🔥 import your central feature definition
from li_models.feature_builder_li import FEATURE_COLUMNS


# -----------------------------
# TRAIN FUNCTION
# -----------------------------
def train_model():

    # ✅ LOAD YOUR FINAL DATASET
    df = pd.read_csv("dataset/final_dataset_real_1000.csv")

    print("📊 Dataset loaded:", df.shape)

    # -----------------------------
    # FEATURES & TARGETS
    # -----------------------------
    TARGET_COLUMNS = [ "heat_score", "flood_score", "veg_score"]

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMNS]

    # -----------------------------
    # SPLIT
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("✅ Data split:", X_train.shape)

    # -----------------------------
    # MODEL (MULTI OUTPUT)
    # -----------------------------
    base_model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model = MultiOutputRegressor(base_model)

    # -----------------------------
    # TRAIN
    # -----------------------------
    model.fit(X_train, y_train)

    print("🚀 Model trained")

    # -----------------------------
    # EVALUATE
    # -----------------------------
    y_pred = model.predict(X_test)

    for i, col in enumerate(TARGET_COLUMNS):
        r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mean_squared_error(y_test.iloc[:, i], y_pred[:, i]))

        print(f"\n🎯 {col.upper()}")
        print("R2:", round(r2, 3))
        print("RMSE:", round(rmse, 3))

    # -----------------------------
    # SAVE (INSIDE YOUR STRUCTURE)
    # -----------------------------
    os.makedirs("li_models", exist_ok=True)

    joblib.dump(model, "li_models/xgb_multi_model.pkl")
    joblib.dump(FEATURE_COLUMNS, "li_models/features.pkl")

    print("\n💾 Model saved inside li_models/")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    train_model()