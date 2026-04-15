import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

NUM_ROWS = 1500

locations = [
    (28.61, 77.20),  # Delhi
    (19.07, 72.87),  # Mumbai
    (13.08, 80.27),  # Chennai
    (22.57, 88.36),  # Kolkata
    (26.85, 80.95),  # Lucknow
    (12.97, 77.59),  # Bangalore
    (23.02, 72.57),  # Ahmedabad
    (17.38, 78.48),  # Hyderabad
]

start_date = datetime(2023, 1, 1)

data = []

for i in range(NUM_ROWS):

    lat, lon = random.choice(locations)
    date = start_date + timedelta(days=random.randint(0, 365))

    # -----------------------
    # TIME FEATURES
    # -----------------------
    month = date.month
    day_of_year = date.timetuple().tm_yday

    # -----------------------
    # SEASONAL EFFECTS
    # -----------------------
    season_factor = np.sin((2 * np.pi * day_of_year) / 365)

    # -----------------------
    # Vegetation
    # -----------------------
    ndvi = np.clip(0.5 + 0.2 * season_factor + np.random.normal(0, 0.1), 0, 1)
    ndwi = np.clip(0.3 + 0.2 * season_factor + np.random.normal(0, 0.1), 0, 1)
    ndbi = np.clip(0.4 - 0.1 * season_factor + np.random.normal(0, 0.1), 0, 1)
    nbr = np.clip(np.random.normal(0.2, 0.1), 0, 1)

    # -----------------------
    # Pollution (higher in winter)
    # -----------------------
    pollution_boost = 1 - season_factor

    no2 = np.clip(0.03 + 0.02 * pollution_boost + np.random.normal(0, 0.01), 0, 0.1)
    so2 = np.clip(0.02 + 0.01 * pollution_boost, 0, 0.08)
    co = np.clip(0.5 + 0.3 * pollution_boost, 0, 2)
    o3 = np.clip(0.04 + 0.02 * season_factor, 0, 0.1)

    # -----------------------
    # Weather
    # -----------------------
    temperature = 25 + 10 * season_factor + np.random.uniform(-5, 5)
    dewpoint = temperature - np.random.uniform(2, 10)
    wind_speed = np.random.uniform(0.5, 8)

    # -----------------------
    # Rain (monsoon spike)
    # -----------------------
    rainfall = np.random.exponential(5 + 5 * max(season_factor, 0))

    # -----------------------
    # Surface Temp
    # -----------------------
    lst = temperature + np.random.uniform(0, 5)

    # -----------------------
    # DERIVED
    # -----------------------
    temp_diff = temperature - dewpoint
    pollution_index = no2 + so2 + co
    green_inverse = 1 - ndvi

    # -----------------------
    # TARGETS
    # -----------------------
    aqi = (
        0.4 * (no2 * 100) +
        0.3 * (so2 * 80) +
        0.2 * (co * 50) +
        0.1 * (o3 * 70)
    ) / (wind_speed + 0.5)

    heat_score = (
        0.5 * temperature +
        0.3 * lst +
        0.2 * (ndbi * 50)
    ) - (ndvi * 30)

    flood_score = (
        rainfall * 2 +
        ndwi * 50
    )

    veg_score = (
        ndvi * 100
    ) - (nbr * 20)

    # Clamp
    aqi = max(0, min(aqi, 500))
    heat_score = max(0, min(heat_score, 100))
    flood_score = max(0, min(flood_score, 100))
    veg_score = max(0, min(veg_score, 100))

    data.append([
        lat, lon, month, day_of_year,
        ndvi, ndwi, ndbi, nbr,
        no2, so2, co, o3,
        temperature, dewpoint, wind_speed,
        rainfall, lst,
        temp_diff, pollution_index, green_inverse,
        aqi, heat_score, flood_score, veg_score
    ])

columns = [
    "lat","lon","month","day_of_year",
    "ndvi","ndwi","ndbi","nbr",
    "no2","so2","co","o3",
    "temperature","dewpoint","wind_speed",
    "rainfall","lst",
    "temp_diff","pollution_index","green_inverse",
    "aqi","heat_score","flood_score","veg_score"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("final_environment_dataset.csv", index=False)

print("✅ XGBoost-ready dataset created:", df.shape)
df.to_csv("final_environment_dataset.csv", index=False)