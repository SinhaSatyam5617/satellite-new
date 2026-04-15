# --------------------------------------------------
# PATH FIX
# --------------------------------------------------
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------
from datetime import datetime, timedelta
import pandas as pd

from engine.data.gee_init import init_gee
from engine.data.sentinel2 import get_sentinel2_data
from engine.data.sentinel5p import get_pollution_data
from engine.data.era5 import get_weather_data
from engine.data.chirps import get_rainfall_data
from engine.data.landsat import get_lst_data

# --------------------------------------------------
# INIT GEE
# --------------------------------------------------
init_gee()

# --------------------------------------------------
# LOCATIONS (15)
# --------------------------------------------------
LOCATIONS = [
    (28.61, 77.20), (19.07, 72.87), (13.08, 80.27),
    (22.57, 88.36), (26.85, 80.95), (23.02, 72.57),
    (17.38, 78.48), (12.97, 77.59), (18.52, 73.85),
    (21.17, 72.83), (26.91, 75.78), (30.73, 76.77),
    (25.61, 85.14), (11.01, 76.96), (9.93, 76.26),
]

# --------------------------------------------------
# DATE RANGES
# --------------------------------------------------
DATE_RANGES = [
    (datetime(2023, 1, 1), datetime(2023, 1, 31)),
    (datetime(2023, 8, 1), datetime(2023, 9, 30)),
    (datetime(2023, 11, 1), datetime(2023, 12, 31)),
]

# --------------------------------------------------
# GENERATE DATASET
# --------------------------------------------------
def generate_dataset():

    rows = []

    for start_date, end_date in DATE_RANGES:

        current = start_date

        while current <= end_date:

            for lat, lon in LOCATIONS:

                print(f"📡 {lat},{lon} | {current}")

                try:
                    # -----------------------------
                    # REAL DATA CALLS
                    # -----------------------------
                    s2 = get_sentinel2_data(lat, lon, current)
                    p = get_pollution_data(lat, lon, current)
                    w = get_weather_data(lat, lon, current)
                    rain = get_rainfall_data(lat, lon, current)
                    lst = get_lst_data(lat, lon, current)

                    if s2 is None or w is None:
                        print("⚠️ Missing core data, skipping")
                        continue

                    # -----------------------------
                    # EXTRACT
                    # -----------------------------
                    ndvi = s2.get("ndvi")
                    ndwi = s2.get("ndwi")
                    ndbi = s2.get("ndbi")
                    nbr = s2.get("nbr")

                    no2 = p.get("no2") if p else None
                    so2 = p.get("so2") if p else None
                    co = p.get("co") if p else None
                    o3 = p.get("o3") if p else None

                    temp = w.get("temperature")
                    dew = w.get("dewpoint")
                    wind = w.get("wind_speed")

                    # -----------------------------
                    # DERIVED
                    # -----------------------------
                    temp_diff = (temp - dew) if temp and dew else None
                    pollution_index = (no2 or 0) + (so2 or 0) + (co or 0)
                    green_inverse = (1 - ndvi) if ndvi else None

                    # -----------------------------
                    # TARGETS
                    # -----------------------------
                    aqi = min(
                        0.5 * (no2 or 0) +
                        0.2 * (so2 or 0) +
                        0.2 * ((co or 0) * 50) +
                        0.1 * (o3 or 0),
                        500
                    )

                    heat_score = (
                        (temp or 0) * 1.5 +
                        (dew or 0) * 0.5 -
                        (wind or 0) * 2
                    )
                    heat_score = max(0, min(heat_score, 100))

                    flood_score = min((rain or 0) * 2, 100)
                    veg_score = (ndvi * 100) if ndvi else None

                    # -----------------------------
                    # FINAL ROW
                    # -----------------------------
                    row = {
                        "date": current.strftime("%Y-%m-%d"),
                        "lat": lat,
                        "lon": lon,

                        "ndvi": ndvi,
                        "ndwi": ndwi,
                        "ndbi": ndbi,
                        "nbr": nbr,

                        "no2": no2,
                        "so2": so2,
                        "co": co,
                        "o3": o3,

                        "temperature": temp,
                        "dewpoint": dew,
                        "wind_speed": wind,

                        "rainfall": rain,
                        "lst": lst,

                        "temp_diff": temp_diff,
                        "pollution_index": pollution_index,
                        "green_inverse": green_inverse,

                        "aqi": aqi,
                        "heat_score": heat_score,
                        "flood_score": flood_score,
                        "veg_score": veg_score
                    }

                    rows.append(row)

                except Exception as e:
                    print("❌ ERROR:", e)

            # 🔥 STEP SIZE (→ ~1000 rows)
            current += timedelta(days=2)

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------
    df = pd.DataFrame(rows)

    os.makedirs("dataset", exist_ok=True)

    path = "dataset/final_dataset_real_1000.csv"
    df.to_csv(path, index=False)

    print("\n✅ DONE")
    print("Rows:", len(df))


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    generate_dataset()