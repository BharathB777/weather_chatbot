from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "weather" in incoming_msg:
        msg.body("Fetching weather data for you... 🌦️")
        # Later we'll integrate IMD API here
    else:
        msg.body("Hi! Send 'weather' to get live updates 🌤️")

    return str(resp)

if __name__ == "__main__":
    app.run()
