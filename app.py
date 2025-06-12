import os
from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

district_coords = {
    "1": ("Chennai", 13.08, 80.27),
    "2": ("Coimbatore", 11.01, 76.96),
    "3": ("Madurai", 9.93, 78.12),
    "4": ("Tiruchirappalli", 10.79, 78.70),
    "5": ("Salem", 11.66, 78.15),
    "6": ("Tirunelveli", 8.73, 77.69),
    "7": ("Erode", 11.34, 77.72),
    "8": ("Vellore", 12.92, 79.13),
    "9": ("Thoothukudi", 8.78, 78.13),
    "10": ("Thanjavur", 10.79, 79.14),
    "11": ("Dindigul", 10.35, 77.95),
    "12": ("Cuddalore", 11.75, 79.75),
    "13": ("Kanchipuram", 12.84, 79.70),
    "14": ("Nagapattinam", 10.77, 79.84),
    "15": ("Theni", 10.01, 77.47),
    "16": ("Namakkal", 11.22, 78.17),
    "17": ("Virudhunagar", 9.59, 77.95),
    "18": ("Karur", 10.95, 78.08),
    "19": ("Krishnagiri", 12.53, 78.22),
    "20": ("Dharmapuri", 12.13, 78.16),
    "21": ("Sivaganga", 9.84, 78.48),
    "22": ("Ramanathapuram", 9.37, 78.83),
    "23": ("Nilgiris", 11.41, 76.70),
    "24": ("Perambalur", 11.23, 78.88),
    "25": ("Pudukkottai", 10.38, 78.82),
    "26": ("Villupuram", 11.94, 79.48),
    "27": ("Tenkasi", 8.96, 77.32),
    "28": ("Ariyalur", 11.14, 79.07),
    "29": ("Kallakurichi", 11.73, 78.97),
    "30": ("Pondicherry", 11.94, 79.83),
    "31": ("Radar", 0.0, 0.0)
}

radars = {
    "1": "https://mausam.imd.gov.in/Radar/chennai.gif",
    "2": "https://mausam.imd.gov.in/Radar/karaikal.gif"
}

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return f"🌦️ Weather: {weather}\n🌡️ Temp: {temp}°C\n💧 Humidity: {humidity}%"
    else:
        return "❌ Failed to fetch weather data."

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()

    if incoming_msg.lower() == "list":
        menu = "\n".join([f"{k}. {v[0]}" for k, v in district_coords.items()])
        return respond(f"📍 *Select a district number:*\n{menu}")
    
    elif incoming_msg == "31":
        return respond("📡 Choose radar:\n1. Chennai Radar\n2. Karaikal Radar")
    
    elif incoming_msg in radars:
        return respond(f"🛰️ Radar link:\n{radars[incoming_msg]}")

    elif incoming_msg in district_coords:
        name, lat, lon = district_coords[incoming_msg]
        if lat == 0.0:
            return respond("❓ Please choose radar option.")
        return respond(f"*{name}*\n" + get_weather(lat, lon))
    
    else:
        return respond("❌ Invalid input. Type *list* to get all district options.")

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""

@app.route("/")
def home():
    return "✅ Weather Bot with Radar is live."

if __name__ == "__main__":
    app.run(port=5000)
