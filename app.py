import streamlit as st

st.set_page_config(layout="wide", page_title="GeoAI Platform")

# -------------------------
# HERO SECTION
# -------------------------
st.title("AI-Based Satellite Imagery for  Climate Change & Environmental Sustainability")

st.markdown("""
An integrated GeoAI platform that uses **satellite imagery, machine learning, and AI (LLM)**  
to analyze environmental changes, predict risks, and support sustainable decision-making.

 *Ask anything about Earth. Get AI-powered answers from satellite data.*
""")

st.divider()

# -------------------------
# TOOLS SECTION
# -------------------------
st.header(" Core Tools")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌱 Satellite Vegetation Module")
    st.write("""
    Analyze vegetation health using NDVI from satellite data.  
    Detect deforestation, crop stress, and environmental degradation trends.
    """)

    st.subheader("📊 Time-Series Climate Analysis")
    st.write("""
    Track rainfall, temperature, and vegetation changes over time.  
    Identify trends, anomalies, and seasonal climate patterns.
    """)

    st.subheader("🔍 GeoRisk Time Explorer")
    st.write("""
    Compare satellite data between two dates to highlight environmental changes.  
    Useful for disaster impact and urban expansion analysis. Though we are looking through NDVI values here in this tool
    """)

with col2:
    st.subheader("⚠️ GeoRisk AI Engine")
    st.write("""
    Predict environmental risks like floods, droughts, and heatwaves.  
    Uses ML models with satellite data for risk scoring and insights.
    """)

    st.subheader("🌫️ Environmental Intelligence")
    st.write("""
    Combine AQI and weather data with satellite insights.  
    Get a complete view of environmental conditions.
    """)

    st.subheader("🤖 GeoAI Analyzer")
    st.write("""
    Ask natural language queries like:  
    *“Rainfall trend in Chennai between Dec 1–10”*  
    Get AI-powered analysis and recommendations.
    """)

st.divider()

# -------------------------
# HOW TO USE
# -------------------------
st.header(" How to Use")

st.markdown("""
1. **Select a tool** from the sidebar  
2. **Choose location and range of dates(if given)**  
3. Click **Analyze / Generate Insights**  
4. View **data, charts, and AI insights**
""")

st.divider()

# -------------------------
# LLM USAGE
# -------------------------
st.header(" AI (LLM) Integration")

st.markdown("""
This platform uses **OpenAI API** to:

- Understand user queries  
- Extract location, date, and parameters  
- Generate insights and reports  

 **Setup API Key:**
""")

st.code('export OPENAI_API_KEY="your_api_key_here"', language='bash') - Though we have already done this part

st.markdown("""
 Best Practice:
- Use AI for **analysis, not raw data fetching**  
- Always provide **clean structured data**  
""")

st.divider()

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
###  Why This Platform Matters

- Supports climate research, make easy derivations  
- Converts complex satellite data into simple insights  
- Can help study environmental risks thoroughly  
- Bridges gap between data & decision-making  
""")
