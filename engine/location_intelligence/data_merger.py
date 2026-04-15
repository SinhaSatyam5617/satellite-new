import sys
import os
from datetime import datetime, timedelta

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# ----------------------------------
# IMPORT YOUR REAL FUNCTIONS
# ----------------------------------
from engine.data.sentinel2 import extract_sentinel2_features
from engine.data.sentinel5p import extract_pollution_features
from engine.data.era5 import extract_era5_features
from engine.data.chirps import extract_chirps_features
from engine.data.landsat import extract_landsat_features


# ----------------------------------
# SAFE GET
# ----------------------------------
def safe_get(d, key, default=0):
    try:
        return d.get(key, default)
    except:
        return default


# ----------------------------------
# DATE HANDLER (important)
# ----------------------------------
def get_date_range(date):
    date_obj = datetime.strptime(str(date), "%Y-%m-%d")

    start_date = str(date_obj - timedelta(days=2))
    end_date = str(date_obj)

    return start_date, end_date


# ----------------------------------
# MAIN FUNCTION
# ----------------------------------
def get_location_features(lat, lon, date):

    try:
        start_date, end_date = get_date_range(date)

        # -------------------------
        # FETCH ALL DATA
        # -------------------------
        s2 = extract_sentinel2_features(lat, lon, start_date, end_date)
        s5p = extract_pollution_features(lat, lon, start_date, end_date)
        era5 = extract_era5_features(lat, lon, start_date, end_date)
        chirps = extract_chirps_features(lat, lon, start_date, end_date)
        landsat = extract_landsat_features(lat, lon, start_date, end_date)

        # -------------------------
        # MERGE + STANDARDIZE
        # -------------------------
        features = {

            # 🌱 Sentinel-2
            "ndvi": safe_get(s2, "NDVI"),
            "ndwi": safe_get(s2, "NDWI"),
            "ndbi": safe_get(s2, "NDBI"),
            "nbr": safe_get(s2, "NBR"),

            # 🏭 Sentinel-5P
            "no2": safe_get(s5p, "NO2"),
            "so2": safe_get(s5p, "SO2"),
            "co": safe_get(s5p, "CO"),

            # 🌦 ERA5
            "temperature": safe_get(era5, "Temperature"),
            "dewpoint": safe_get(era5, "Dewpoint"),

            # 🌧 CHIRPS
            "rainfall": safe_get(chirps, "Rainfall"),

            # 🌡 Landsat
            "lst_ndvi": safe_get(landsat, "NDVI"),  # Landsat NDVI proxy
        }

        return features

    except Exception as e:
        return {
            "error": str(e)
        }