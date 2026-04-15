import streamlit as st

def render_navigation():

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # -------------------------
    # TOPBAR (MAIN)
    # -------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "Home"

    with col2:
        if st.button("📊 Data Intelligence Tool"):
            st.session_state.page = "Data Intelligence Tool"

    with col3:
        if st.button("🧭 Region Selection Tool"):
            st.session_state.page = "Region Selection Tool"

    with col4:
        if st.button("🤖 AI Modules"):
            st.session_state.page = "AI Modules"

    with col5:
        if st.button("🛰 Satellite Modules"):
            st.session_state.page = "Satellite Modules"

    st.divider()

    # -------------------------
    # ROUTING
    # -------------------------
    page = st.session_state.page

    if page == "Home":
        from pages.home import show
        show()

    elif page == "Data Intelligence Tool":
        from pages.data import show
        show()

    elif page == "Region Selection Tool":
        from pages.region import show
        show()

    elif page == "AI Modules":
        render_ai_modules()

    elif page == "Satellite Modules":
        render_satellite_modules()


# -------------------------
# AI MODULES (YOUR EXACT NAMES)
# -------------------------
def render_ai_modules():
    st.subheader("🤖 AI Intelligence Modules")

    choice = st.selectbox("Select Module", [
        "Atmospheric Intelligence Module",
        "Geo AI Analyzer",
        "Time-Series Analyzer",
        "Weather Intelligence Module"
    ])

    if choice == "Atmospheric Intelligence Module":
        from pages.atmospheric import show
        show()

    elif choice == "Geo AI Analyzer":
        from pages.ai_geo import show
        show()

    elif choice == "Time-Series Analyzer":
        from pages.ai_timeseries import show
        show()

    elif choice == "Weather Intelligence Module":
        from pages.ai_weather import show
        show()


# -------------------------
# SATELLITE MODULES
# -------------------------
def render_satellite_modules():
    st.subheader("🛰 Satellite Intelligence")

    choice = st.selectbox("Select Module", [
        "Satellite Vegetation Module",
        "Geo-Risk Time Explorer",
        "Location Intelligence Tool"
    ])

    if choice == "Satellite Vegetation Module":
        from pages.vegetation import show
        show()

    elif choice == "Geo-Risk Time Explorer":
        from pages.risk import show
        show()

    elif choice == "Location Intelligence Tool":
        from pages.location_intelligence import show
        show()