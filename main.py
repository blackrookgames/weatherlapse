import requests

def get_weather(city, api_key):
    # Base URL for Current Weather Data
    url = "http://api.openweathermap.org/data/2.5/weather"

    https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}

    # Parameters: q=city, appid=your_key, units=metric (for Celsius)
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' 
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        print(f"Weather in {city}: {temp}°C, {desc}")
    else:
        print(f"Error: {response.status_code}")

# Use your actual API key here
get_weather("London", "YOUR_API_KEY")
