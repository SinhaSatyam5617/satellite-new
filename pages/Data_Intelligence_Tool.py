import streamlit as st
import ee
from datetime import date
import streamlit as st

def show():
    st.title("📊 Data Intelligence Tool")
# -----------------------------
# 🌍 INIT
# -----------------------------
try:
    ee.Initialize(project="satellite-new-489422")
except:
    ee.Authenticate()
    ee.Initialize(project="satellite-new-489422")

st.set_page_config(layout="wide")
st.title("Data Intelligence & Extraction Engine")

st.markdown("---")
st.markdown("""
This module extracts pixel-level data from multiple satellite datasets to generate a unified environmental profile for any location.  
It applies temporal aggregation and statistical reduction on optical, radar, climatic, and atmospheric variables.  
All outputs represent calibrated satellite-derived metrics over the selected region and time window.
""")

st.markdown("---")
# # =============================
# 📍 EXTRACTION TOOL + ENGINE
# =============================
st.markdown("---")
st.header("Live Data Extraction")

# -----------------------------
# INPUTS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    lat = st.number_input("Latitude", value=26.84)
with col2:
    lon = st.number_input("Longitude", value=81.00)
with col3:
    agg = st.selectbox("Aggregation", ["mean", "median", "max"])

col4, col5 = st.columns(2)

with col4:
    start_date = st.date_input("Start Date", date(2023, 1, 1))
with col5:
    end_date = st.date_input("End Date", date(2023, 2, 1))

# -----------------------------
# GEOMETRY + REDUCER
# -----------------------------
geom = ee.Geometry.Point([lon, lat]).buffer(5000)

def get_reducer():
    return {
        "mean": ee.Reducer.mean(),
        "median": ee.Reducer.median(),
        "max": ee.Reducer.max()
    }[agg]

reducer = get_reducer()

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("Extract Data", type="primary"):

    with st.spinner("Extracting multi-satellite intelligence..."):

        start = start_date.strftime("%Y-%m-%d")
        end   = end_date.strftime("%Y-%m-%d")

        # -----------------------------
        # Sentinel-2 (Bands)
        # -----------------------------
        try:
            s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                .filterBounds(geom).filterDate(start, end).median()

            s2_stats = s2.select(["B2","B3","B4","B8","B11","B12"]) \
                .reduceRegion(reducer=reducer, geometry=geom, scale=10, maxPixels=1e9) \
                .getInfo()
        except:
            s2_stats = {"error": "No Data"}

        # -----------------------------
        # CHIRPS (Rainfall)
        # -----------------------------
        try:
            chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
                .filterBounds(geom).filterDate(start, end).sum()

            rain_stats = chirps.reduceRegion(
                reducer=reducer,
                geometry=geom,
                scale=5000,
                maxPixels=1e9
            ).getInfo()
        except:
            rain_stats = {"error": "No Data"}

        # -----------------------------
        # ERA5 (Weather)
        # -----------------------------
        try:
            era5 = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
                .filterBounds(geom).filterDate(start, end).mean()

            era_stats = era5.reduceRegion(
                reducer=reducer,
                geometry=geom,
                scale=10000,
                maxPixels=1e9
            ).getInfo()
        except:
            era_stats = {"error": "No Data"}

        # -----------------------------
        # Sentinel-5P (Pollution)
        # -----------------------------
        try:
            s5p = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
                .filterBounds(geom).filterDate(start, end).mean()

            s5p_stats = s5p.reduceRegion(
                reducer=reducer,
                geometry=geom,
                scale=10000,
                maxPixels=1e9
            ).getInfo()
        except:
            s5p_stats = {"error": "No Data"}

        # =============================
        # 📊 RESULTS (2 PER ROW)
        # =============================
        st.markdown("---")
        st.subheader("Extracted Results")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Sentinel-2 Bands")
            st.code(str(s2_stats))

        with col2:
            st.markdown("### CHIRPS Rainfall")
            st.code(str(rain_stats))

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### ERA5 Weather")
            st.code(str(era_stats))

        with col4:
            st.markdown("### Sentinel-5P Pollution")
            st.code(str(s5p_stats))
