import sys, os

# -----------------------------
# FIX PATH
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
from datetime import timedelta

from engine.data.sentinel2 import get_sentinel2_data
from engine.data.sentinel5p import get_pollution_data
from engine.data.era5 import get_weather_data
from engine.data.chirps import get_rainfall_data
from engine.data.landsat import get_lst_data


def build_feature_row_range(lat, lon, start_date, end_date):

    collected = []

    def safe(func, d):
        try:
            return func(lat, lon, d)
        except:
            return None

    current = start_date

    # -----------------------------
    # LOOP THROUGH DATE RANGE
    # -----------------------------
    while current <= end_date:

        s2 = safe(get_sentinel2_data, current)
        p  = safe(get_pollution_data, current)
        w  = safe(get_weather_data, current)
        r  = safe(get_rainfall_data, current)
        lst = safe(get_lst_data, current)

        collected.append({
            "ndvi": s2.get("ndvi") if s2 else None,
            "ndwi": s2.get("ndwi") if s2 else None,
            "ndbi": s2.get("ndbi") if s2 else None,
            "nbr": s2.get("nbr") if s2 else None,

            "no2": p.get("no2") if p else None,

            "temperature": w.get("temperature") if w else None,
            "dewpoint": w.get("dewpoint") if w else None,
            "wind_speed": w.get("wind_speed") if w else None,

            "rainfall": r if r else None,
            "lst": lst if lst else None
        })

        current += timedelta(days=1)

    # -----------------------------
    # AGGREGATION (IGNORE NONE/0)
    # -----------------------------
    aggregated = {}

    keys = collected[0].keys()

    for key in keys:

        values = [d[key] for d in collected if d[key] not in [None, 0]]

        if len(values) == 0:
            aggregated[key] = None
            continue

        if key == "rainfall":
            aggregated[key] = sum(values)  # 🔥 important
        else:
            aggregated[key] = sum(values) / len(values)

    # -----------------------------
    # SAFE FALLBACKS
    # -----------------------------
    aggregated["ndvi"] = aggregated["ndvi"] if aggregated["ndvi"] else 0.3
    aggregated["temperature"] = aggregated["temperature"] if aggregated["temperature"] else 30
    aggregated["dewpoint"] = aggregated["dewpoint"] if aggregated["dewpoint"] else 25
    aggregated["wind_speed"] = aggregated["wind_speed"] if aggregated["wind_speed"] else 2
    aggregated["lst"] = aggregated["lst"] if aggregated["lst"] else 30
    aggregated["rainfall"] = aggregated["rainfall"] if aggregated["rainfall"] else 0
    aggregated["no2"] = aggregated["no2"] if aggregated["no2"] else 0

    # -----------------------------
    # DERIVED
    # -----------------------------
    temp_diff = aggregated["temperature"] - aggregated["dewpoint"]
    pollution_index = aggregated["no2"]
    green_inverse = 1 - aggregated["ndvi"]

    # -----------------------------
    # FEATURE VECTOR
    # -----------------------------
    features = [
        aggregated["ndvi"], aggregated["ndwi"] or 0, aggregated["ndbi"] or 0, aggregated["nbr"] or 0,
        aggregated["no2"], 0, 0, 0,
        aggregated["temperature"], aggregated["dewpoint"], aggregated["wind_speed"],
        aggregated["rainfall"],
        aggregated["lst"],
        temp_diff,
        pollution_index,
        green_inverse
    ]

    return features, aggregated