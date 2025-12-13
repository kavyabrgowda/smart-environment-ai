# utils/emission_calculator.py
import numpy as np

# CO2 emission factors (grams per liter)
CO2_FACTORS = {
    "petrol": 2392,
    "diesel": 2640,
    "cng": 2020,
    "hybrid": 1700,
    "electric": 0
}

# Vehicle multipliers for realistic scaling
VEHICLE_MULTIPLIER = {
    "motorcycle": 0.25,
    "car": 1.0,
    "van": 1.3,
    "truck": 2.5,
    "bus": 3.0
}

def predict_emission(fuel_l_per_100km, avg_speed_kmh, distance_km, traffic_level,
                     vehicle_type="car", fuel_type="petrol"):

    ft = str(fuel_type).lower().strip()
    vt = str(vehicle_type).lower().strip()

    # Electric = zero tailpipe emissions
    if ft == "electric":
        return 0.0

    # Fuel consumed (liters)
    fuel_used = distance_km * (fuel_l_per_100km / 100)

    # Get CO₂ grams per liter
    factor = CO2_FACTORS.get(ft, CO2_FACTORS["petrol"])

    # Base CO₂ (grams → kg)
    co2_kg = (fuel_used * factor) / 1000.0

    # Apply vehicle type multiplier
    vehicle_factor = VEHICLE_MULTIPLIER.get(vt, 1.0)
    co2_kg *= vehicle_factor

    # Traffic adjustment
    traffic_multiplier = 1 + (traffic_level - 2) * 0.05
    co2_kg *= traffic_multiplier

    return round(co2_kg, 3)
