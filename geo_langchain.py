
# 🧠 FIX PATH
# ----------------------------------
import sys, os
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ----------------------------------
# 📦 IMPORTS
# ----------------------------------
from datetime import datetime
import numpy as np
import json
import streamlit as st

from engine.data.unified_features import get_unified_features
from langchain_openai import ChatOpenAI


api_key = st.secrets.get("OPENAI_API_KEY")

# ----------------------------------
# 🤖 LLM SETUP
# ----------------------------------
api_key = st.secrets.get("OPENAI_API_KEY") 

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=api_key
)

# ----------------------------------
# 🧠 MONTH DETECTION
# ----------------------------------
def extract_month(question):
    months = {
        "january":1,"february":2,"march":3,"april":4,
        "may":5,"june":6,"july":7,"august":8,
        "september":9,"october":10,"november":11,"december":12
    }

    q = question.lower()
    for m in months:
        if m in q:
            return months[m]

    return None


# ----------------------------------
# 🧠 HISTORICAL DATES
# ----------------------------------
def get_historical_dates(month, years=3):
    today = datetime.today()

    return [
        datetime(today.year - i, month, 15)
        for i in range(1, years + 1)
    ]


# ----------------------------------
# 🧠 SAFE MEAN
# ----------------------------------
def safe_mean(values):
    clean = [v for v in values if v is not None]
    return round(np.mean(clean), 4) if clean else 0


# ----------------------------------
# 🚀 MAIN AI FUNCTION
# ----------------------------------
def run_ai(lat, lon, question, start_date=None, end_date=None):

    month = extract_month(question)

    # ----------------------------------
    # 🔥 HISTORICAL MODE
    # ----------------------------------
    if month:

        dates = get_historical_dates(month)
        all_data = []

        for d in dates:
            f = get_unified_features(lat, lon, base_date=d)
            all_data.append(f)

        features = {
            "ndvi": safe_mean([x["ndvi"] for x in all_data]),
            "rainfall": safe_mean([x["rainfall"] for x in all_data]),
            "temperature": safe_mean([x["temperature"] for x in all_data]),
            "lst": safe_mean([x["lst"] for x in all_data]),

            # MULTI-POLLUTION
            "pollution": {
                "no2": safe_mean([x["pollution"]["no2"] for x in all_data]),
                "co": safe_mean([x["pollution"]["co"] for x in all_data]),
                "o3": safe_mean([x["pollution"]["o3"] for x in all_data]),
                "so2": safe_mean([x["pollution"]["so2"] for x in all_data]),
            }
        }

        mode = "Historical (multi-year seasonal average)"

    # ----------------------------------
    # 🔥 CURRENT MODE
    # ----------------------------------
    else:

        f = get_unified_features(lat, lon)

        features = {
            "ndvi": f["ndvi"],
            "rainfall": f["rainfall"],
            "temperature": f["temperature"],
            "lst": f["lst"],
            "pollution": f["pollution"]
        }

        mode = "Current (recent 30-day window)"

    # ----------------------------------
    # 🧠 PROMPT (PRO JSON)
    # ----------------------------------
    prompt = f"""
You are a professional environmental intelligence analyst.

Mode: {mode}

Location:
Latitude: {lat}
Longitude: {lon}

Satellite Data:
{features}

User Question:
{question}

Instructions:
- Base analysis strictly on provided data
- Do not assume missing values
- Be concise but insightful
- Consider vegetation, rainfall, temperature, pollution

Return JSON ONLY:
{{
  "summary": "...",
  "risk_level": "Low | Moderate | High",
  "suitability_score": 0-100,
  "key_factors": ["..."],
  "recommendations": ["..."]
}}
"""

    try:
        response = llm.invoke(prompt)
        raw = response.content

        # ----------------------------------
        # 🧠 SAFE JSON PARSE
        # ----------------------------------
        try:
            parsed = json.loads(raw)
            return parsed
        except:
            return {
                "summary": raw,
                "risk_level": "Unknown",
                "suitability_score": 50,
                "key_factors": [],
                "recommendations": []
            }

    except Exception as e:
        return {
            "summary": f"AI Error: {e}",
            "risk_level": "Error",
            "suitability_score": 0,
            "key_factors": [],
            "recommendations": []
        }
    print("API KEY:", api_key)