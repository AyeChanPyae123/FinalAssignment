import requests
import pandas as pd
import sqlite3

# OpenWeatherMap API settings
API_KEY = "8909c9622810eaf68b2e6d9620dd66d7"  # Your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of cities to fetch weather data for
CITIES = ["London", "New York", "Tokyo", "Delhi", "Paris"]

def fetch_weather(city):
    """Fetch weather data for a city from OpenWeatherMap API."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Extract relevant weather data
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        # Handle API errors
        print(f"Failed to fetch data for {city}. HTTP Status Code: {response.status_code}")
        return None

# Fetch weather data for all cities
weather_data = [fetch_weather(city) for city in CITIES]
weather_data = [data for data in weather_data if data is not None]

# Convert to DataFrame
df = pd.DataFrame(weather_data)

# Check if DataFrame is empty before attempting to save to database
if not df.empty:
    # Save to SQLite database
    conn = sqlite3.connect("weather_data.db")
    df.to_sql("weather", conn, if_exists="replace", index=False)
    conn.close()
    print("Weather data saved to SQLite database.")
else:
    print("No data available to save to the database.")
