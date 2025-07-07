import requests
import json

def get_weather(zip_code):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={zip_code}&count=1&language=en&format=json"
    response = requests.get(geocode_url)
    data = response.json()
    location = data["results"][0]
    lat = location['latitude']
    lon = location['longitude']
    city = location['name']


    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
    response = requests.get(weather_url)
    data = response.json()
    
    current = data.get('current', {})
    daily = data.get('daily', {})
        
    weather_data = {
        'city': city,
        'current_temp': f"{current.get('temperature_2m', 'N/A')}°C",
        'max_temp': f"{daily.get('temperature_2m_max', ['N/A'])[0]}°C" if daily.get('temperature_2m_max') else "N/A",
        'min_temp': f"{daily.get('temperature_2m_min', ['N/A'])[0]}°C" if daily.get('temperature_2m_min') else "N/A",
        'rain_chance': f"{daily.get('precipitation_probability_max', ['N/A'])[0]}%" if daily.get('precipitation_probability_max') else "N/A"
    }


    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi&timezone=auto"
    response = requests.get(aqi_url)
    data = response.json()
        
    current = data.get('current', {})
    aqi = current.get('us_aqi', 'N/A')

    weather_data['aqi'] = aqi

    return f"### Forecast for {weather_data['city']}:\n\n### Current Temperature: {weather_data['current_temp']}\n### Max Temperature: {weather_data['max_temp']}\n### Min Temperature: {weather_data['min_temp']}\n\n### Chance of Rain: {weather_data['rain_chance']}\n### Air Quality Index (AQI): {weather_data['aqi']}\n"

if __name__ == "__main__":
    zip_code = "10016"
    weather_info = get_weather(zip_code)
    print(json.dumps(weather_info, indent=4))