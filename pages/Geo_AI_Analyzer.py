# ----------------------------------
# 🧠 FIX PATH
# ----------------------------------
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ----------------------------------
# 📦 IMPORTS
# ----------------------------------
import streamlit as st
from datetime import datetime
import json

from engine.data.unified_features import get_unified_features
from engine.analysis.analyzer_rules import analyze_all
from geo_langchain import run_ai

from streamlit_folium import st_folium
import folium
import streamlit as st

def show():
    st.title("🧠 Geo AI Analyzer")

# ----------------------------------
# 🎨 CONFIG
# ----------------------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.title {font-size:36px;font-weight:bold;color:#2E86C1;}
.card {padding:20px;border-radius:10px;background:#f5f7fa;}
.metric {background:#eef;padding:15px;border-radius:8px;text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title"> Geo AI Analyzer</div>', unsafe_allow_html=True)
st.markdown("""This module integrates multi-satellite data with rule-based analytics and AI reasoning to evaluate environmental conditions for any location.  
            It combines vegetation, rainfall, temperature, land surface heat, and atmospheric pollution into a unified geospatial intelligence system.  
            The output includes quantitative metrics, rule-based interpretation, and AI-driven insights for decision support""")

st.markdown("---")
# ----------------------------------
# MAP
# ----------------------------------
st.subheader("🗺️ Select Location")

m = folium.Map(location=[26.85, 80.95], zoom_start=5)
map_data = st_folium(m, height=400)

lat, lon = None, None
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"📍 {lat:.4f}, {lon:.4f}")

# ----------------------------------
# DATE
# ----------------------------------
st.subheader("📅 Date Range")

col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime(2023, 1, 1))
end_date = col2.date_input("End Date", datetime.today())

# ----------------------------------
# QUESTION
# ----------------------------------
st.subheader("❓ Ask Your Question")

question = st.text_area("", placeholder="e.g. Is this area good for farming in March?")

# ----------------------------------
# RUN
# ----------------------------------
if st.button("🚀 Analyze Location", use_container_width=True):

    if lat is None:
        st.warning("Select location")
        st.stop()

    if not question:
        st.warning("Enter question")
        st.stop()

    with st.spinner("Processing..."):

        try:
            # ----------------------------------
            # DATA
            # ----------------------------------
            data = get_unified_features(lat, lon, start_date=start_date, end_date=end_date)
            pollution = data["pollution"]

            # ----------------------------------
            # RULES
            # ----------------------------------
            rules = analyze_all(data)

            st.success("Data Loaded ✅")

            # ----------------------------------
            # METRICS
            # ----------------------------------
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("NDVI", round(data["ndvi"], 3))
            c2.metric("Rainfall", round(data["rainfall"], 2))
            c3.metric("Temp", round(data["temperature"], 2))
            c4.metric("LST", round(data["lst"], 2))

            c5, c6, c7, c8 = st.columns(4)
            c5.metric("NO₂", f"{pollution['no2']:.6f}")
            c6.metric("CO", f"{pollution['co']:.6f}")
            c7.metric("O₃", f"{pollution['o3']:.6f}")
            c8.metric("SO₂", f"{pollution['so2']:.6f}")

            st.markdown("---")

            # ----------------------------------
            # RULES
            # ----------------------------------
            st.subheader("📊 Rule-Based Analysis")
            for k, v in rules.items():
                st.write(f"**{k.upper()}**: {v}")

            st.markdown("---")

            # ----------------------------------
            # AI
            # ----------------------------------
            ai = run_ai(lat, lon, question, start_date, end_date)

            # SAFE PARSE
            if isinstance(ai, str):
                try:
                    ai = json.loads(ai)
                except:
                    st.error("AI parsing failed")
                    st.code(ai)
                    st.stop()

            # ----------------------------------
            # DISPLAY AI
            # ----------------------------------
            st.subheader("🤖 AI Insight")

            c1, c2 = st.columns(2)
            c1.metric("Risk Level", ai.get("risk_level", "N/A"))
            c2.metric("Suitability Score", ai.get("suitability_score", 0))

            st.markdown("### 🧠 Summary")
            st.write(ai.get("summary", ""))

            st.markdown("### 📊 Key Factors")
            for f in ai.get("key_factors") or []:
                st.write(f"- {f}")

            st.markdown("### ✅ Recommendations")
            for r in ai.get("recommendations") or []:
                st.write(f"- {r}")

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("### Use Cases")

