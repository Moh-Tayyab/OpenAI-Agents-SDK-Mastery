from agents import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()
LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")

@function_tool
def get_user_location() -> str:
    """
    Get the user's current city and country using IP detection.

    Returns:
        str: The user's location in the format "City, Country".
    """
    if not LOCATION_API_KEY:
        return "Location API key is missing."

    url = "https://api.ipgeolocation.io/ipgeo"
    params = {"apiKey": LOCATION_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        city = data.get("city")
        country = data.get("country_name")

        if city and country:
            return f"{city}, {country}"
        elif country:
            return country
        else:
            return "Location could not be determined."

    except requests.RequestException as e:
        return f"Error fetching location: {str(e)}"
