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
import folium
from streamlit_folium import st_folium

from engine.data.unified_features import get_unified_features
import streamlit as st

def show():
    st.title("🌦 Weather Intelligence Module")
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
.title {font-size:36px;font-weight:bold;color:#3498DB;}
.box {padding:20px;border-radius:10px;background:#eef7ff;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌦️ Weather Intelligence Module</div>', unsafe_allow_html=True)

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
start_date = col1.date_input("Start Date", datetime(2023,1,1))
end_date   = col2.date_input("End Date", datetime.today())

# ----------------------------------
# RUN
# ----------------------------------
if st.button("🌦️ Analyze Weather", use_container_width=True):

    if lat is None:
        st.warning("Select location")
        st.stop()

    if start_date > end_date:
        st.error("Invalid date range")
        st.stop()

    with st.spinner("Fetching weather data..."):

        try:
            data = get_unified_features(lat, lon, start_date=start_date, end_date=end_date)

            rain = data["rainfall"]
            temp = data["temperature"]
            humidity = data["humidity"]
            heat = data["heat_index"]
            anomaly = data["anomaly"]

            if rain == 0 and temp == 0:
                st.warning("No valid data")
                st.stop()

            # METRICS
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Rainfall", round(rain,2))
            c2.metric("Temperature", round(temp,2))
            c3.metric("Humidity", round(humidity,2))
            c4.metric("Heat Index", round(heat,2))

            st.markdown("---")

            # RULES
            st.subheader("📊 Climate Analysis")

            if rain > 150:
                st.write("🌊 Flood risk")
            elif rain < 10:
                st.write("🌵 Drought risk")

            if temp > 35:
                st.write("🔥 Heatwave")
            elif temp < 15:
                st.write("❄️ Cold")

            if humidity > 80:
                st.write("💧 High humidity")

            if anomaly > 3:
                st.write("📈 Above normal temp")
            elif anomaly < -3:
                st.write("📉 Below normal")

            st.markdown("---")

            # AI
            st.subheader("🤖 AI Insight")

            if AI_AVAILABLE:
                try:
                    prompt = f"""
Rainfall: {rain}
Temperature: {temp}
Humidity: {humidity}
Heat Index: {heat}
Anomaly: {anomaly}

Explain climate condition and farming suitability
"""

                    ai = run_ai(lat, lon, prompt)

                    if ai:
                        st.write(ai)
                    else:
                        st.warning("AI returned empty")

                except Exception as e:
                    st.warning("AI not working")
                    st.code(str(e))

        except Exception as e:
            st.error(f"❌ Error: {e}")
            
st.markdown("### Weather Data Extraction")

st.markdown("""
This function retrieves satellite-derived climate variables for a selected location and date range.

It focuses on extracting core environmental parameters required for climate analysis.
""")

st.markdown("#### Processing Steps")

st.markdown("""
1. User selects location on map  
2. Date range is provided manually  
3. Unified feature pipeline is called  
4. Climate variables are extracted:
   - Rainfall  
   - Temperature  
   - Humidity  
   - Heat Index  
   - Temperature anomaly  
5. Values are aggregated over the selected region  
""")

st.markdown("#### Extracted Variables")

st.markdown("""
- Rainfall  
- Temperature  
- Humidity  
- Heat Index  
- Temperature Anomaly  

All values represent averaged satellite-derived conditions.
""")

st.markdown("#### Derived Metrics")

st.code("""
Rainfall → Aggregated precipitation

Temperature → Converted to °C

Heat Index → Combination of temperature + humidity

Anomaly → Deviation from normal temperature
""")

st.markdown("#### Data Validation")

st.markdown("""
- If rainfall = 0 and temperature = 0 → treated as no data  
- Prevents false interpretation due to missing satellite coverage  
""")

st.markdown("#### Data Validation")

st.markdown("""
- If rainfall = 0 and temperature = 0 → treated as no data  
- Prevents false interpretation due to missing satellite coverage  
""")

st.code("""
Rainfall:
> 150 → Flood risk
< 10 → Drought risk

Temperature:
> 35 → Heatwave risk
< 15 → Cold conditions

Humidity:
> 80 → High discomfort

Temperature Anomaly:
> +3 → Above normal
< -3 → Below normal
""")

st.markdown("#### Output")

st.markdown("""
- Generates a list of climate insights  
- If no condition triggered → "Stable climate conditions"  
- Provides quick environmental risk overview  
""")

st.markdown("### AI Insight Engine")

st.markdown("""
AI is used to generate contextual interpretation of climate conditions.

Input:
- Rainfall
- Temperature
- Humidity
- Heat Index
- Anomaly

Output:
- Climate summary  
- Flood or drought risk  
- Human comfort analysis  
- Farming suitability  
""")

st.markdown("#### AI Handling")

st.markdown("""
- AI execution is optional  
- If API fails or quota exceeded:
  - Warning is shown  
  - Rule-based output is still displayed  
- Prevents blank screen failures  
""")

st.markdown("### Interpretation Guide")

st.markdown("""
| Parameter | Condition | Meaning |
|----------|----------|--------|
| Rainfall >150 | High | Flood risk |
| Rainfall <10 | Low | Drought risk |
| Temp >35°C | High | Heat stress |
| Temp <15°C | Low | Cold |
| Humidity >80% | High | Discomfort |
| Anomaly >3 | Positive | Warmer than normal |
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Missing data → detected using zero-value check  
- Invalid date range → blocked before processing  
- AI failures → fallback to rule-based system  
- Requires manual location selection  
""")

st.markdown("### Limitations")

st.markdown("""
- Does not include wind speed in analysis  
- Heat index formula not shown explicitly  
- No time-series trends (single aggregated output)  
- AI output depends on API availability  
""")

st.markdown("### Future Scope")

st.markdown("""
- Add wind speed and pressure analysis  
- Include time-series climate trends  
- Improve heat index modeling  
- Advanced AI-based climate prediction  
""")

st.markdown("---")
st.caption("Weather Intelligence Module • Climate Analysis Engine")