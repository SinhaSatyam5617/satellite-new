import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
from datetime import datetime
import requests
import math

st.set_page_config(layout="wide")
st.title("🗺️ Advanced Geo Selector (All Shapes)")

# ----------------------------------
# 🗺️ MAP
# ----------------------------------
m = folium.Map(location=[26.85, 80.95], zoom_start=6)

draw = Draw(
    export=True,
    draw_options={
        "polyline": False,
        "polygon": True,
        "rectangle": True,
        "circle": True,
        "marker": False,
        "circlemarker": False,
    }
)
draw.add_to(m)

map_data = st_folium(m, height=500, width=900)

# ----------------------------------
# 🛠️ HELPER: Circle → Polygon
# ----------------------------------
def circle_to_polygon(lat, lon, radius_m, points=36):
    coords = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        dx = radius_m * math.cos(angle)
        dy = radius_m * math.sin(angle)

        new_lat = lat + (dy / 111320)
        new_lon = lon + (dx / (111320 * math.cos(math.radians(lat))))

        coords.append([new_lon, new_lat])

    return coords

# ----------------------------------
# 📍 PROCESS DRAWING
# ----------------------------------
if map_data and map_data.get("all_drawings"):

    drawing = map_data["all_drawings"][-1]
    geom_type = drawing["geometry"]["type"]

    st.success(f"✅ Shape Selected: {geom_type}")

    # ----------------------------------
    # 🔺 POLYGON / RECTANGLE
    # ----------------------------------
    if geom_type == "Polygon":

        coords = drawing["geometry"]["coordinates"][0]

    # ----------------------------------
    # 🔵 CIRCLE
    # ----------------------------------
    elif geom_type == "Point" and "radius" in drawing["properties"]:

        center = drawing["geometry"]["coordinates"]
        radius = drawing["properties"]["radius"]

        lon, lat = center
        coords = circle_to_polygon(lat, lon, radius)

        st.info(f"Circle radius: {radius:.2f} meters")

    else:
        st.warning("Unsupported shape")
        st.stop()

    # ----------------------------------
    # 📐 SHOW COORDINATES
    # ----------------------------------
    st.subheader("📐 Coordinates")

    formatted = [[c[1], c[0]] for c in coords]
    st.write(formatted)

    # ----------------------------------
    # 🌍 LOCATION DETECTION
    # ----------------------------------
    center_lat = sum([c[1] for c in coords]) / len(coords)
    center_lon = sum([c[0] for c in coords]) / len(coords)

    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={center_lat}&lon={center_lon}&format=json"
        res = requests.get(url, headers={"User-Agent": "geo-app"})
        data = res.json()

        addr = data.get("address", {})

        city = addr.get("city") or addr.get("town") or addr.get("village")
        state = addr.get("state")
        country = addr.get("country")

        st.subheader("🌍 Location Info")
        st.write(f"City: {city}")
        st.write(f"State: {state}")
        st.write(f"Country: {country}")

    except:
        st.warning("Location fetch failed")

    # ----------------------------------
    # ⏱️ TIME
    # ----------------------------------
    st.subheader("⏱️ Time")
    st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # ----------------------------------
    # 🚀 GEE READY
    # ----------------------------------
    st.subheader("🧠 GEE Geometry")

    gee_geom = [[coord for coord in coords]]
    st.code(f"{gee_geom}")