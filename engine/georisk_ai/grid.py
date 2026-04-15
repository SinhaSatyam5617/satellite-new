import ee
from engine.georisk_ai.gee import init_gee

# ✅ Initialize GEE once
init_gee()


def sample_ndvi_from_image(image, geometry):
    region = ee.Geometry.Polygon(geometry)

    # Generate random sample points
    points = ee.FeatureCollection.randomPoints(
        region=region,
        points=250
    )

    # Sample NDVI values
    sampled = image.sampleRegions(
        collection=points,
        scale=30,
        geometries=True
    )

    data = sampled.getInfo()

    result = []

    for f in data["features"]:
        coords = f["geometry"]["coordinates"]
        value = f["properties"].get("NDVI")

        if value is not None:
            result.append({
                "lon": coords[0],
                "lat": coords[1],
                "value": float(value)
            })

    return result