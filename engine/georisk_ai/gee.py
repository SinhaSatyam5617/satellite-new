import ee

# ✅ Your project ID
GEE_PROJECT_ID = "satellite-new-489422"


def init_gee():
    """
    Initialize Google Earth Engine safely
    """
    try:
        # Try normal init
        ee.Initialize(project=GEE_PROJECT_ID)

    except Exception:
        # If not authenticated
        ee.Authenticate()
        ee.Initialize(project=GEE_PROJECT_ID)