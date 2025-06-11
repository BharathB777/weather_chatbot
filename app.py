from flask import Flask, request
import requests

app = Flask(__name__)

# Your OpenWeatherMap API key
API_KEY = "62a7efa862edc1c03e49d032122f978c"

# Tamil Nadu and Pondicherry District Coordinates
district_coords = {
    "Pondicherry": {"lat": 11.94, "lon": 79.83},
    "Chennai": {"lat": 13.08, "lon": 80.27},
    "Coimbatore": {"lat": 11.01, "lon": 76.96},
    "Madurai": {"lat": 9.93, "lon": 78.12},
    "Tiruchirappalli": {"lat": 10.79, "lon": 78.70},
    "Salem": {"lat": 11.66, "lon": 78.15},
    "Tirunelveli": {"lat": 8.73, "lon": 77.69},
    # Add more districts if needed
}

# Fetch weather from OpenWeatherMap
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return f"🌦️ Weather: {weather}\n🌡️ Temperature: {temp} °C\n💧 Humidity: {humidity}%"
    else:
        return "❌ Failed to fetch weather data."

# Webhook for WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().title()
    coords = district_coords.get(incoming_msg)

    if coords:
        reply = get_weather(coords['lat'], coords['lon'])
    elif incoming_msg.lower() == "list":
        reply = "📍 Available Districts:\n" + "\n".join(district_coords.keys())
    else:
        reply = "❓ Invalid district. Type *list* to see available options."

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

# Home route (optional)
@app.route("/", methods=["GET"])
def home():
    return "✅ Weather WhatsApp Bot is live."

# Start server
if __name__ == "__main__":
    app.run(port=5000)
