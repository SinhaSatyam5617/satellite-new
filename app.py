import streamlit as st

st.set_page_config(layout="wide", page_title="GeoAI Platform")

# -------------------------
# 🔄 RESET BUTTON
# -------------------------
col1, col2 = st.columns([9, 1])
with col2:
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# -------------------------
# HERO SECTION
# -------------------------
st.title(" GeoAI Platform for Climate Intelligence")

st.subheader("AI-Based Satellite Analysis for Climate Change & Environmental Sustainability")

st.markdown("""
An integrated GeoAI system leveraging **satellite imagery, machine learning, and geospatial analytics**  
to monitor environmental changes, predict risks, and support data-driven decision-making.
""")

st.divider()

# -------------------------
# 🎯 PROBLEM STATEMENT
# -------------------------
st.header("Problem Statement")

st.markdown("""
Climate data is vast, complex, and difficult to interpret in real-time.  
Traditional tools require expertise in geospatial systems and lack integrated intelligence.

This platform addresses:
- Fragmented environmental data sources  
- Lack of real-time decision support  
- Difficulty in interpreting satellite data  
""")

st.divider()

# -------------------------
# 💡 APPROACH
# -------------------------
st.header("Our Approach")

st.markdown("""
We combine:

-  Satellite Data (NDVI, rainfall, temperature, pollution)  
-  Machine Learning for prediction  
-  Time-series analysis for trend detection  
-  GeoAI for intelligent insights  

Result: A unified environmental intelligence platform.
""")

st.divider()

# -------------------------
# 🧠 CORE TOOLS
# -------------------------
st.header("Core Tools")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌱 Satellite Vegetation Module")
    st.write("Analyze vegetation health using NDVI from satellite data. Detect deforestation, crop stress, and environmental degradation trends.")

    st.subheader("📊 Time-Series Climate Analysis")
    st.write("Track rainfall, temperature, and vegetation changes over time.  
    Identify trends, anomalies, and seasonal climate patterns.")

    st.subheader("🔍 GeoRisk Time Explorer")
    st.write("Compare satellite data between two dates to highlight environmental changes.  
    Useful for disaster impact and urban expansion analysis.")

with col2:
    st.subheader("⚠️ GeoRisk AI Engine")
    st.write("Predict environmental risks like floods, droughts, and heatwaves.  
    Uses ML models with satellite data for risk scoring and insights.")

    st.subheader("🌫️ Environmental Intelligence")
    st.write("Combine AQI and weather data with satellite insights.  
    Get a complete view of environmental conditions.")

    st.subheader("🤖 GeoAI Analyzer")
    st.write("Query environmental data using AI-driven analysis and insights generation.  
    Supports intelligent interpretation of satellite-derived features.")

st.divider()

# -------------------------
# 🧠 TECH STACK
# -------------------------
st.header(" Technology Stack")

st.markdown("""
- **Frontend:** Streamlit  
- **Geospatial Engine:** Google Earth Engine  
- **Machine Learning:** XGBoost, Regression Models 
- **Data Processing:** NumPy, Pandas  
- **Visualization:** Folium, Charts  
""")

st.divider()

# -------------------------
# 📊 ARCHITECTURE
# -------------------------
st.header("📊 System Architecture")

st.markdown("""
Pipeline:

1. User selects region or inputs query  
2. Satellite data fetched via GEE  
3. Feature extraction (NDVI, rainfall, temperature)  
4. Rules-based AI logic and ML models process data ( We have used ML algorithm in one tool)
5. Results visualized and interpreted  

Designed as a modular and scalable system.
""")

st.divider()

# -------------------------
# 🌍 USE CASES
# -------------------------
st.header("🌍 Use Cases")

st.markdown("""
-  Agriculture monitoring  
-  Flood and drought prediction  
-  Urban expansion tracking  
-  Air quality assessment  
-  Climate change analysis  
""")

st.divider()

# -------------------------
# 📈 IMPACT
# -------------------------
st.header(" Impact")

st.markdown("""
- Enables data-driven environmental decisions  
- Simplifies satellite data interpretation  
- Supports climate research and sustainability  
- Bridges gap between data and decision-making  
""")
