# app.py
import os
import html
from flask import Flask, request, send_from_directory
from utils.emission_calculator import predict_emission
from utils.route_optimizer import get_eco_friendly_route
from utils.carbon_footprint import calculate_carbon_footprint

app = Flask(__name__, static_folder="static")

# ---------------- STATIC FILES ------------------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# ---------------- PAGES -------------------------
@app.route("/")
def home():
    return send_from_directory("static_pages", "index.html")

@app.route("/transport")
def transport_page():
    return send_from_directory("static_pages", "transport_form.html")

@app.route("/carbon")
def carbon_page():
    return send_from_directory("static_pages", "carbon_form.html")

# ---------------- TRANSPORT PREDICT -----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        fuel = float(request.form.get("fuel", 7.5))
        speed = float(request.form.get("speed", 50))
        distance = float(request.form.get("distance", 10))
        traffic = int(request.form.get("traffic", 2))
        vehicle_type = request.form.get("vehicle_type", "Car")
        fuel_type = request.form.get("fuel_type", "Petrol")
    except Exception:
        return "Invalid form input", 400

    co2 = predict_emission(
        fuel, speed, distance, traffic,
        vehicle_type=vehicle_type,
        fuel_type=fuel_type
    )

    suggestions = get_eco_friendly_route(distance, traffic, speed)

    if fuel_type.lower() == "electric":
        co2_message = "<b style='color:red;'>Electric vehicles do not produce CO₂ tailpipe emissions.</b>"
    else:
        co2_message = f"<b>{co2} kg CO₂</b>"

    safe = lambda x: html.escape(str(x))
    suggestions_html = "".join(f"<li>{safe(s)}</li>" for s in suggestions)

    result_html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Transport Prediction Result</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="container">
    <h2>Transportation CO₂ Emission Result</h2>

    <p><b>Vehicle type:</b> {safe(vehicle_type)}</p>
    <p><b>Fuel type:</b> {safe(fuel_type)}</p>
    <p><b>Fuel consumption:</b> {safe(fuel)} L/100km</p>
    <p><b>Speed:</b> {safe(speed)} km/h</p>
    <p><b>Distance:</b> {safe(distance)} km</p>
    <p><b>Traffic Level:</b> {safe(traffic)}</p>

    <h3>Total CO₂ Emission: {co2_message}</h3>

    <h3>Eco Route Suggestions:</h3>
    <ul>
      {suggestions_html}
    </ul>

    <a class="back-btn" href="/">Home</a>
    <a class="back-btn" href="/transport">Back</a>
  </div>
</body>
</html>"""

    return result_html



# ---------------- CARBON CALCULATION ------------------
@app.route("/carbon/calc", methods=["POST"])
def carbon_calc():
    try:
        electricity = float(request.form.get("electricity", 300.0))
        lpg = float(request.form.get("lpg", 10.0))
        waste = float(request.form.get("waste", 20.0))
        km = float(request.form.get("km", 200.0))
    except Exception:
        return "Invalid form input", 400

    total, tips = calculate_carbon_footprint(electricity, lpg, waste, km)

    safe = lambda s: html.escape(str(s))
    tips_html = "".join(f"<li>{html.escape(t)}</li>" for t in tips)

    result_html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Carbon Footprint Result</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="container">
    <h2>Your Monthly Carbon Footprint</h2>

    <h3 class="highlight">{safe(total)} kg CO₂</h3>

    <h3>Details</h3>
    <p>Electricity: {safe(electricity)} kWh / month</p>
    <p>LPG: {safe(lpg)} kg / month</p>
    <p>Waste: {safe(waste)} kg / month</p>
    <p>Vehicle distance: {safe(km)} km / month</p>

    <h3>Suggestions</h3>
    <ul>
      {tips_html}
    </ul>

    <a class="back-btn" href="/">Home</a>
    <a class="back-btn" href="/carbon">Back to calculator</a>
  </div>
</body>
</html>"""

    return result_html


if __name__ == "__main__":
    # Use PORT provided by host (Render/Heroku). Default to 5000 locally.
    port = int(os.environ.get("PORT", 5000))
    # Never run debug=True in production
    app.run(host="0.0.0.0", port=port, debug=False)
