import ee
from datetime import timedelta


def mask_s2_clouds(image):
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1 << 10).eq(0).And(
        qa.bitwiseAnd(1 << 11).eq(0)
    )
    return image.updateMask(mask).divide(10000)


def get_sentinel2_data(lat, lon, date):

    geometry = ee.Geometry.Point([lon, lat])

    start = date.strftime("%Y-%m-%d")
    end = (date + timedelta(days=3)).strftime("%Y-%m-%d")

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(geometry)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60))
        .map(mask_s2_clouds)
    )

    # 🚨 CHECK IF COLLECTION HAS DATA
    size = collection.size().getInfo()
    if size == 0:
        raise Exception("❌ No Sentinel-2 images in date range")

    image = collection.median()

    ndvi = image.normalizedDifference(['B8', 'B4']).rename('ndvi')
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('ndwi')
    ndbi = image.normalizedDifference(['B11', 'B8']).rename('ndbi')
    nbr  = image.normalizedDifference(['B8', 'B12']).rename('nbr')

    stats = image.addBands([ndvi, ndwi, ndbi, nbr]).reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(5000),
        scale=10,
        maxPixels=1e9
    ).getInfo()

    # 🚨 STRICT VALIDATION (ALL FEATURES)
    required = ["ndvi", "ndwi", "ndbi", "nbr"]

    if stats is None or any(stats.get(k) is None for k in required):
        raise Exception("❌ Sentinel-2 incomplete data")

    print("🌱 REAL Sentinel-2 OK")

    return {
        "ndvi": float(stats["ndvi"]),
        "ndwi": float(stats["ndwi"]),
        "ndbi": float(stats["ndbi"]),
        "nbr": float(stats["nbr"])
    }