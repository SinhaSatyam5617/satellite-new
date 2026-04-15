import sys
import os

# -----------------------------
# PATH FIX
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pydeck as pdk
import pandas as pd
import ee
import streamlit as st

def show():
    st.title("⚠️ Geo-Risk Time Explorer")

# ======================
# IMPORTS
# ======================
from engine.georisk_ai.gee import init_gee
from engine.georisk_ai.timeseries import (
    get_ndvi_timeseries_images,
    get_image_by_index
)
from engine.georisk_ai.grid import sample_ndvi_from_image
from engine.georisk_ai.risk import (
    calculate_risk,
    risk_label,
    generate_insight
)

# ======================
# INIT GEE
# ======================
@st.cache_resource
def load_gee():
    init_gee()

load_gee()

# ======================
# UI
# ======================
st.set_page_config(layout="wide")
st.title(" Geo-Risk Time Explorer")
st.markdown("""
This module performs time-series environmental analysis using satellite imagery.  
It extracts vegetation, water, and built-up indicators from Sentinel-2 data and computes a composite environmental risk score.  
All outputs are derived from real satellite acquisition dates and spatial aggregation over the selected polygon.
""")
# ======================
# INPUT: POLYGON
# ======================
st.subheader("📐 Enter 4 Coordinates (Polygon)")

coords = []

for i in range(4):
    col1, col2 = st.columns(2)
    lat = col1.number_input(f"Lat {i+1}", value=26.85 + i * 0.01)
    lon = col2.number_input(f"Lon {i+1}", value=80.94 + i * 0.01)
    coords.append([lon, lat])

polygon = coords

# ======================
# LOAD TIME SERIES
# ======================
if st.button("Load Time Series"):

    with st.spinner("Fetching satellite time series..."):
        ts_images = get_ndvi_timeseries_images(polygon)

    if not ts_images:
        st.error("❌ No time-series data available")
        st.stop()

    st.session_state["ts_images"] = ts_images

# ======================
# SAFE VALUE
# ======================
def safe_get(val):
    try:
        return val.getInfo() if val else 0
    except:
        return 0

# ======================
# FUNCTION: GET INDICES
# ======================
def get_indices_from_image(image, geometry):

    region = ee.Geometry.Polygon(geometry)

    # 🚨 CHECK BANDS FIRST
    band_names = image.bandNames().getInfo()

    if not band_names:
        return {"ndvi": 0, "ndwi": 0, "ndbi": 0}

    # ✅ Ensure NDVI exists
    if "NDVI" not in band_names:
        try:
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            image = image.addBands(ndvi)
        except:
            return {"ndvi": 0, "ndwi": 0, "ndbi": 0}

    # SAFE CALCULATIONS
    ndvi = image.select('NDVI')
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')

    combined = ndvi.addBands([ndwi, ndbi])

    stats = combined.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30,
        maxPixels=1e9,
        bestEffort=True
    )

    return {
        "ndvi": safe_get(stats.get('NDVI')),
        "ndwi": safe_get(stats.get('NDWI')),
        "ndbi": safe_get(stats.get('NDBI'))
    }

# ======================
# MAIN
# ======================
if "ts_images" in st.session_state:

    ts_images = st.session_state["ts_images"]

    index = st.slider(
        "📅 Time Slider",
        0,
        len(ts_images) - 1,
        0
    )

    selected = ts_images[index]

    st.markdown(f"### 📅 Date: `{selected['date']}`")

    with st.spinner("Processing satellite data..."):

        # -----------------------------
        # IMAGE FETCH
        # -----------------------------
        image = get_image_by_index(polygon, selected["index"])

        if image is None:
            st.warning("❌ No image available for this date")
            st.stop()

        # -----------------------------
        # GRID
        # -----------------------------
        grid = sample_ndvi_from_image(image, polygon)

        if not grid:
            st.warning("❌ No spatial data found")
            st.stop()

        # -----------------------------
        # INDICES
        # -----------------------------
        indices = get_indices_from_image(image, polygon)

        # -----------------------------
        # RISK
        # -----------------------------
        risk = calculate_risk(
            indices["ndvi"],
            indices["ndwi"],
            indices["ndbi"]
        )

        label = risk_label(risk)

        insight = generate_insight(
            indices["ndvi"],
            indices["ndwi"],
            indices["ndbi"],
            risk
        )

    # ======================
    # METRICS
    # ======================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Risk Score", risk)
    c2.metric("NDVI", round(indices["ndvi"], 3))
    c3.metric("NDWI", round(indices["ndwi"], 3))
    c4.metric("NDBI", round(indices["ndbi"], 3))

    st.markdown(f"### {label}")
    st.info(insight)

    # ======================
    # MAP
    # ======================
    df = pd.DataFrame(grid)

    if df.empty:
        st.warning("No map data")
        st.stop()

    hex_layer = pdk.Layer(
        "HexagonLayer",
        data=df,
        get_position='[lon, lat]',
        radius=120,
        elevation_scale=40,
        get_elevation='value',
        get_fill_color='[255 * (1 - value), 255 * value, 80]',
        extruded=True,
        pickable=True,
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": polygon}],
        get_polygon="polygon",
        get_line_color=[255, 0, 0],
        line_width_min_pixels=2,
        get_fill_color=[0, 0, 0, 20],
    )

    view = pdk.ViewState(
        latitude=float(df["lat"].mean()),
        longitude=float(df["lon"].mean()),
        zoom=12
    )

    st.subheader("🧊 NDVI Spatial Map")

    st.pydeck_chart(
        pdk.Deck(
            layers=[polygon_layer, hex_layer],
            initial_view_state=view
        )
    )

