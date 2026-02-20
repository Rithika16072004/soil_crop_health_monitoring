def recommend_irrigation(soil_moisture, temperature):
    """Simple rule-based irrigation recommendation"""
    if soil_moisture < 30:
        return "🚰 Irrigation needed — soil moisture too low."
    elif soil_moisture > 70:
        return "✅ Soil moisture optimal. No irrigation required."
    else:
        return "💧 Soil moisture moderate — monitor regularly."


def recommend_fertilizer(ph, N, P, K):
    """Rule-based fertilizer recommendation considering NPK and pH"""
    msg = []

    # pH condition
    if ph < 5.5:
        msg.append("Soil too acidic — add lime or organic matter.")
    elif ph > 7.5:
        msg.append("Soil too alkaline — add compost or sulfur.")
    else:
        msg.append("Soil pH is balanced.")

    # Nutrient balance
    if N < 40:
        msg.append("Low Nitrogen — apply urea or compost.")
    if P < 40:
        msg.append("Low Phosphorus — use DAP fertilizer.")
    if K < 40:
        msg.append("Low Potassium — apply potash fertilizer.")

    if len(msg) == 1:
        msg.append("NPK levels are adequate.")

    return " | ".join(msg)


def recommend_crop(temperature, humidity, rainfall):
    """Recommend crops based on general climate and soil conditions"""
    if 20 <= temperature <= 30 and 100 <= rainfall <= 200 and 60 <= humidity <= 80:
        return "🌾 Ideal for rice, wheat, or maize."
    elif temperature > 30 and rainfall < 100:
        return "🌻 Suitable for maize, sunflower, or cotton."
    elif rainfall < 80 and temperature < 25:
        return "🥔 Try potato, chickpea, or pulses."
    else:
        return "🌿 Moderate conditions — suitable for multiple crops."