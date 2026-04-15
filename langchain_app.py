# ----------------------------------
# 🌍 STREAMLIT MAIN APP
# ----------------------------------
import streamlit as st

st.set_page_config(
    page_title="GeoAI",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------------
# 🎨 UI STYLING
# ----------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: bold;
    color: #2E86C1;
}
.sub-text {
    font-size: 20px;
    color: #555;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# 🧠 HEADER
# ----------------------------------
st.markdown('<div class="main-title">🌍 GeoAI Platform</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-text">AI-powered satellite intelligence for any location</div>', unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------
# 🚀 FEATURES CARDS
# ----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🌱 Vegetation</h3>
        <p>NDVI & land health analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🌧️ Risk Analysis</h3>
        <p>Flood & environmental risk detection</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🌫️ Pollution</h3>
        <p>Air quality & NO₂ insights</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------
# 🚀 CTA SECTION
# ----------------------------------
st.success("🚀 Click **Analyzer** in sidebar to start")

st.markdown("""
### 💡 Try asking:
- Is this area good for farming?  
- Is flood risk high here?  
- Is pollution dangerous?  
""")