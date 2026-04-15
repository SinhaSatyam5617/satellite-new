import pandas as pd
from datetime import datetime, timedelta
import random

from engine.dataset.builder import build_feature_row


# ----------------------------------
# 🇮🇳 INDIA BALANCED LOCATIONS
# ----------------------------------
locations = [

    # 🏙️ METRO
    (28.61, 77.23),   # Delhi
    (19.07, 72.87),   # Mumbai
    (13.08, 80.27),   # Chennai
    (22.57, 88.36),   # Kolkata
    (12.97, 77.59),   # Bangalore
    (17.38, 78.48),   # Hyderabad

    # 🏙️ TIER-2
    (26.84, 80.94),   # Lucknow
    (18.52, 73.85),   # Pune
    (26.91, 75.78),   # Jaipur
    (23.02, 72.57),   # Ahmedabad

    # 🌾 RURAL / AGRICULTURE
    (28.40, 77.85),   # Western UP
    (30.90, 75.85),   # Punjab
    (25.60, 85.10),   # Bihar
    (21.15, 79.08),   # Central India

    # 🌲 FOREST
    (22.30, 80.00),   # MP forest
    (20.59, 84.80),   # Odisha forest
    (10.85, 76.27),   # Kerala

    # 🏜️ DRY / DESERT
    (27.00, 71.00),   # Rajasthan
    (23.25, 77.41),   # Bhopal

    # 🏔️ MOUNTAIN
    (30.07, 79.02),   # Uttarakhand
    (34.15, 77.57),   # Ladakh

    # 🌊 COAST
    (15.49, 73.82),   # Goa
    (21.64, 69.60),   # Gujarat coast
]


# ----------------------------------
# 📅 RANDOM DATE GENERATOR
# ----------------------------------
def generate_random_dates(num_samples=40):

    base_date = datetime(2022, 1, 1)
    dates = []

    for _ in range(num_samples):
        offset = random.randint(0, 800)

        start = base_date + timedelta(days=offset)
        end = start + timedelta(days=random.randint(5, 15))

        dates.append((
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d")
        ))

    return dates


# ----------------------------------
# 📊 DATASET GENERATOR
# ----------------------------------
def generate_large_dataset():

    rows = []
    date_ranges = generate_random_dates(40)

    for lat, lon in locations:

        for start, end in date_ranges:

            # 🔥 ADD SMALL RANDOM VARIATION
            lat_var = lat + random.uniform(-0.2, 0.2)
            lon_var = lon + random.uniform(-0.2, 0.2)

            print(f"Processing: {lat_var}, {lon_var}, {start}")

            row = build_feature_row(lat_var, lon_var, start, end)

            if row and "error" not in row:

                row["lat"] = lat_var
                row["lon"] = lon_var
                row["start"] = start
                row["end"] = end

                rows.append(row)

    df = pd.DataFrame(rows)

    # ----------------------------------
    # 🔥 FIXED CLEANING (IMPORTANT)
    # ----------------------------------

    # remove only fully empty rows
    df = df.dropna(how="all")

    # fill missing values instead of deleting rows
    df = df.fillna(0)

    return df


# ----------------------------------
# 💾 SAVE DATASET
# ----------------------------------
def save_dataset(df, filename="dataset.csv"):
    df.to_csv(filename, index=False)
    return filename