st.markdown("### Processing Workflow")

st.markdown("""
- User defines a polygon using coordinates  
- Satellite time-series is fetched for the region  
- A time slider selects a specific satellite date  
- NDVI, NDWI, and NDBI are computed  
- Mean values are extracted over the region  
- A risk score is calculated from indices  
- Spatial grid is generated for visualization  
- Insights are generated based on environmental conditions  
""")

st.markdown("### Date Handling")

st.markdown("""
Dates are automatically derived from satellite availability.  
The system does not use manually entered dates.

- Time-series is generated using available satellite passes  
- Each slider step corresponds to a real acquisition date  
- The selected index maps to a specific satellite image  

This ensures all analysis is based on real observed data rather than interpolated values.
""")

st.markdown("### Date Handling")

st.markdown("""
Dates are automatically derived from satellite availability.  
The system does not use manually entered dates.

- Time-series is generated using available satellite passes  
- Each slider step corresponds to a real acquisition date  
- The selected index maps to a specific satellite image  

This ensures all analysis is based on real observed data rather than interpolated values.
""")

st.markdown("### Spectral Band Matrix")

st.code("""
Band     | Wavelength (µm) | Operational Use
---------|------------------|----------------------------
B3       | 0.56             | Water detection, vegetation
B4       | 0.665            | Chlorophyll absorption
B8       | 0.842            | Vegetation health (NIR)
B11      | 1.61             | Moisture & urban detection
""")

st.markdown("### Spectral Indices")

st.code("""
NDVI  = (B8 - B4) / (B8 + B4)
NDWI  = (B3 - B8) / (B3 + B8)
NDBI  = (B11 - B8) / (B11 + B8)
""")

st.markdown("""
Interpretation:

- NDVI:
  High → Dense vegetation  
  Low → Sparse or no vegetation  

- NDWI:
  High → Water presence  
  Low → Dry land  

- NDBI:
  High → Built-up / urban areas  
  Low → Natural surfaces  
""")

st.markdown("### Core Calculation")

st.markdown("""
For each selected date:

1. Satellite image is retrieved  
2. Indices are computed per pixel  
3. Values are aggregated using mean over the polygon  

Mathematically:

Mean Index = Σ(pixel values) / number of pixels

These mean values are used as representative environmental indicators for the region.
""")

st.markdown("### Core Calculation")

st.markdown("""
For each selected date:

1. Satellite image is retrieved  
2. Indices are computed per pixel  
3. Values are aggregated using mean over the polygon  

Mathematically:

Mean Index = Σ(pixel values) / number of pixels

These mean values are used as representative environmental indicators for the region.
""")

st.markdown("### Insight Generation")

st.markdown("""
Insights are generated based on computed indices and risk score.

Input:
- NDVI, NDWI, NDBI  
- Risk score  

Output:
- Environmental condition summary  
- Interpretation of vegetation, water, and urban impact  

This provides a simplified explanation of complex satellite-derived data.
""")

st.markdown("### Challenges & Handling")

st.markdown("""
Potential Issues and Solutions:

- Missing satellite data:
  → Handled by checking image availability before processing  

- Missing bands (e.g., B8):
  → Prevented using safe image validation  

- Null values from reduceRegion:
  → Replaced with fallback values (0)  

- Small or invalid polygon:
  → Execution stopped with warning  

- Sparse grid sampling:
  → Map rendering skipped safely  
""")

st.markdown("### Limitations")

st.markdown("""
- Uses mean aggregation (no variance or distribution analysis)  
- Limited to Sentinel-2 (no multi-satellite fusion)  
- Simplified risk model (not machine learning-based)  
- No advanced cloud masking beyond basic filtering  
- Does not include weather or rainfall data  
""")

st.markdown("### Future Scope")

st.markdown("""
- Integration with CHIRPS (rainfall)  
- Integration with ERA5 (temperature, weather)  
- Pollution analysis using Sentinel-5P  
- Multi-year trend analysis  
- Machine learning-based risk prediction  
- AI-generated recommendations and forecasting  
""")

st.markdown("### Interpretation Guide")

st.markdown("""
- NDVI close to 1 → Dense vegetation  
- NDVI near 0 → Sparse vegetation  
- NDWI > 0 → Water presence  
- NDBI > 0 → Built-up area  

Combined interpretation:

- High NDVI + Low NDBI → Healthy ecosystem  
- Low NDVI + High NDBI → Urban stress  
- Low NDWI → Dry conditions  

This enables quick environmental assessment for any region.
""")