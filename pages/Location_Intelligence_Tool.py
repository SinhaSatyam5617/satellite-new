import sys
import os

# -----------------------------
# FIX PATH
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# -----------------------------
# IMPORTS
# -----------------------------
import streamlit as st
from datetime import date

from engine.li_models.predict_li import predict_location_range
import streamlit as st

def show():
    st.title(" Location Intelligence Tool")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title=" Location Intelligence Tool", layout="wide")

st.title("🌍 Location Intelligence System")
st.markdown("""
This module performs multi-day environmental analysis for a given geographic location.  
It aggregates satellite-derived variables over a selected time range and generates predictive scores for heat, flood risk, and vegetation condition.  
The system integrates satellite data processing with rule-based and AI-driven insights.
""")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader(" Enter Location & Time Range")

col1, col2 = st.columns(2)

with col1:
    lat = st.number_input("Latitude", value=13.08, format="%.5f")

with col2:
    lon = st.number_input("Longitude", value=80.27, format="%.5f")

col3, col4 = st.columns(2)

with col3:
    start_date = st.date_input("Start Date", value=date(2023, 12, 1))

with col4:
    end_date = st.date_input("End Date", value=date(2023, 12, 7))

# -----------------------------
# VALIDATION
# -----------------------------
if start_date > end_date:
    st.error("❌ Start date must be before end date")
    st.stop()

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("Analyze Location"):

    with st.spinner("Fetching multi-day satellite data... ⏳"):

        result = predict_location_range(
            lat,
            lon,
            str(start_date),
            str(end_date)
        )

    # -----------------------------
    # ERROR HANDLING
    # -----------------------------
    if "error" in result:
        st.error(result["error"])
        st.stop()

    # -----------------------------
    # LOCATION INFO
    # -----------------------------
    st.subheader("📍 Analysis Window")
    st.json(result["location"])

    # -----------------------------
    # ENVIRONMENT DATA
    # -----------------------------
    st.subheader(" Aggregated Environment Data")
    st.json(result["environment"])

    # -----------------------------
    # MISSING DATA
    # -----------------------------
    if result.get("missing"):
        st.warning(f"⚠️ Missing data for: {', '.join(result['missing'])}")

    # -----------------------------
    # PREDICTIONS
    # -----------------------------
    st.subheader("📊 Predicted Scores")

    preds = result["predictions"]

    col1, col2, col3 = st.columns(3)

    col1.metric(" Heat Score", preds["heat_score"])
    col2.metric(" Flood Score", preds["flood_score"])
    col3.metric(" Vegetation Score", preds["veg_score"])

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.subheader(" Risk Insights")

    insights = result["insights"]

    col1, col2, col3 = st.columns(3)

    col1.success(f" Heat Risk: {insights['heat_risk']}")
    col2.success(f" Flood Risk: {insights['flood_risk']}")
    col3.success(f" Vegetation: {insights['vegetation_status']}")

    st.success(" Multi-day analysis complete")

    st.markdown("### Processing Workflow")

st.markdown("""
- User inputs geographic coordinates (latitude, longitude)  
- A start and end date define the analysis window  
- Multi-day satellite data is retrieved for the selected range  
- Environmental variables are aggregated across the time period  
- Predictive models compute risk scores (heat, flood, vegetation)  
- Results are classified into interpretable insights  
- Output is displayed as structured metrics and summaries  
""")

st.markdown("### Date Handling")

st.markdown("""
The system uses a user-defined time window:

- Start Date → Beginning of analysis  
- End Date → End of analysis  

All satellite data between these dates is processed.  
Instead of single-day analysis, this module computes aggregated values across multiple days.

This improves stability by reducing noise from:
- Cloud cover  
- Missing satellite passes  
- Daily fluctuations  

The result represents an averaged environmental condition over the selected period.
""")

st.markdown("### Data Pipeline")

st.markdown("""
Data is retrieved using:

predict_location_range(lat, lon, start_date, end_date)

The pipeline performs:

- Satellite data extraction across multiple sources  
- Temporal aggregation (mean / combined features)  
- Feature validation and missing data handling  
- Structured output generation for predictions  

The output includes:
- Location metadata  
- Aggregated environmental variables  
- Prediction scores  
- Interpreted insights  
""")

st.markdown("### Environmental Variables")

st.markdown("""
The system aggregates key environmental indicators:

- Vegetation Index (NDVI) → Plant health  
- Moisture / Water Indicators → Flood potential  
- Temperature / Heat Indicators → Thermal conditions  
- Additional derived satellite features  

These variables are averaged over the selected date range to represent overall environmental conditions.
""")

st.markdown("### Prediction Model")

st.markdown("""
Three primary scores are generated:

- Heat Score → Indicates temperature stress  
- Flood Score → Indicates water accumulation risk  
- Vegetation Score → Indicates plant health  

Each score is computed using aggregated satellite features and predefined model logic.

Scores are normalized to allow comparison across locations.
""")

st.markdown("### Classification Logic")

st.markdown("""
Prediction scores are interpreted into human-readable insights:

- Heat Risk → Low / Moderate / High  
- Flood Risk → Low / Moderate / High  
- Vegetation Status → Healthy / Moderate / Poor  

This simplifies raw numerical outputs into actionable insights.
""")

st.markdown("### Output Structure")

st.markdown("""
The system returns structured results:

- Location → Coordinates and metadata  
- Environment → Aggregated feature values  
- Predictions → Heat, flood, vegetation scores  
- Insights → Interpreted risk levels  

Missing data is explicitly flagged to ensure transparency.
""")

st.markdown("### Use Cases")

st.markdown("""
- Multi-day environmental monitoring  
- Flood risk assessment for a region  
- Heat stress evaluation  
- Agricultural suitability analysis  
- Comparing environmental conditions across time ranges  
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Invalid date range:
  → Execution stopped with validation  

- Missing satellite data:
  → Flagged and displayed to user  

- Data variability:
  → Reduced using multi-day averaging  

- Partial data availability:
  → Missing variables listed explicitly  
""")

st.markdown("### Limitations")

st.markdown("""
- Uses aggregated averages (no daily breakdown)  
- Model logic is predefined (not adaptive ML)  
- Does not include all environmental variables (e.g., air pollution)  
- Accuracy depends on satellite data availability  
""")

st.markdown("### Future Scope")

st.markdown("""
- Time-series visualization (daily trends)  
- Integration with rainfall (CHIRPS) and weather (ERA5)  
- Pollution analysis (Sentinel-5P)  
- AI-based predictive modeling  
- Region comparison across multiple locations  
""")
