import ee
import numpy as np
import requests
from PIL import Image
from io import BytesIO

# ✅ INIT WITH PROJECT
ee.Initialize(project="satellite-new-489422")

PATCH_SIZE = 64

# -----------------------------
# GET RGB IMAGE
# -----------------------------
def get_rgb(image, region):
    try:
        image = image.select(['B4', 'B3', 'B2'])

        url = image.getThumbURL({
            'region': region,
            'dimensions': PATCH_SIZE,
            'format': 'png',
            'min': 0,
            'max': 3000
        })

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        img = Image.open(BytesIO(response.content)).convert("RGB")
        return np.array(img) / 255.0

    except Exception as e:
        print("RGB error:", e)
        return None


# -----------------------------
# GET MASK (NDVI)
# -----------------------------
def get_mask(image, region):
    try:
        ndvi = image.normalizedDifference(['B8', 'B4'])

        url = ndvi.getThumbURL({
            'region': region,
            'dimensions': PATCH_SIZE,
            'format': 'png',
            'min': 0,
            'max': 1
        })

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        img = Image.open(BytesIO(response.content)).convert("L")
        ndvi_np = np.array(img) / 255.0

        return (ndvi_np > 0.3).astype(np.float32)

    except Exception as e:
        print("Mask error:", e)
        return None


# -----------------------------
# GENERATE DATASET
# -----------------------------
def generate_dataset(num_samples=100):
    X = []
    y = []

    coords = [
        (13.08, 80.27),   # Chennai
        (28.61, 77.20),   # Delhi
        (19.07, 72.87),   # Mumbai
        (22.57, 88.36),   # Kolkata
        (26.85, 80.95)    # Lucknow
    ]

    for i in range(num_samples):
        lat, lon = coords[i % len(coords)]

        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(200 + (i % 10) * 20).bounds().getInfo()['coordinates']

        collection = ee.ImageCollection('COPERNICUS/S2') \
            .filterBounds(point) \
            .filterDate('2023-01-01', '2023-12-31')

        image = collection.median()

        rgb = get_rgb(image, region)
        mask = get_mask(image, region)

        # ✅ SKIP BAD DATA
        if rgb is None or mask is None:
            print("⚠️ Skipping bad sample")
            continue

        X.append(rgb)
        y.append(mask)

        print(f"Sample {len(X)}/{num_samples}")

    return np.array(X), np.array(y)