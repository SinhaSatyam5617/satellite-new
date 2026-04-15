import ee

def init_gee():
    try:
        ee.Initialize(project='satellite-new-489422')
        print("✅ GEE Initialized")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project='satellite-new-489422')
        print("🔐 GEE Authenticated")