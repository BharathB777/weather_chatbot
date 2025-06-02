def get_weather_data(city):
    if city.lower() == "chennai":
        return {
            "temperature": 34.2,
            "rainfall": 15.6
        }
    else:
        return {
            "temperature": "N/A",
            "rainfall": "N/A"
        }
