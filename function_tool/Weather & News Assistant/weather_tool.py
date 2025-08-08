from agents import function_tool
from dotenv import load_dotenv
import os
import requests

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@function_tool
def get_weather_by_location(location: str) -> dict:
    """
    Fetch current weather data for a given city or location.

    Args:
        location (str): The city or location name.

    Returns:
        dict: A dictionary containing weather information.
    """
    if not OPENWEATHER_API_KEY:
        raise ValueError("OpenWeather API key is not set.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        weather = {
            "location": data.get("name"),
            "temperature_celsius": round(data["main"]["temp"], 1),
            "temperature_fahrenheit": round((data["main"]["temp"] * 9/5) + 32, 1),
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed_mps": data["wind"]["speed"],
            "wind_speed_kmh": round(data["wind"]["speed"] * 3.6, 1),
            "feels_like_celsius": round(data["main"]["feels_like"], 1),
            "pressure": data["main"]["pressure"],
            "visibility_km": round(data.get("visibility", 0) / 1000, 1) if data.get("visibility") else None
        }
        return weather
    except requests.RequestException as e:
        return {"error": f"Error fetching weather: {str(e)}"}
    except (KeyError, TypeError):
        return {"error": "Unexpected response format from weather API."}