# 🛰️ SECTION 2: CONSTELLATION
# =============================
st.markdown("---")
st.header("Virtual Constellation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Sentinel-2 (A/B/C)")
    st.caption("2015–Present | 10m | 5-day revisit")
    st.write("Optical multispectral imaging for vegetation, water, and land monitoring.")

with col2:
    st.markdown("### Landsat 8 / 9")
    st.caption("2013–Present | 30m | 16-day revisit")
    st.write("Long-term surface reflectance and thermal monitoring.")

with col3:
    st.markdown("### Sentinel-1 (SAR)")
    st.caption("2014–Present | Radar | All-weather")
    st.write("Microwave radar imaging for flood and structural detection.")

col4, col5 = st.columns(2)

with col4:
    st.markdown("### CHIRPS")
    st.caption("1981–Present | Rainfall")
    st.write("Satellite + station rainfall dataset.")

with col5:
    st.markdown("### ERA5 / Sentinel-5P")
    st.caption("Global Weather + Pollution")
    st.write("Atmospheric variables and air quality monitoring.")

    # =============================
# 📡 SECTION 3: DATASET DETAILS
# =============================
st.markdown("---")
st.header("Dataset Inventory")

st.markdown("""
**Sentinel-2 (Optical):**
- Provides multispectral reflectance data across 13 bands.
- Used for vegetation indices, water detection, and land classification.
- High spatial resolution (10m–60m).

**Landsat (Thermal + Optical):**
- Includes thermal infrared bands for temperature extraction.
- Useful for long-term climate and land surface monitoring.

**Sentinel-1 (Radar):**
- Uses microwave signals (VH, VV polarization).
- Penetrates clouds → critical for flood detection.

**CHIRPS (Rainfall):**
- Combines satellite + ground station rainfall.
- Daily precipitation estimates (mm/day).

**ERA5 (Weather):**
- Global reanalysis dataset.
- Includes temperature, wind, humidity.

**Sentinel-5P (Pollution):**
- Measures NO₂, CO, SO₂.
- Atmospheric column density.

**MODIS (Global Monitoring):**
- Daily low-resolution data.
- Used for large-scale environmental trends.
""")

# =============================
# 🌈 SECTION 4: BANDS USED
# =============================
st.markdown("---")
st.header("Bands & Variables Extracted")

st.code("""
Sentinel-2:
B2 (Blue), B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR1), B12 (SWIR2)

Landsat:
ST_B10 (Thermal band → LST)

Sentinel-1:
VH polarization (flood detection)

CHIRPS:
Precipitation (mm)

ERA5:
Temperature, Wind (u/v components)

Sentinel-5P:
NO₂ column density

MODIS:
NDVI (global vegetation)
""")

# =============================
# 🌈 SECTION 5: SPECTRAL MATRIX
# =============================
st.markdown("---")
st.header("Spectral Band Matrix")

band_matrix = """
Band      | Wavelength (μm) | Operational Use                | Interpretation
----------|------------------|--------------------------------|------------------------------
Blue      | 0.45 – 0.49      | Aerosol / haze detection       | High → atmospheric scattering
Green     | 0.53 – 0.57      | Vegetation reflectance         | High → healthy vegetation
Red       | 0.64 – 0.67      | Chlorophyll absorption         | Low → dense vegetation
NIR       | 0.84 – 0.88      | Biomass / vegetation health    | High → strong photosynthesis
SWIR1     | 1.57 – 1.65      | Moisture sensitivity           | High → dry soil
SWIR2     | 2.11 – 2.29      | Burn / urban detection         | High → burned or built-up
"""

st.code(band_matrix)

# =============================
# 🎨 SECTION 6: INTERPRETATION
# =============================
st.markdown("---")
st.header("Band Interpretation Guide")

col1, col2, col3, col4 = st.columns(4)

col1.markdown("**Healthy Vegetation**")
col1.markdown("<span style='color:#10B981'>High NDVI</span>", unsafe_allow_html=True)

col2.markdown("**Dry / Stressed**")
col2.markdown("<span style='color:#F59E0B'>Moderate NDVI</span>", unsafe_allow_html=True)

col3.markdown("**Urban / Bare Soil**")
col3.markdown("<span style='color:#64748B'>Low NDVI</span>", unsafe_allow_html=True)

