import ee
from datetime import timedelta


# ----------------------------------
# 🌦 EXTRACT ERA5
# ----------------------------------
def extract_era5_features(lat, lon, start_date, end_date):

    geometry = ee.Geometry.Point([lon, lat])

    collection = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterBounds(geometry)
        .filterDate(start_date, end_date)
    )

    # 🚨 CHECK COLLECTION
    size = collection.size().getInfo()
    if size == 0:
        raise Exception("❌ No ERA5 data in date range")

    image = collection.mean()

    stats = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(10000),
        scale=10000,
        maxPixels=1e9
    ).getInfo()

    if stats is None:
        raise Exception("❌ ERA5 returned no data")

    return stats


# ----------------------------------
# 🎯 MAIN FUNCTION
# ----------------------------------
def get_weather_data(lat, lon, date):

    start_date = date.strftime("%Y-%m-%d")

    # ERA5 daily → small extension
    end_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    result = extract_era5_features(lat, lon, start_date, end_date)

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if (
        result.get("temperature_2m") is None or
        result.get("dewpoint_temperature_2m") is None
    ):
        raise Exception("❌ Missing ERA5 core values")

    # -----------------------------
    # CONVERT UNITS
    # -----------------------------
    temperature = result["temperature_2m"] - 273.15
    dewpoint = result["dewpoint_temperature_2m"] - 273.15

    # 🔥 REAL WIND SPEED (u + v)
    u = result.get("u_component_of_wind_10m", 0)
    v = result.get("v_component_of_wind_10m", 0)

    wind_speed = (u**2 + v**2) ** 0.5

    print("🌦 REAL ERA5 OK")

    return {
        "temperature": float(temperature),
        "dewpoint": float(dewpoint),
        "wind_speed": float(wind_speed)
    }