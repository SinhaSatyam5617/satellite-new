import requests
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time

# -----------------------------
# CONFIG
# -----------------------------
NUM_ROWS = 300   # real rows (keep small due to API)
OUTPUT_FILE = "real_partial_dataset.csv"

locations = [
    (28.61, 77.20),  # Delhi
    (26.85, 80.95),  # Lucknow
    (19.07, 72.87),  # Mumbai
    (13.08, 80.27),  # Chennai
]

start_date = datetime(2023, 1, 1)

data = []

# -----------------------------
# FETCH WEATHER FROM API
# -----------------------------
def fetch_weather(lat, lon, date):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max,precipitation_sum&timezone=auto"
    
    try:
        res = requests.get(url)
        js = res.json()

        temp_max = js["daily"]["temperature_2m_max"][0]
        temp_min = js["daily"]["temperature_2m_min"][0]
        wind = js["daily"]["windspeed_10m_max"][0]
        rain = js["daily"]["precipitation_sum"][0]

        temperature = (temp_max + temp_min) / 2
        dewpoint = temperature - np.random.uniform(2, 6)

        return temperature, dewpoint, wind, rain

    except:
        return None

# -----------------------------
# MAIN LOOP
# -----------------------------
for i in range(NUM_ROWS):

    lat, lon = random.choice(locations)
    date_obj = start_date + timedelta(days=random.randint(0, 365))
    date = date_obj.strftime("%Y-%m-%d")

    result = fetch_weather(lat, lon, date)

    if result is None:
        continue

    temperature, dewpoint, wind_speed, rainfall = result

    # -----------------------------
    # PLACEHOLDER (SATELLITE LATER)
    # -----------------------------
    ndvi = np.random.uniform(0.2, 0.8)
    ndwi = np.random.uniform(0.1, 0.6)
    ndbi = np.random.uniform(0.2, 0.7)
    nbr = np.random.uniform(0.1, 0.4)

    # -----------------------------
    # PLACEHOLDER (CPCB LATER)
    # -----------------------------
    no2 = np.random.uniform(0.01, 0.08)
    so2 = np.random.uniform(0.01, 0.05)
    co = np.random.uniform(0.3, 1.2)
    o3 = np.random.uniform(0.02, 0.07)

    # -----------------------------
    # TIME FEATURES
    # -----------------------------
    day_of_year = date_obj.timetuple().tm_yday
    month = date_obj.month

    # -----------------------------
    # SURFACE TEMP
    # -----------------------------
    lst = temperature + np.random.uniform(0, 3)

    # -----------------------------
    # DERIVED
    # -----------------------------
    temp_diff = temperature - dewpoint
    pollution_index = no2 + so2 + co
    green_inverse = 1 - ndvi

    # -----------------------------
    # TARGETS (TEMPORARY)
    # -----------------------------
    aqi = (
        0.4 * (no2 * 100) +
        0.3 * (so2 * 80) +
        0.2 * (co * 50)
    ) / (wind_speed + 0.5)

    heat_score = (
        0.5 * temperature +
        0.3 * lst +
        0.2 * (ndbi * 50)
    ) - (ndvi * 30)

    flood_score = rainfall * 2 + ndwi * 50
    veg_score = ndvi * 100 - nbr * 20

    # -----------------------------
    # ADD ROW
    # -----------------------------
    data.append([
        lat, lon, month, day_of_year,
        ndvi, ndwi, ndbi, nbr,
        no2, so2, co, o3,
        temperature, dewpoint, wind_speed,
        rainfall, lst,
        temp_diff, pollution_index, green_inverse,
        aqi, heat_score, flood_score, veg_score
    ])

    print(f"✅ Row {i+1} collected")

    time.sleep(1)  # avoid API overload

# -----------------------------
# SAVE DATASET
# -----------------------------
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
df.to_csv(OUTPUT_FILE, index=False)

print("🎯 Real partial dataset saved:", OUTPUT_FILE)
print("Shape:", df.shape)