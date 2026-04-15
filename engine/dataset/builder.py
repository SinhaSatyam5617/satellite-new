import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta

from engine.data.sentinel2 import extract_sentinel2_features
from engine.data.sentinel5p import extract_pollution_features
from engine.data.era5 import extract_era5_features
from engine.data.chirps import extract_chirps_features


def safe_get(data, key):
    return data.get(key) if data and data.get(key) is not None else 0


# ----------------------------------
# Build One Row (FIXED + ADVANCED)
# ----------------------------------
def build_feature_row(lat, lon, date):

    try:
        # ----------------------------------
        # Convert date → small window
        # ----------------------------------
        d = datetime.strptime(date, "%Y-%m-%d")

        start_date = (d - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date   = (d + timedelta(days=1)).strftime("%Y-%m-%d")

        # ----------------------------------
        # Fetch Data
        # ----------------------------------
        s2 = extract_sentinel2_features(lat, lon, start_date, end_date)
        p  = extract_pollution_features(lat, lon, start_date, end_date)
        w  = extract_era5_features(lat, lon, start_date, end_date)
        r  = extract_chirps_features(lat, lon, start_date, end_date)

        # Debug logs
        print("Date:", date)
        print("Sentinel-2:", s2)
        print("Pollution:", p)
        print("Weather:", w)
        print("Rainfall:", r)

        row = {}

        # -----------------------------
        # Sentinel-2
        # -----------------------------
        row["NDVI"] = safe_get(s2, "NDVI")
        row["NDWI"] = safe_get(s2, "NDWI")
        row["NDBI"] = safe_get(s2, "NDBI")
        row["NBR"]  = safe_get(s2, "NBR")

        # -----------------------------
        # Pollution
        # -----------------------------
        row["NO2"] = safe_get(p, "NO2")
        row["SO2"] = safe_get(p, "SO2")
        row["CO"]  = safe_get(p, "CO")
        row["O3"]  = safe_get(p, "O3")  # 🔥 NEW

        # -----------------------------
        # Weather
        # -----------------------------
        row["Temperature"] = safe_get(w, "Temperature")
        row["Dewpoint"]    = safe_get(w, "Dewpoint")

        # -----------------------------
        # Rainfall
        # -----------------------------
        row["Rainfall"] = safe_get(r, "Rainfall")

        # -----------------------------
        # OPTIONAL META FEATURES (🔥 improves model)
        # -----------------------------
        row["month"] = d.month
        row["day"]   = d.day

        # -----------------------------
        # VALIDATION
        # -----------------------------
        if row["CO"] == 0 and row["NO2"] == 0:
            return {"error": "No pollution data available"}

        return row

    except Exception as e:
        return {"error": str(e)}