# ----------------------------------
# 🧠 FIX PATH
# ----------------------------------
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ----------------------------------
# 📦 IMPORTS
# ----------------------------------
import streamlit as st
import json
from datetime import datetime
import folium
from streamlit_folium import st_folium

from engine.data.unified_features import get_unified_features
from geo_langchain import run_ai
import streamlit as st

def show():
    st.title(" Satellite Vegetation Module")

# ----------------------------------
# 🎨 CONFIG
# ----------------------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.title {font-size:36px;font-weight:bold;color:#2E86C1;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Satellite Vegetation Module</div>', unsafe_allow_html=True)

st.markdown("""
This module analyzes vegetation health using NDVI derived from satellite data over a selected location and time range.
""")

st.markdown("---")

# ----------------------------------
# 🗺️ MAP
# ----------------------------------
st.subheader(" Select Location")

m = folium.Map(location=[26.85, 80.95], zoom_start=5)
map_data = st_folium(m, height=400)

lat, lon = None, None

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"📍 {lat:.4f}, {lon:.4f}")

# ----------------------------------
# 📅 DATE
# ----------------------------------
st.subheader(" Date Range")

col1, col2 = st.columns(2)

start_date = col1.date_input("Start Date", datetime(2023, 1, 1))
end_date = col2.date_input("End Date", datetime.today())

# ----------------------------------
# 🚀 RUN
# ----------------------------------
if st.button("🚀 Analyze NDVI", use_container_width=True):

    if lat is None:
        st.warning("Select location")
        st.stop()

    with st.spinner("Processing NDVI..."):

        try:
            # ----------------------------------
            # DATA
            # ----------------------------------
            data = get_unified_features(
                lat,
                lon,
                start_date=start_date,
                end_date=end_date
            )

            ndvi = data.get("ndvi", 0)

            if ndvi == 0:
                st.error("No NDVI data available")
                st.stop()

            # ----------------------------------
            # SCORE + CATEGORY
            # ----------------------------------
            score = ((ndvi + 1) / 2) * 100

            if ndvi >= 0.6:
                category = "Dense Vegetation"
            elif ndvi >= 0.3:
                category = "Moderate Vegetation"
            else:
                category = "Sparse Vegetation"

            # ----------------------------------
            # DISPLAY METRICS
            # ----------------------------------
            c1, c2, c3 = st.columns(3)

            c1.metric("NDVI", round(ndvi, 3))
            c2.metric("Score", round(score, 1))
            c3.metric("Category", category)

            st.markdown("---")

            # ----------------------------------
            # 🤖 AI SECTION (MATCH WORKING FILE)
            # ----------------------------------
            st.subheader(" AI Insight")

            try:
                question = f"""
NDVI is {ndvi}.
Explain vegetation health and farming suitability.
"""

                ai = run_ai(lat, lon, question, start_date, end_date)

                # SAFE PARSE (same as working file)
                if isinstance(ai, str):
                    try:
                        ai = json.loads(ai)
                    except:
                        st.error("AI parsing failed")
                        st.code(ai)
                        st.stop()

                # DISPLAY (same structure as working analyzer)
                c1, c2 = st.columns(2)

                c1.metric("Risk Level", ai.get("risk_level", "N/A"))
                c2.metric("Suitability Score", ai.get("suitability_score", 0))

                st.markdown("###  Summary")
                st.write(ai.get("summary", ""))

                st.markdown("### Key Factors")
                for f in ai.get("key_factors") or []:
                    st.write(f"- {f}")

                st.markdown("###  Recommendations")
                for r in ai.get("recommendations") or []:
                    st.write(f"- {r}")

            except Exception as e:
                st.error(f"❌ AI Error: {e}")

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("### Use Cases")

st.markdown("""
- Vegetation density analysis for selected regions  
- Basic agricultural suitability assessment  
- Monitoring land health over a time period  
- Comparing vegetation conditions across locations  
""")

st.markdown("### Processing Workflow")

st.markdown("""
1. User selects a location on the map  
2. Date range is selected manually  
3. Satellite data is fetched using the unified feature pipeline  
4. NDVI value is extracted from the dataset  
5. Vegetation score is calculated from NDVI  
6. Rule-based category is assigned  
7. AI insight is optionally generated if available  
""")

st.markdown("### Data Source")

st.markdown("""
NDVI is retrieved using the unified feature pipeline.

- Source: Satellite-derived NDVI (via backend engine)
- Data is aggregated over selected location and date range
- Value represents average vegetation condition

Note: This module only uses NDVI from the dataset and does not use other variables.
""")

st.markdown("### Core Calculation")

st.code("""
Vegetation Score = ((NDVI + 1) / 2) × 100
""")

st.markdown("### Classification Logic")

st.markdown("""
Vegetation is classified based on NDVI thresholds:

- NDVI ≥ 0.6 → Dense Vegetation  
- NDVI ≥ 0.3 → Moderate Vegetation  
- NDVI < 0.3 → Sparse Vegetation  
""")

st.markdown("### Why NDVI")

st.markdown("""
NDVI is used as a direct indicator of vegetation density.

Higher NDVI values correspond to healthier vegetation, while lower values indicate sparse or stressed vegetation.

This module uses NDVI as the primary metric for vegetation analysis.
""")

st.markdown("### AI Insight")

st.markdown("""
AI is optionally used to generate textual interpretation.

- Input: NDVI value + user-selected location and date  
- Output: Explanation of vegetation health and farming suitability  

If API quota is exceeded or unavailable, AI output is skipped.
""")

st.markdown("### Interpretation")

st.markdown("""
- NDVI value represents vegetation density  
- Vegetation Score converts NDVI into a percentage scale  
- Category provides a simplified classification  

These outputs help in quick understanding of land vegetation condition.
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Missing Data: If NDVI = 0, system stops execution  
- AI Failure: API errors handled with fallback message  
- User Input: Requires location selection before processing  
""")

st.markdown("### Limitations")

st.markdown("""
- Only NDVI is used (no rainfall, temperature, or other factors)  
- No time-series analysis (single aggregated value)  
- No multi-index analysis (NDWI, NDBI not included)  
- AI depends on external API availability  
""")

st.markdown("### Future Scope")

st.markdown("""
- Integration of additional indices (NDWI, NDBI)  
- Inclusion of rainfall and temperature data  
- Time-series vegetation trend analysis  
- Improved AI-based agricultural recommendations  
""")

st.markdown("---")
st.caption("NDVI Analyzer • Satellite Vegetation Module")
