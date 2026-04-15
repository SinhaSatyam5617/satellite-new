import ee
from datetime import timedelta


# ----------------------------------
# 🌧 EXTRACT CHIRPS
# ----------------------------------
def extract_chirps_features(lat, lon, start_date, end_date):

    geometry = ee.Geometry.Point([lon, lat])

    collection = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterBounds(geometry)
        .filterDate(start_date, end_date)
    )

    # 🚨 CHECK COLLECTION SIZE
    size = collection.size().getInfo()
    if size == 0:
        raise Exception("❌ No CHIRPS data in date range")

    rainfall = collection.sum().rename("rainfall")

    stats = rainfall.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(5000),
        scale=5000,
        maxPixels=1e9
    ).getInfo()

    # 🚨 STRICT VALIDATION
    value = stats.get("rainfall") if stats else None

    if value is None:
        raise Exception("❌ Rainfall value missing")

    return {"rainfall": float(value)}


# ----------------------------------
# 🎯 MAIN FUNCTION
# ----------------------------------
def get_rainfall_data(lat, lon, date):

    start_date = date.strftime("%Y-%m-%d")

    # small extension (daily dataset)
    end_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    result = extract_chirps_features(lat, lon, start_date, end_date)

    print("🌧 REAL CHIRPS OK")

    return result["rainfall"]