col4.markdown("**Water / Snow**")
col4.markdown("<span style='color:#3B82F6'>High NDWI</span>", unsafe_allow_html=True)

# =============================
# 🧠 SECTION 7: EXTRACTION LOGIC
# =============================
st.markdown("---")
st.header("Pixel-Level Data Extraction Logic")

st.markdown("""
Data is extracted at pixel level using Earth Engine APIs.

Process:
- Satellite imagery is filtered by spatial and temporal bounds
- Bands are selected and aggregated (mean / median / max)
- Pixel values are reduced over the region of interest
- Values are normalized or converted to physical units

Each pixel represents reflectance or radiance measured at sensor level.
""")

st.code("""
Region → ImageCollection → Band Selection → Reducer → Value Extraction
""")

# =============================
# 📐 SECTION 8: FORMULAS
# =============================
st.markdown("---")
st.header("Core Indices & Formulas")

st.code("""
NDVI = (NIR - RED) / (NIR + RED)
→ Vegetation health

NDWI = (GREEN - NIR) / (GREEN + NIR)
→ Water detection

NDBI = (SWIR - NIR) / (SWIR + NIR)
→ Urban / built-up areas

NBR = (NIR - SWIR2) / (NIR + SWIR2)
→ Burn severity

LST = Radiance → Temperature conversion
→ Land surface temperature

Rainfall = Sum(CHIRPS precipitation)
→ mm over period

Wind Speed = sqrt(u² + v²)
→ ERA5 wind calculation
""")

# =============================
# 📖 SECTION 9: WHY USED
# =============================
st.markdown("---")
st.header("Scientific Purpose of Indices")

st.markdown("""
**NDVI:**  
Used to quantify vegetation density and photosynthetic activity.  
Higher values indicate healthy crops and forest cover.

**NDWI:**  
Highlights water bodies and moisture content.  
Used in flood and drought monitoring.

**NDBI:**  
Separates built-up areas from vegetation.  
Useful for urban expansion analysis.

**NBR:**  
Detects burned areas and vegetation stress.  
Used in wildfire impact assessment.

**LST:**  
Represents surface heat energy.  
Used in urban heat and climate studies.

**Rainfall (CHIRPS):**  
Provides precipitation trends for hydrological modeling.

**ERA5 Variables:**  
Used for climate, temperature, and wind analysis.

**Sentinel-5P:**  
Tracks atmospheric pollution levels (NO₂).
""")

# =============================
# 📅 SECTION 10: AVAILABILITY
# =============================
st.markdown("---")
st.header("Dataset Availability")

st.code("""
Sentinel-2: 2015 – Present | 10m | 5-day revisit
Landsat 8/9: 2013 – Present | 30m | 16-day revisit
Sentinel-1: 2014 – Present | Radar | 6–12 days
CHIRPS: 1981 – Present | Daily rainfall
ERA5: 1950 – Present | Global hourly/daily
Sentinel-5P: 2017 – Present | Daily pollution
MODIS: 1999 – Present | Daily global
""")

# =============================
# ⚠️ SECTION 11: QUALITY
# =============================
st.markdown("---")
st.header("Data Quality & Limitations")

st.markdown("""
- Cloud contamination affects optical data
- Radar avoids cloud issues (Sentinel-1)
- Temporal gaps handled via aggregation
- Atmospheric correction applied (Surface Reflectance)
- Spatial resolution varies (10m to 1km)
""")

# =============================
# ❓ SECTION 12: FAQ
# =============================
st.markdown("---")
st.header("FAQs")

st.markdown("""
**Q1: Why different satellites are used together?**  
To combine optical, thermal, radar, and atmospheric insights.

**Q2: Why NDVI range is -1 to 1?**  
It is a normalized ratio of reflectance values.

**Q3: Why sometimes data is missing?**  
Due to cloud cover or satellite revisit gaps.

**Q4: Which dataset is best for rainfall?**  
CHIRPS provides the most reliable long-term rainfall data.

**Q5: Can this be used for real-time decisions?**  
Yes, but depends on satellite revisit frequency.

**Q6: Why aggregation is needed?**  
To reduce noise and improve stability of results.
""")