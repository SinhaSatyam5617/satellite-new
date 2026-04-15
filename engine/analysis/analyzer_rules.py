def analyze_all(data):

    ndvi = data.get("ndvi", 0)
    rain = data.get("rainfall", 0)
    temp = data.get("temperature", 0)
    pollution = data.get("pollution", {})

    summary = {}

    # vegetation
    if ndvi > 0.6:
        summary["vegetation"] = "Dense"
    elif ndvi > 0.3:
        summary["vegetation"] = "Moderate"
    else:
        summary["vegetation"] = "Low"

    # rainfall
    if rain > 200:
        summary["rainfall"] = "Heavy (Flood Risk)"
    elif rain > 50:
        summary["rainfall"] = "Moderate"
    else:
        summary["rainfall"] = "Low"

    # temperature
    if temp > 35:
        summary["temperature"] = "High"
    else:
        summary["temperature"] = "Normal"

    # pollution
    no2 = pollution.get("no2", 0)
    if no2 > 0.0005:
        summary["pollution"] = "High"
    else:
        summary["pollution"] = "Low"

    return summary