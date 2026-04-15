import streamlit as st
from openai import OpenAI

# Load key safely
api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)