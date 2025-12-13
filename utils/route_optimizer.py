# utils/route_optimizer.py
def get_eco_friendly_route(distance, traffic, speed):
    suggestions = []

    if traffic >= 4:
        suggestions.append("Consider an alternative route with lower congestion.")
    else:
        suggestions.append("Traffic is moderate or low — OK.")

    if speed < 50:
        suggestions.append("Avoid very slow driving; maintain steady speed around 50–60 km/h for better efficiency.")
    elif speed > 80:
        suggestions.append("High speeds increase fuel consumption — reduce speed to 60–80 km/h if safe.")
    else:
        suggestions.append("Speed is within efficient range.")

    if distance > 50:
        suggestions.append("For long trips (>50 km), consider public transport or carpooling.")

    return suggestions
