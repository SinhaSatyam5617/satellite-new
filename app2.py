import streamlit as st
import ee
import geemap
from datetime import date

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Satellite Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("🌍 Satellite Environment Dashboard")

# -----------------------------
# Initialize GEE
# -----------------------------
credentials = ee.ServiceAccountCredentials(
    st.secrets["gee"]["service_account"],
    key_data=st.secrets["gee"]["private_key"]
)
ee.Initialize(credentials)

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Controls")

lat = st.sidebar.number_input("Latitude", value=13.0827)
lon = st.sidebar.number_input("Longitude", value=80.2707)

start_date = st.sidebar.date_input("Start Date", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date(2023, 1, 31))

# Convert to string for GEE
start = start_date.strftime("%Y-%m-%d")
end = end_date.strftime("%Y-%m-%d")

# -----------------------------
# Geometry
# -----------------------------
point = ee.Geometry.Point([lon, lat])

# -----------------------------
# Load Satellite Data
# -----------------------------
collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(point) \
    .filterDate(start, end)

image = collection.median()

# -----------------------------
# NDVI Calculation
# -----------------------------
ndvi = image.normalizedDifference(['B8', 'B4'])

# -----------------------------
# Map
# -----------------------------
Map = geemap.Map(center=[lat, lon], zoom=10)

Map.addLayer(ndvi, {"min": 0, "max": 1, "palette": ["blue", "white", "green"]}, "NDVI")

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.write("### NDVI Map")
    st.write(Map)

with col2:
    st.write("### Info")
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {lon}")
    st.write(f"Start Date: {start}")
    st.write(f"End Date: {end}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("Built with Google Earth Engine + Streamlit")