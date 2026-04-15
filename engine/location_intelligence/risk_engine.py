def classify_risks(pred):
    """
    Convert raw predictions into meaningful insights
    """

    heat = pred["heat_score"]
    flood = pred["flood_score"]
    veg = pred["veg_score"]

    return {
        # 🌡 HEAT RISK
        "heat_risk": (
            "Low" if heat < 30 else
            "Moderate" if heat < 60 else
            "High"
        ),

        # 🌊 FLOOD RISK
        "flood_risk": (
            "Low" if flood < 30 else
            "Moderate" if flood < 60 else
            "High"
        ),

        # 🌱 VEGETATION HEALTH
        "vegetation_status": (
            "Poor" if veg < 40 else
            "Moderate" if veg < 70 else
            "Healthy"
        )
    }