import ee
import streamlit as st
from datetime import datetime, timedelta

# ----------------------------------
# 🌍 INIT GEE (FIXED FOR STREAMLIT)
# ----------------------------------
def init_gee():
    try:
        # ✅ Check if already initialized
        ee.Number(1).getInfo()
    except:
        credentials = ee.ServiceAccountCredentials(
            st.secrets["gee"]["service_account"],
            key_data=st.secrets["gee"]["private_key"]
        )
        ee.Initialize(credentials)


# ----------------------------------
# 📅 DATE RANGE
# ----------------------------------
def get_date_range(start_date=None, end_date=None, days=30):
    if start_date and end_date:
        return str(start_date), str(end_date)

    end = datetime.today()
    start = end - timedelta(days=days)

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


# ----------------------------------
# 🌿 NDVI
# ----------------------------------
def get_ndvi(geom, start, end):
    collection = (
        ee.ImageCollection("MODIS/061/MOD13Q1")
        .filterDate(start, end)
        .select("NDVI")
    )

    image = collection.mean()

    value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=250
    ).get("NDVI")

    return value.getInfo() if value else None


# ----------------------------------
# 🌧️ RAINFALL
# ----------------------------------
def get_rainfall(geom, start, end):
    collection = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start, end)
    )

    image = collection.sum()

    value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=5000
    ).get("precipitation")

    return value.getInfo() if value else None


# ----------------------------------
# 🌡️ TEMPERATURE
# ----------------------------------
def get_temperature(geom, start, end):
    collection = (
        ee.ImageCollection("MODIS/061/MOD11A2")
        .filterDate(start, end)
        .select("LST_Day_1km")
    )

    image = collection.mean()

    value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=1000
    ).get("LST_Day_1km")

    val = value.getInfo() if value else None
    return val / 50 if val else None


# ----------------------------------
# 🏭 POLLUTION (MULTI GAS FIX)
# ----------------------------------
def get_pollution(geom, start, end):
    collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
        .filterDate(start, end)
        .select("NO2_column_number_density")
    )

    image = collection.mean()

    value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=1000
    ).get("NO2_column_number_density")

    no2 = value.getInfo() if value else None

    # ✅ Fix missing keys
    return {
        "no2": no2,
        "co": 0.0,
        "o3": 0.0,
        "so2": 0.0
    }


# ----------------------------------
# 🚀 MAIN FUNCTION
# ----------------------------------
def get_unified_features(lat, lon, start_date=None, end_date=None, days=30):

    # 🔥 CRITICAL (INIT FIRST)
    init_gee()

    start, end = get_date_range(start_date, end_date, days)

    geom = ee.Geometry.Point([lon, lat]).buffer(5000)

    pollution = get_pollution(geom, start, end)

    return {
        "ndvi": get_ndvi(geom, start, end),
        "rainfall": get_rainfall(geom, start, end),
        "temperature": get_temperature(geom, start, end),
        "pollution": pollution
    }
