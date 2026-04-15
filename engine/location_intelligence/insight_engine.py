def generate_insights(data, risk):

    insights = []

    if data.get("ndvi", 1) < 0.3:
        insights.append("Low vegetation cover detected")

    if data.get("no2", 0) > 40:
        insights.append("High pollution (NO2 levels)")

    if data.get("temperature", 0) > 305:
        insights.append("High temperature → heat stress")

    if data.get("rainfall", 0) > 50:
        insights.append("Heavy rainfall → flood risk")

    if data.get("ndvi", 1) < 0.3 and data.get("temperature", 0) > 305:
        insights.append("Urban heat island effect likely")

    message = f"⚠️ {risk} environmental risk detected.\n\n"

    message += "Key observations:\n"
    for i in insights:
        message += f"- {i}\n"

    return message