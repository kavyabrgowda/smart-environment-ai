# utils/carbon_footprint.py
def calculate_carbon_footprint(electricity_kwh, lpg_kg, waste_kg, vehicle_km):
    """
    Monthly footprint approximation (kg CO2 per month)
    Emission factors are approximate and can be adjusted.
    """
    EF_ELECTRICITY = 0.82      # kg CO2 per kWh
    EF_LPG = 2.983             # kg CO2 per kg LPG
    EF_WASTE = 1.2             # kg CO2 per kg waste
    EF_VEHICLE = 0.271         # kg CO2 per km

    electricity_emission = electricity_kwh * EF_ELECTRICITY
    lpg_emission = lpg_kg * EF_LPG
    waste_emission = waste_kg * EF_WASTE
    transport_emission = vehicle_km * EF_VEHICLE

    total = electricity_emission + lpg_emission + waste_emission + transport_emission

    tips = []
    if electricity_kwh > 300:
        tips.append("Reduce electricity usage: use LED bulbs and energy-efficient appliances.")
    if lpg_kg > 20:
        tips.append("Plan meals and reduce LPG usage; consider induction cooking.")
    if waste_kg > 30:
        tips.append("Segregate waste and compost organic waste, recycle plastic/paper.")
    if vehicle_km > 800:
        tips.append("Use public transport or carpool to cut travel emissions.")
    if not tips:
        tips.append("Good job — your footprint looks reasonable. Keep it up!")

    return round(total, 2), tips
