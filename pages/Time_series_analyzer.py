# ----------------------------------
# 🧠 FIX IMPORT PATH
# ----------------------------------
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ----------------------------------
# 📦 IMPORTS
# ----------------------------------
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

from engine.data.unified_features import get_unified_features
import streamlit as st

def show():
    st.title("Time-Series Analyzer")

# SAFE AI (optional)
try:
    from geo_langchain import run_ai
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ----------------------------------
#  PAGE CONFIG
# ----------------------------------
st.set_page_config(layout="wide")

st.markdown("## Time-Series Analyzer")
st.markdown("""
This module performs time-series analysis of vegetation, rainfall, and temperature using satellite-derived data.
""")

st.markdown("---")

# ----------------------------------
# 🗺️ MAP
# ----------------------------------
st.subheader("Select Location")

m = folium.Map(location=[26.85, 80.95], zoom_start=5)
map_data = st_folium(m, height=400)

lat, lon = None, None

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"📍 Selected: {lat:.4f}, {lon:.4f}")

st.markdown("---")

# ----------------------------------
# 📅 DATE RANGE
# ----------------------------------
st.subheader(" Select Date Range")

col1, col2 = st.columns(2)

start_date = col1.date_input("Start Date", datetime(2023, 1, 1))
end_date = col2.date_input("End Date", datetime.today())

# ----------------------------------
# 🚀 RUN
# ----------------------------------
if st.button(" Analyze Trends", use_container_width=True):

    if lat is None:
        st.warning("⚠️Please select a location")
        st.stop()

    if start_date >= end_date:
        st.warning("⚠️ Invalid date range")
        st.stop()

    with st.spinner("🛰️ Fetching satellite time-series..Depending on the data, it may take 30 seconds to 5 minutes"):

        try:
            dates, ndvi, rain, temp = [], [], [], []

            current = start_date

            # ----------------------------------
            # LOOP
            # ----------------------------------
            while current <= end_date:

                data = get_unified_features(
                    lat, lon,
                    start_date=current - timedelta(days=7),
                    end_date=current
                )

                if data["ndvi"] == 0:
                    current += timedelta(days=1)
                    continue

                dates.append(current.strftime("%Y-%m-%d"))
                ndvi.append(data["ndvi"])
                rain.append(data["rainfall"])
                temp.append(data["temperature"])

                current += timedelta(days=1)

            # ----------------------------------
            # NO DATA
            # ----------------------------------
            if len(ndvi) == 0:
                st.error(" No valid satellite data")
                st.stop()

            # ----------------------------------
            # DATAFRAME
            # ----------------------------------
            df = pd.DataFrame({
                "Date": dates,
                "NDVI": ndvi,
                "Rainfall": rain,
                "Temperature": temp
            }).sort_values("Date")

            st.success("Data Loaded ")

            # ----------------------------------
            # CHART
            # ----------------------------------
            st.markdown("### 📈 Trends")
            st.line_chart(df.set_index("Date"))

            st.markdown("---")

            # ----------------------------------
            # METRICS
            # ----------------------------------
            avg_ndvi = np.mean(ndvi)
            score = (avg_ndvi + 1) / 2 * 100 if avg_ndvi != 0 else 0

            slope = np.polyfit(range(len(ndvi)), ndvi, 1)[0] if len(ndvi) > 1 else 0
            volatility = np.std(ndvi)

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("NDVI Score", round(score, 1))
            c2.metric("Trend", round(slope, 4))
            c3.metric("Volatility", round(volatility, 3))
            c4.metric("Current NDVI", round(ndvi[-1], 3))

            st.markdown("---")

            # ----------------------------------
            # RISK
            # ----------------------------------
            st.markdown("## ⚠️ Risk Analysis")

            risks = []

            if avg_ndvi < 0.3:
                risks.append(" Drought risk")

            if np.mean(rain) > 20:
                risks.append(" Flood risk")

            if slope < -0.01:
                risks.append("Vegetation declining")

            if not risks:
                risks.append(" Stable conditions")

            for r in risks:
                st.write(f"- {r}")

            st.markdown("---")

            # ----------------------------------
            # 🤖 AI (SAFE TEXT MODE)
            # ----------------------------------
            st.subheader("AI Insight")

            if AI_AVAILABLE:
                try:
                    prompt = f"""
NDVI trend: {round(avg_ndvi,2)}
Slope: {round(slope,4)}
Rainfall avg: {round(np.mean(rain),2)}
Temperature avg: {round(np.mean(temp),2)}

Explain environmental trend and risks
"""

                    ai = run_ai(lat, lon, prompt, start_date, end_date)

                    if ai:
                        st.markdown(ai)
                    else:
                        st.warning("AI returned empty")

                except Exception as e:
                    st.warning("AI not working")
                    st.code(str(e))

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("### Use Cases")

