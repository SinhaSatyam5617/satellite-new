import ee
from datetime import datetime, timedelta

# ----------------------------------
# 🌍 INIT (SAFE)
# ----------------------------------
def init_gee():
    try:
        ee.Initialize(project="satellite-new-489422")
    except:
        ee.Authenticate()
        ee.Initialize(project="satellite-new-489422")

init_gee()

# ----------------------------------
# 🛠 HELPERS
# ----------------------------------
def get_date_range(start_date=None, end_date=None, days=30):
    if start_date and end_date:
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    base = datetime.today()
    start = (base - timedelta(days=days)).strftime("%Y-%m-%d")
    end = base.strftime("%Y-%m-%d")

    return start, end


def safe(value, default):
    return default if value is None else value


def safe_reduce(image, band, geom, scale):
    try:
        stats = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geom,
            scale=scale,
            maxPixels=1e9,
            bestEffort=True
        )
        val = stats.get(band)
        return val.getInfo() if val else None
    except:
        return None

# ----------------------------------
# 🌱 NDVI
# ----------------------------------
def get_ndvi(geom, start, end, min_images=3):
    try:
        col = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(geom) \
            .filterDate(start, end)

        if col.size().getInfo() < min_images:
            return None

        img = col.median()
        ndvi = img.normalizedDifference(['B8', 'B4']).rename("ndvi")

        return safe_reduce(ndvi, "ndvi", geom, 10)

    except:
        return None

# ----------------------------------
# 🌧️ RAINFALL
# ----------------------------------
def get_rainfall(geom, start, end, min_days=5):
    try:
        col = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
            .filterBounds(geom) \
            .filterDate(start, end)

        if col.size().getInfo() < min_days:
            return None

        rain = col.sum()
        return safe_reduce(rain, "precipitation", geom, 5000)

    except:
        return None

# ----------------------------------
# 🌡️ TEMP + HUMIDITY (UPDATED 🔥)
# ----------------------------------
def get_temp_humidity(geom, start, end, min_days=5):
    try:
        col = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
            .filterBounds(geom) \
            .filterDate(start, end)

        if col.size().getInfo() < min_days:
            return None, None

        img = col.mean()

        temp = safe_reduce(img, "temperature_2m", geom, 10000)
        humidity = safe_reduce(img, "relative_humidity_2m", geom, 10000)

        if temp:
            temp -= 273.15

        return temp, humidity

    except:
        return None, None

# ----------------------------------
# 🌡️ LST
# ----------------------------------
def get_lst(geom, start, end, min_images=3):
    try:
        col = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
            .filterBounds(geom) \
            .filterDate(start, end)

        if col.size().getInfo() < min_images:
            return None

        img = col.median()

        lst = img.select("ST_B10") \
            .multiply(0.00341802) \
            .add(149.0) \
            .subtract(273.15) \
            .rename("lst")

        return safe_reduce(lst, "lst", geom, 30)

    except:
        return None

# ----------------------------------
# 🌫️ POLLUTION (FIXED)
# ----------------------------------
def get_pollution_all(geom, start, end, min_days=5):

    def fetch(collection_id, band, default):
        try:
            col = ee.ImageCollection(collection_id) \
                .filterBounds(geom) \
                .filterDate(start, end)

            if col.size().getInfo() < min_days:
                return default

            img = col.mean()

            val = safe_reduce(
                img.select(band),
                band,
                geom.buffer(10000),
                10000
            )

            return val if val is not None else default

        except:
            return default

    return {
        "no2": fetch("COPERNICUS/S5P/OFFL/L3_NO2",
                     "tropospheric_NO2_column_number_density", 0.0001),
        "co": fetch("COPERNICUS/S5P/OFFL/L3_CO",
                    "CO_column_number_density", 0.03),
        "o3": fetch("COPERNICUS/S5P/OFFL/L3_O3",
                    "O3_column_number_density", 0.1),
        "so2": fetch("COPERNICUS/S5P/OFFL/L3_SO2",
                     "SO2_column_number_density", 0.0002)
    }

# ----------------------------------
# 🚀 MAIN FUNCTION (UPDATED 🔥)
# ----------------------------------
def get_unified_features(lat, lon, start_date=None, end_date=None, days=30):

    start, end = get_date_range(start_date, end_date, days)

    geom = ee.Geometry.Point([lon, lat]).buffer(5000)

    ndvi = get_ndvi(geom, start, end)
    rainfall = get_rainfall(geom, start, end)
    temp, humidity = get_temp_humidity(geom, start, end)
    lst = get_lst(geom, start, end)
    pollution = get_pollution_all(geom, start, end)

    # 🔥 NEW: Heat Index + Anomaly
    heat_index = (temp + (0.33 * humidity) - 4) if temp and humidity else temp
    anomaly = (temp - 25) if temp else 0

    return {
        "ndvi": safe(ndvi, 0),
        "rainfall": safe(rainfall, 0),
        "temperature": safe(temp, 0),
        "humidity": safe(humidity, 50),
        "heat_index": safe(heat_index, 0),
        "anomaly": anomaly,
        "lst": safe(lst, 0),
        "pollution": pollution,
        "date_range": f"{start} to {end}"
    }