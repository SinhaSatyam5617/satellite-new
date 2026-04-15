import streamlit as st

st.set_page_config(page_title="Troubleshooting Guide", layout="wide")

st.title(" Troubleshooting & Common Errors")

st.markdown("""
This page helps users understand **common issues** that may occur while using the platform  
and how to resolve them effectively.
""")

st.divider()

# -------------------------
# ERROR 1
# -------------------------
st.subheader(" App Not Loading / Slow Start")

st.write("""
**Cause:**
- Streamlit Cloud goes to sleep after inactivity

**Solution:**
- Wait 30–60 seconds
- Refresh the page
""")

# -------------------------
# ERROR 2
# -------------------------
st.subheader(" No Data Returned")

st.write("""
**Cause:**
- Selected region has no satellite data
- Date range too short or invalid

**Solution:**
- Try a larger area
- Increase date range
- Select a different location
""")

# -------------------------
# ERROR 3
# -------------------------
st.subheader(" AI Not Working")

st.write("""
**Cause:**
- API key not configured correctly
- API rate limit reached

**Solution:**
- Check API key setup
- Wait and retry
""")

# -------------------------
# ERROR 4
# -------------------------
st.subheader(" Timeout / Analysis Failed")

st.write("""
**Cause:**
- Large region or long date range
- Heavy computation

**Solution:**
- Reduce area size
- Use shorter time range
""")

# -------------------------
# ERROR 5
# -------------------------
st.subheader(" Map Not Updating")

st.write("""
**Cause:**
- No coordinates selected
- Session state not updated

**Solution:**
- Click on map again
- Use Reset button
""")

# -------------------------
# ERROR 6
# -------------------------
st.subheader(" Unexpected Results")

st.write("""
**Cause:**
- Missing satellite data
- Environmental variability

**Solution:**
- Try different dates
- Cross-check with other tools
""")

st.divider()

# -------------------------
# BEST PRACTICES
# -------------------------
st.header("💡 Best Practices")

st.markdown("""
- Use **small regions for faster results**
- Avoid running multiple heavy analyses simultaneously
- Wait for processing to complete before new actions
- Use Reset button if app behaves unexpectedly
""")