st.markdown("""
- Monitoring vegetation trends over time  
- Detecting land degradation or recovery  
- Rainfall pattern analysis  
- Climate variability assessment  
""")

st.markdown("### Processing Workflow")

st.markdown("""
1. User selects location and date range  
2. System iterates day-by-day  
3. For each day, a 7-day window of satellite data is used  
4. NDVI, rainfall, and temperature are extracted  
5. Invalid data (NDVI = 0) is skipped  
6. Time-series dataset is created  
7. Trends and statistics are computed  
8. Risk conditions are evaluated  
""")

st.markdown("### Data Source")

st.markdown("""
Data is retrieved using the unified feature pipeline.

Variables used:
- NDVI (vegetation)
- Rainfall
- Temperature

Values are aggregated over a rolling 7-day window to improve reliability.
""")

st.markdown("### Core Logic")

st.code("""
For each day:
Data = last 7 days aggregation

If NDVI == 0 → skip data point

Time-series = daily aggregated values
""")

st.markdown("### Derived Metrics")

st.code("""
NDVI Score = ((mean NDVI + 1) / 2) × 100

Trend Slope = linear regression slope

Volatility = standard deviation of NDVI

Current NDVI = last value in series
""")

st.markdown("### Metric Interpretation")

st.markdown("""
**NDVI Score:** Overall vegetation health  

**Trend Slope:** Direction of vegetation change  
- Positive → improving  
- Negative → degrading  

**Volatility:** Stability of vegetation  
- High → unstable conditions  

**Current NDVI:** Latest vegetation condition  
""")

st.markdown("### Risk Analysis Logic")

st.markdown("""
- NDVI < 0.3 → Drought risk  
- Mean rainfall > 20 → Flood risk  
- NDVI slope < -0.01 → Land degradation  

If no condition is triggered:
→ Stable environmental conditions
""")

st.markdown("### Risk Analysis Logic")

st.markdown("""
- NDVI < 0.3 → Drought risk  
- Mean rainfall > 20 → Flood risk  
- NDVI slope < -0.01 → Land degradation  

If no condition is triggered:
→ Stable environmental conditions
""")

st.markdown("### Interpretation")

st.markdown("""
The system combines vegetation trends and rainfall patterns to detect environmental risks.

- Declining NDVI indicates land degradation  
- High rainfall indicates possible flooding  
- Stable NDVI suggests balanced ecosystem  
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Missing satellite data → filtered using NDVI = 0 condition  
- Cloud interference → reduced via 7-day aggregation  
- Data inconsistency → smoothed using rolling window  
- Invalid inputs → handled via validation checks  
""")

st.markdown("### Limitations")

st.markdown("""
- Only NDVI, rainfall, and temperature are used  
- No AI analysis layer  
- Daily iteration may be slow for long ranges  
- No seasonal or advanced time-series modeling  
""")

st.markdown("### Future Scope")

st.markdown("""
- Add AI-based trend prediction  
- Seasonal and long-term analysis  
- Multi-variable correlation (NDVI vs rainfall)  
- Advanced anomaly detection  
""")

st.markdown("---")
st.caption("Time-Series Analyzer • Environmental Trend Engine")

# =============================
# 🛠️ REPORT / ERROR BUTTON
# =============================
st.markdown("---")
st.subheader("🛠️ Report Issue / Feedback")

feedback = st.text_area("Describe issue or suggestion")

if st.button("Submit Report"):

    if not feedback.strip():
        st.warning("Please enter feedback")
    else:
        # simple logging (you can upgrade later)
        with open("feedback_log.txt", "a") as f:
            f.write(f"{datetime.now()} → {feedback}\n")

        st.success("Report submitted ✅")
