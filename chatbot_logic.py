from imd_api import get_weather_data

def get_response(message):
    message = message.lower()

    if "temperature" in message and "chennai" in message:
        data = get_weather_data("Chennai")
        return f"The temperature in Chennai is {data['temperature']} °C"
    elif "rainfall" in message and "chennai" in message:
        data = get_weather_data("Chennai")
        return f"Rainfall in Chennai is {data['rainfall']} mm"
    else:
        return "Sorry, I can only tell temperature and rainfall for Chennai for now."
