import ee
import streamlit as st

def init_gee():
    try:
        ee.Number(1).getInfo()
    except:
        credentials = ee.ServiceAccountCredentials(
            st.secrets["gee"]["service_account"],
            key_data=st.secrets["gee"]["private_key"]
        )
        ee.Initialize(credentials)
