import pandas as pd
import os

# -----------------------------
# INPUT FILE PATH
# -----------------------------
input_path = "data_files/global_air_quality_data_10000.csv"

# -----------------------------
# OUTPUT FILE PATH
# -----------------------------
output_path = "data_files/clean_global_dataset.csv"

print("📂 Loading dataset...")

df = pd.read_csv(input_path)

# -----------------------------
# 1. DROP BAD ROWS
# -----------------------------
df = df.dropna()

# -----------------------------
# 2. FIX DATE
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# -----------------------------
# 3. ADD TIME FEATURES
# -----------------------------
df["month"] = df["Date"].dt.month
df["day"] = df["Date"].dt.day

# -----------------------------
# 4. REMOVE OUTLIERS
# -----------------------------
df = df[(df["PM2.5"] > 5) & (df["PM2.5"] < 300)]

# -----------------------------
# 5. ENCODE CATEGORICAL
# -----------------------------
df["City"] = df["City"].astype("category").cat.codes
df["Country"] = df["Country"].astype("category").cat.codes

# -----------------------------
# 6. SELECT FINAL COLUMNS
# -----------------------------
final_columns = [
    "City", "Country",
    "PM2.5", "PM10", "NO2", "SO2", "CO", "O3",
    "Temperature", "Humidity", "Wind Speed",
    "month", "day"
]

df = df[final_columns]

print("✅ Cleaned dataset shape:", df.shape)

# -----------------------------
# 7. SAVE FILE
# -----------------------------
os.makedirs("data_files", exist_ok=True)

df.to_csv(output_path, index=False)

print(f"💾 Saved cleaned dataset → {output_path}")