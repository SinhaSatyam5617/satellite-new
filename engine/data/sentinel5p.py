import ee
from datetime import timedelta


# --------------------------------------------------
# 🌍 REAL SENTINEL-5P DATA
# --------------------------------------------------
def get_pollution_data(lat, lon, date):

    geometry = ee.Geometry.Point([lon, lat])

    start = date.strftime("%Y-%m-%d")
    end = (date + timedelta(days=3)).strftime("%Y-%m-%d")

    # -----------------------------
    # NO2 COLLECTION
    # -----------------------------
    collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
        .filterBounds(geometry)
        .filterDate(start, end)
    )

    # 🚨 CHECK COLLECTION SIZE
    size = collection.size().getInfo()
    if size == 0:
        raise Exception("❌ No Sentinel-5P data in date range")

    image = collection.mean()

    band = "tropospheric_NO2_column_number_density"

    stats = image.select(band).reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(10000),
        scale=10000,
        maxPixels=1e9
    ).getInfo()

    # 🚨 STRICT VALIDATION
    value = stats.get(band) if stats else None

    if value is None:
        raise Exception("❌ NO2 value missing")

    print("🌍 REAL Sentinel-5P OK")

    return {
        "no2": float(value),
        "so2": None,   # extend later if needed
        "co": None,
        "o3": None
    }