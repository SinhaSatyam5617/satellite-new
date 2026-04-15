import ee
from engine.georisk_ai.gee import init_gee


# ======================
# SHARED COLLECTION BUILDER
# ======================
def build_collection(region):

    init_gee()   # 🔥 MOVE INIT HERE (SAFE)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filterDate("2022-01-01", "2023-12-31")
        .filter(ee.Filter.notNull(['system:time_start']))
        .select(['B3', 'B4', 'B8', 'B11'])
        .limit(25)
    )

    def add_ndvi(img):
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return img.addBands(ndvi)

    return collection.map(add_ndvi)


# ======================
# GET TIME SERIES
# ======================
def get_ndvi_timeseries_images(geometry):

    init_gee()   # 🔥 SAFE INIT

    region = ee.Geometry.Polygon(geometry)

    collection = build_collection(region)

    images = collection.toList(collection.size())
    size = images.size().getInfo()

    result = []

    for i in range(size):
        try:
            img = ee.Image(images.get(i))

            date = ee.Date(
                img.get('system:time_start')
            ).format("YYYY-MM-dd").getInfo()

            result.append({
                "index": i,
                "date": date
            })
        except:
            break

    return result


# ======================
# GET IMAGE BY INDEX
# ======================
def get_image_by_index(geometry, index):

    init_gee()   # 🔥 SAFE INIT

    region = ee.Geometry.Polygon(geometry)

    collection = build_collection(region)

    images = collection.toList(collection.size())

    try:
        return ee.Image(images.get(index))
    except:
        return None
