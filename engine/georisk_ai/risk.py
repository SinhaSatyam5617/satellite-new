def normalize(value, min_val=-1, max_val=1):
    """Normalize value safely to 0–1 range"""
    try:
        norm = (value - min_val) / (max_val - min_val)
        return max(0, min(1, norm))  # ✅ clamp between 0–1
    except:
        return 0


def calculate_risk(ndvi, ndwi, ndbi):
    # ✅ Handle None safely
    ndvi = ndvi if ndvi is not None else 0
    ndwi = ndwi if ndwi is not None else 0
    ndbi = ndbi if ndbi is not None else 0

    # ✅ Normalize values
    ndvi_n = normalize(ndvi)
    ndwi_n = normalize(ndwi)
    ndbi_n = normalize(ndbi)

    # ✅ Risk components
    vegetation_risk = 1 - ndvi_n
    water_risk = 1 - ndwi_n
    urban_risk = ndbi_n

    # ✅ Weighted score
    risk_score = (
        vegetation_risk * 0.4 +
        urban_risk * 0.4 +
        water_risk * 0.2
    ) * 100

    return round(risk_score, 2)


def risk_label(score):
    if score >= 70:
        return "🔴 High Risk"
    elif score >= 40:
        return "🟡 Moderate Risk"
    else:
        return "🟢 Low Risk"


def generate_insight(ndvi, ndwi, ndbi, risk):
    # ✅ Handle None
    ndvi = ndvi if ndvi is not None else 0
    ndwi = ndwi if ndwi is not None else 0
    ndbi = ndbi if ndbi is not None else 0

    insights = []

    # 🌱 Vegetation
    if ndvi < 0.2:
        insights.append("very low vegetation")
    elif ndvi < 0.5:
        insights.append("moderate vegetation")
    else:
        insights.append("healthy vegetation")

    # 🏙 Urbanization
    if ndbi > 0.3:
        insights.append("high urban development")
    elif ndbi > 0:
        insights.append("moderate built-up area")

    # 💧 Water
    if ndwi < 0:
        insights.append("low water presence")
    elif ndwi > 0.3:
        insights.append("good water availability")

    # Combine safely
    base = ", ".join(insights) if insights else "mixed environmental conditions"

    # Final message
    if risk >= 70:
        return f"{base}. Overall environmental risk is HIGH."
    elif risk >= 40:
        return f"{base}. Area shows MODERATE environmental stress."
    else:
        return f"{base}. Area is environmentally STABLE."