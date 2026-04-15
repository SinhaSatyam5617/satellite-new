import streamlit as st

st.set_page_config(page_title="Platform Limitations", layout="wide")

st.title("⚠️ Platform Limitations & Performance Notice")

st.markdown("""
This application is deployed on **Streamlit Community Cloud (Free Tier)**.  
While fully functional, certain technical limitations may affect performance.
""")

st.divider()

# -------------------------
# LIMITATIONS
# -------------------------
st.header("Key Technical Constraints")

st.subheader("1️⃣ Cold Start Delay")
st.write("""
The app may take **30–60 seconds to load initially** after inactivity.  
This happens because the server goes to sleep and needs to restart.
""")

st.subheader("2️⃣ Limited Compute Resources")
st.write("""
The platform has limited CPU and memory.  
Heavy operations like:

- Satellite data processing  
- Large geographic areas  
- Long date ranges  

may slow down or fail.
""")

st.subheader("3️⃣ Execution Timeouts")
st.write("""
Long-running tasks such as:

- Time-series analysis  
- AI inference  
- Multi-year computations  

may timeout due to platform limits.
""")

st.subheader("4️⃣ API Constraints")
st.write("""
External APIs like:

- OpenAI (LLM)  
- Google Earth Engine  

have rate limits and request constraints.
""")

st.divider()

# -------------------------
# RECOMMENDATION
# -------------------------
st.header("Best Usage Guidelines")

st.markdown("""
To get optimal performance:

- Use **smaller geographic regions**
- Select **shorter date ranges**
- Avoid repeated rapid queries
- Wait a few seconds between heavy operations
""")


