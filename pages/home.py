import streamlit as st

def show():

    # -------------------------
    # HERO SECTION
    # -------------------------
    st.title("🌍 TerraMind AI")

    st.markdown("""
    ### AI-Powered Satellite Intelligence Platform  

    Analyze **climate change**, **environmental patterns**, and **geospatial data**
    using satellite imagery, AI models, and real-time analytics.
    """)

    st.divider()

    # -------------------------
    # FEATURE CARDS
    # -------------------------
    st.subheader("🚀 Platform Capabilities")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="padding:20px;border-radius:15px;background:#111827;">
        <h4>📡 Satellite Intelligence</h4>
        <p>Analyze NDVI, vegetation, land surface changes using satellite data.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding:20px;border-radius:15px;background:#111827;">
        <h4>🤖 AI Analysis</h4>
        <p>Predict weather, analyze trends, and generate AI-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding:20px;border-radius:15px;background:#111827;">
        <h4>⚠️ Risk Detection</h4>
        <p>Flood, drought, and environmental risk monitoring.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # -------------------------
    # MODULE OVERVIEW
    # -------------------------
    st.subheader("🧠 Available Tools")

    tools = [
        "📊 Data Intelligence Tool",
        "🧭 Region Selection Tool",
        "🌦 Weather Intelligence Module",
        "📈 Time-Series Analyzer",
        "🌫 Atmospheric Intelligence Module",
        "🧠 Geo AI Analyzer",
        "🌱 Satellite Vegetation Module",
        "⚠️ Geo-Risk Time Explorer",
        "📍 Location Intelligence Tool"
    ]

    for tool in tools:
        st.write(f"✔ {tool}")

    st.divider()

    # -------------------------
    # CTA SECTION
    # -------------------------
    st.subheader("⚡ Start Exploring")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Open Data Intelligence Tool"):
            st.session_state.page = "Data Intelligence Tool"

    with col2:
        if st.button("🤖 Explore AI Modules"):
            st.session_state.page = "AI Modules"

    st.divider()

    # -------------------------
    # GEO AI QUERY (KILLER FEATURE PLACEHOLDER)
    # -------------------------
    st.subheader("💬 GeoAI Assistant")

    query = st.text_input("Ask anything about climate, satellite, or environment")

    if query:
        st.info(f"Analyzing: {query}")
        st.success("AI Insight: (connect your OpenAI + GEE here)")