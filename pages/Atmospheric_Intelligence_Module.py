# ----------------------------------
# 🧠 FIX PATH
# ----------------------------------
import ee
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ----------------------------------
# 📦 IMPORTS
# ----------------------------------
import streamlit as st
from datetime import datetime
import folium
from streamlit_folium import st_folium

from engine.data.unified_features import get_unified_features
import streamlit as st

def show():
    st.title(" Atmospheric Intelligence Module")

# SAFE AI
try:
    from geo_langchain import run_ai
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ----------------------------------
# 🎨 CONFIG
# ----------------------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.title {font-size:36px;font-weight:bold;color:#8E44AD;}
.box {padding:20px;border-radius:10px;background:#f5f0ff;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Atmospheric Intelligence Module</div>', unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------
# MAP
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
# DATE
# ----------------------------------
st.subheader(" Date Range")

col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime(2023,1,1))
end_date   = col2.date_input("End Date", datetime.today())

# ----------------------------------
# RUN
# ----------------------------------
if st.button("Analyze Pollution", use_container_width=True):

    if lat is None:
        st.warning("Select location")
        st.stop()

    with st.spinner("Analyzing pollution..."):

        try:
            data = get_unified_features(lat, lon, start_date=start_date, end_date=end_date)

            pollution = data["pollution"]

            no2 = pollution["no2"]
            co  = pollution["co"]
            o3  = pollution["o3"]
            so2 = pollution["so2"]

            def norm(v, max_val):
                return min(100, (v / max_val) * 100)

            score = int(
                norm(no2, 0.0002) * 0.3 +
                norm(o3, 0.2) * 0.3 +
                norm(co, 0.1) * 0.2 +
                norm(so2, 0.0003) * 0.2
            )

            if score < 30:
                label = "Good"
                impact = "Safe air quality"
            elif score < 70:
                label = "Moderate"
                impact = "Sensitive groups affected"
            else:
                label = "Poor"
                impact = "Health risk"

            # DISPLAY
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("NO₂", f"{no2:.6f}")
            c2.metric("CO", f"{co:.6f}")
            c3.metric("O₃", f"{o3:.6f}")
            c4.metric("SO₂", f"{so2:.6f}")

            st.markdown("---")

            c1, c2 = st.columns(2)
            c1.metric("Pollution Score", score)
            c2.metric("Category", label)

            st.write(f"**Impact:** {impact}")

            st.markdown("---")

            # AI
            st.subheader(" AI Insight")

            if AI_AVAILABLE:
                try:
                    prompt = f"""
Pollution data:
NO2={no2}, CO={co}, O3={o3}, SO2={so2}
Score={score}
Explain health impact and precautions
"""

                    ai = run_ai(lat, lon, prompt, start_date, end_date)

                    if ai:
                        st.write(ai)
                    else:
                        st.warning("AI returned empty")

                except Exception as e:
                    st.warning("AI not working")
                    st.code(str(e))

        except Exception as e:
            st.error(f"❌ Error: {e}")


st.markdown("### Processing Workflow")

st.markdown("""
1. User selects a geographic location on the map  
2. Date range is applied to filter satellite data  
3. Pollution data is retrieved from the unified feature pipeline  
4. Individual gas values are extracted (NO₂, CO, O₃, SO₂)  
5. Each gas is normalized relative to a fixed threshold  
6. A weighted pollution score is computed  
7. Score is classified into Good, Moderate, or Poor  
8. AI generates optional health insights if available  
""")

st.markdown("### Use Cases")

st.markdown("""
- Air quality assessment for specific locations  
- Health risk evaluation based on pollution levels  
- Environmental monitoring and comparison across regions  
- Identifying areas with elevated atmospheric pollution  
""")

st.markdown("### Data Source")

st.markdown("""
Pollution values are obtained through the unified feature pipeline.

- Variables used:
  - NO₂ (Nitrogen Dioxide)
  - CO (Carbon Monoxide)
  - O₃ (Ozone)
  - SO₂ (Sulfur Dioxide)

Values represent averaged atmospheric concentrations over the selected region and time range.
""")

st.markdown("### Core Calculation")

st.code("""
Normalize each gas:

NO2_score = (NO2 / 0.0002) × 100
CO_score  = (CO / 0.1) × 100
O3_score  = (O3 / 0.2) × 100
SO2_score = (SO2 / 0.0003) × 100

Pollution Score =
(0.3 × NO2_score) +
(0.3 × O3_score) +
(0.2 × CO_score) +
(0.2 × SO2_score)

Final score capped at 100
""")

st.markdown("### Classification Logic")

st.markdown("""
Pollution Score is interpreted as:

- Score < 30 → Good (Safe air quality)  
- Score < 70 → Moderate (Sensitive groups affected)  
- Score ≥ 70 → Poor (Health risk for all)  
""")

st.markdown("### Why These Pollutants")

st.markdown("""
**NO₂:** Indicator of traffic and industrial emissions  

**CO:** Represents incomplete combustion processes  

**O₃:** Secondary pollutant affecting respiratory health  

**SO₂:** Emitted from industrial and fossil fuel sources  

These gases are combined to provide a simplified overall air quality indicator.
""")

st.markdown("### AI Insight")

st.markdown("""
AI is used to generate health-related explanations based on pollution data.

- Input: Gas values + pollution score  
- Output: Health impact explanation and precautions  

If API quota is exceeded or unavailable, AI output is skipped and a warning is shown.
""")

st.markdown("### Interpretation")

st.markdown("""
- Individual gas values show pollutant concentration  
- Pollution Score provides a combined metric  
- Classification simplifies understanding of air quality  

This enables quick assessment of environmental conditions for the selected location.
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Missing location input → execution stopped  
- AI failure → handled with warning message  
- Data variability → normalized using fixed thresholds  
""")

st.markdown("### Limitations")

st.markdown("""
- Uses fixed normalization thresholds (not dynamic AQI standards)  
- Does not include particulate matter (PM2.5, PM10)  
- Pollution score is simplified and not equivalent to official AQI  
- AI output depends on external API availability  
""")

st.markdown("### Future Scope")

st.markdown("""
- Integration of PM2.5 and PM10 data  
- Dynamic AQI calculation based on standards  
- Time-series pollution trend analysis  
- Enhanced AI-based health recommendations  
""")

st.markdown("---")
st.caption("Pollution Analyzer • Atmospheric Intelligence Module")
