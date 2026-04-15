import ee
from datetime import timedelta


# ----------------------------------
# 🌡 EXTRACT LST
# ----------------------------------
def extract_landsat_lst(lat, lon, start_date, end_date):

    geometry = ee.Geometry.Point([lon, lat])

    collection = (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(geometry)
        .filterDate(start_date, end_date)
    )

    # 🚨 CHECK IF DATA EXISTS
    size = collection.size().getInfo()
    if size == 0:
        raise Exception("❌ No Landsat images in date range")

    image = collection.median()

    # 🚨 CHECK BAND EXISTS
    band_names = image.bandNames().getInfo()
    if "ST_B10" not in band_names:
        raise Exception("❌ ST_B10 band missing")

    # -----------------------------
    # LST CALCULATION
    # -----------------------------
    lst = image.select("ST_B10") \
        .multiply(0.00341802) \
        .add(149.0) \
        .subtract(273.15) \
        .rename("lst")

    stats = lst.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(5000),
        scale=30,
        maxPixels=1e9
    ).getInfo()

    # 🚨 STRICT VALIDATION
    if stats is None or stats.get("lst") is None:
        raise Exception("❌ No LST value extracted")

    return stats


# ----------------------------------
# 🎯 MAIN FUNCTION
# ----------------------------------
def get_lst_data(lat, lon, date):

    start_date = date.strftime("%Y-%m-%d")

    # 🔥 Landsat revisit is ~16 days → extend window
    end_date = (date + timedelta(days=10)).strftime("%Y-%m-%d")

    result = extract_landsat_lst(lat, lon, start_date, end_date)

    print("🌡 REAL LST OK")

    return float(result["lst"])