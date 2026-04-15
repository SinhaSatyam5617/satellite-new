
# draw_page.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import streamlit as st

def show():
    st.title("🧭 Region Selection Tool")

st.set_page_config(layout="wide")
st.title("Region Selection Tool")
st.markdown("""
This module allows users to define a custom geographic region by drawing polygons or rectangles directly on the map.  
It captures precise spatial coordinates that can be used for downstream satellite-based analysis.  
The selected geometry is stored and passed to other modules for region-level processing.
""")

# Base map
m = folium.Map(location=[26.8467, 80.9462], zoom_start=12)

# Draw tool
Draw(
    export=True,
    draw_options={
        "polyline": False,
        "polygon": True,
        "rectangle": True,
        "circle": False,  # disable for now (clean)
        "marker": False,
    }
).add_to(m)

map_data = st_folium(m, height=500, width=900)

# Handle drawing
if map_data and map_data.get("last_active_drawing"):

    geom = map_data["last_active_drawing"]["geometry"]
    geom_type = geom["type"]

    if geom_type == "Polygon":
        coords = geom["coordinates"][0]

        if len(coords) < 3:
            st.error("❌ Invalid polygon")
        else:
            st.session_state.coords = coords
            st.success("✅ Coordinates saved!")
            st.write(coords)

# Info
if "coords" in st.session_state:
    st.info("👉 Go to 'Analyze Page' → ready 🚀")

st.markdown("### Use Cases")

st.markdown("""
- Selecting agricultural fields for analysis  
- Defining custom regions instead of single-point analysis  
- Urban area mapping and land boundary selection  
- Preparing regions for satellite-based data extraction  
""")

st.markdown("### Processing Workflow")

st.markdown("""
1. User interacts with the map interface  
2. Drawing tool is used to create:
   - Polygon  
   - Rectangle  
3. Geometry is captured from the map  
4. Coordinates are extracted from the shape  
5. Coordinates are stored in session state  
6. Stored region is used in analysis modules  
""")

st.markdown("### Geometry Extraction")

st.code("""
Geometry Type: Polygon

Coordinates Format:
[
  [lon, lat],
  [lon, lat],
  ...
]
""")

st.markdown("### Validation Logic")

st.markdown("""
- Minimum 3 coordinate points required for polygon  
- Invalid shapes are rejected  
- Only polygon and rectangle drawing is allowed  
""")

st.markdown("### Data Flow")

st.markdown("""
Selected coordinates are stored using session state:

st.session_state.coords

This allows:
- Sharing geometry across pages  
- Passing region into analysis pipelines  
""")

st.markdown("### Importance")

st.markdown("""
Point-based analysis provides limited insight.

This tool enables:
- Area-based analysis  
- More accurate satellite aggregation  
- Real-world region mapping  
""")

st.markdown("### Limitations")

st.markdown("""
- Circle drawing is disabled  
- Only polygon and rectangle supported  
- No area calculation implemented  
- No multi-shape support  
""")

st.markdown("### Challenges & Handling")

st.markdown("""
- Invalid shapes → blocked using coordinate length check  
- User errors → feedback messages shown  
- Geometry inconsistencies → simplified via polygon-only mode  
""")

st.markdown("### Future Scope")

st.markdown("""
- Add circle and freehand drawing  
- Compute area (sq km)  
- Support multiple shapes  
- Direct integration with satellite analysis engine  
""")

st.markdown("---")
st.caption("Region Selection Tool • Spatial Input Module")