import ee

# -------------------------
# INIT
# -------------------------
ee.Initialize(project='satellite-new-489422')

def process_region(geometry):

    region = ee.Geometry(geometry)

    # -------------------------
    # DATE
    # -------------------------
    start = ee.Date("2025-12-01")
    end = ee.Date("2025-12-31")

    # -------------------------
    # LOAD COLLECTION
    # -------------------------
    collection = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterBounds(region) \
        .filterDate(start, end)

    # -------------------------
    # 🔥 SCL MASK (PER IMAGE)
    # -------------------------
    def mask_s2(image):
        scl = image.select("SCL")

        mask = (
            scl.neq(3)   # shadow
            .And(scl.neq(8))   # cloud medium
            .And(scl.neq(9))   # cloud high
            .And(scl.neq(10))  # cirrus
        )

        return image.updateMask(mask)

    collection = collection.map(mask_s2)

    # -------------------------
    # COMPOSITE
    # -------------------------
    image = collection.median().clip(region)

    # -------------------------
    # SELECT BANDS
    # -------------------------
    image = image.select(["B2", "B3", "B4", "B8", "B11"])

    # -------------------------
    # INDICES
    # -------------------------
    ndvi = image.normalizedDifference(["B8", "B4"])
    ndwi = image.normalizedDifference(["B3", "B8"])
    ndbi = image.normalizedDifference(["B11", "B8"])

    # -------------------------
    # RAW MASKS
    # -------------------------
    water_raw = ndwi.gt(0.15).And(ndvi.lt(0.2))
    vegetation_raw = ndvi.gt(0.25)
    urban_raw = ndbi.gt(0.2).And(ndvi.lt(0.3))

    # -------------------------
    # 🔥 CLEAN MASKS (IMPORTANT)
    # -------------------------
    def clean(mask):
        return mask.focal_mode(1).focal_max(1).focal_min(1)

    water = clean(water_raw)
    vegetation = clean(vegetation_raw)
    urban = clean(urban_raw)

    # -------------------------
    # PRIORITY LOGIC
    # -------------------------
    vegetation = vegetation.And(water.Not())
    urban = urban.And(water.Not()).And(vegetation.Not())

    # -------------------------
    # FINAL CLASS IMAGE
    # -------------------------
    classified = (
        water.multiply(1)
        .add(vegetation.multiply(2))
        .add(urban.multiply(3))
    )

    # -------------------------
    # 🔥 AREA CALCULATION (FINAL SAFE)
    # -------------------------
    pixel_area = ee.Image.pixelArea().rename("area")

    def compute_area(mask):
        area_img = pixel_area.updateMask(mask)

        area = area_img.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=region,
            scale=20,          # consistent resolution
            maxPixels=1e13,
            tileScale=2
        )

        return ee.Number(area.get("area"))

    water_area = compute_area(water)
    veg_area = compute_area(vegetation)
    urban_area = compute_area(urban)

    total_area = region.area()

    stats = ee.Dictionary({
        "water": water_area,
        "vegetation": veg_area,
        "urban": urban_area,
        "total": total_area
    }).getInfo()

    return classified, stats