st.markdown("""
- Agricultural suitability and crop planning  
- Environmental risk assessment (flood, drought, heat)  
- Urban expansion and land-use monitoring  
- Climate and ecosystem analysis  
- Site selection for infrastructure or farming  
""")

st.markdown("### Processing Workflow")

st.markdown("""
1. User selects geographic coordinates via map  
2. Date range filters satellite datasets  
3. Multi-source data is extracted:
   - Vegetation (Sentinel-2)
   - Rainfall (CHIRPS)
   - Temperature (ERA5)
   - Land Surface Temp (Landsat)
   - Pollution (Sentinel-5P)  
4. Pixel-level aggregation is applied (mean/median)  
5. Rule-based classification evaluates each parameter  
6. AI model generates contextual insights and recommendations  
""")

st.markdown("### Satellite Data Sources")

st.markdown("""
**Sentinel-2 (Optical):**  
Used for vegetation analysis via NDVI.

**CHIRPS (Rainfall):**  
Provides precipitation data in mm.

**ERA5 (Weather):**  
Temperature and atmospheric conditions.

**Landsat (Thermal):**  
Land Surface Temperature (LST).

**Sentinel-5P (Atmospheric):**  
Pollution gases (NO₂, CO, O₃, SO₂).
""")

st.markdown("### Core Calculations")

st.code("""
NDVI = (NIR - RED) / (NIR + RED)

Rainfall = Sum(CHIRPS daily precipitation)

Temperature = ERA5 (Kelvin → Celsius)

Wind Speed = sqrt(u² + v²)

LST = Thermal band conversion (Kelvin → Celsius)

Pollution = Mean atmospheric column density
""")

st.markdown("### Scientific Importance")

st.markdown("""
**NDVI:** Indicates vegetation health and crop productivity  
**Rainfall:** Determines water availability and flood risk  
**Temperature:** Impacts crop growth and environmental stress  
**LST:** Measures surface heating and urban heat effects  
**Pollution:** Reflects air quality and environmental health  
""")

st.markdown("### Rule-Based Interpretation Logic")

st.markdown("""
Each parameter is classified using threshold-based rules:

- Vegetation: Low / Moderate / High  
- Rainfall: Low (<20), Moderate (20–80), High (>80)  
- Temperature: Cool / Moderate / Hot  
- Pollution: Combined gas concentration levels  

These rules provide fast, interpretable baseline insights before AI analysis.
""")

st.markdown("### AI Insight Engine")

st.markdown("""
The AI model analyzes combined satellite features along with user queries.

It generates:
- Risk Level (Low / Moderate / High)  
- Suitability Score (0–100)  
- Contextual summary  
- Key influencing factors  
- Actionable recommendations  

This layer converts raw geospatial data into decision-ready intelligence.
""")

st.markdown("### Interpretation Guide")

st.markdown("""
| Parameter | Good | Moderate | Poor |
|----------|------|----------|------|
| NDVI | > 0.6 | 0.3–0.6 | < 0.3 |
| Rainfall | 20–80 mm | <20 or >80 | Extreme |
| Temp | 20–30°C | 10–20°C | >35°C |
| Pollution | Low gases | Mixed | High |
""")

st.markdown("### Challenges & Solutions")

st.markdown("""
**Cloud Noise:**  
Optical data affected → mitigated using aggregation  

**Data Gaps:**  
Handled via multi-day temporal window  

**Sensor Differences:**  
Standardized using calibrated datasets  

**Noise in Values:**  
Reduced via mean/median computation  
""")

st.markdown("### Limitations")

st.markdown("""
- Satellite revisit delays affect real-time accuracy  
- Pollution values are column-based, not ground sensors  
- NDVI cannot distinguish crop types  
- Resolution varies across datasets  
""")

st.markdown("### Future Scope")

st.markdown("""
- Time-series trend analysis  
- AI-based prediction (yield, flood, drought)  
- Multi-index fusion (NDVI + NDWI + NDBI)  
- Real-time monitoring dashboards  
- API-based data access for businesses  
""")

st.markdown("---")
st.caption("GeoAI Analyzer • Multi-Satellite Intelligence Platform")