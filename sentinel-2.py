import ee
import requests
from PIL import Image
from io import BytesIO

# -------------------------
# INIT EARTH ENGINE
# -------------------------
try:
    ee.Initialize(project='satellite-new-489422')
except Exception:
    ee.Authenticate()
    ee.Initialize(project='satellite-new-489422')

# -------------------------
# INPUT LOCATION
# -------------------------
lat, lon = 26.8467, 80.9462  # change this

point = ee.Geometry.Point([lon, lat])

# -------------------------
# AREA CONTROL
# -------------------------
buffer_meters = 150   # 🔥 best balance (100–200)

region = point.buffer(buffer_meters).bounds()

# -------------------------
# FETCH SENTINEL-2
# -------------------------
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR")
    .filterBounds(point)
    .filterDate("2022-01-01", "2023-12-31")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 15))  # 🔥 stricter cloud filter
)

# -------------------------
# CHECK DATA
# -------------------------
count = collection.size().getInfo()
print("📡 Images found:", count)

if count == 0:
    print("❌ No images found. Try different date/location.")
    exit()

# -------------------------
# 🔥 SELECT BANDS (CRITICAL FIX)
# -------------------------
collection = collection.select(["B4", "B3", "B2"])

# -------------------------
# MEDIAN IMAGE
# -------------------------
image = collection.median()

# -------------------------
# VISUALIZATION (IMPORTANT)
# -------------------------
rgb = image.visualize(
    min=0,
    max=3000,
    gamma=1.2
)

# -------------------------
# GET IMAGE URL
# -------------------------
url = rgb.getThumbURL({
    "region": region,
    "dimensions": 512,
    "format": "png"
})

print("🌐 URL:", url)

# -------------------------
# DOWNLOAD IMAGE
# -------------------------
response = requests.get(url)

print("📥 Status:", response.status_code)

if response.status_code == 200:
    try:
        img = Image.open(BytesIO(response.content))

        # -------------------------
        # SAVE
        # -------------------------
        file_name = "sentinel_image.png"
        img.save(file_name)

        print(f"✅ Saved as {file_name}")

        # -------------------------
        # DISPLAY
        # -------------------------
        img.show()

    except Exception as e:
        print("❌ Not an image:", e)

else:
    print("❌ Failed:")
    print(response.text)