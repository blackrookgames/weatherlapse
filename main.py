import io
import requests
import sys

from pathlib import Path
from PIL import Image

def get_merged_map(z, x, y, api_key):
    # 1. Fetch the Base Map (OpenStreetMap)
    # Note: OSM requires a descriptive User-Agent header
    osm_url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    headers = {"User-Agent": "WeatherApp/1.0 (blackrookgames@gmail.com)"}
    
    osm_response = requests.get(osm_url, headers=headers)
    if osm_response.status_code == 200:
        # Now it should work!
        background = Image.open(io.BytesIO(osm_response.content)).convert("RGBA")
    else:
        print(f"OSM Error: {osm_response.status_code}")
        return

    background = Image.open(io.BytesIO(osm_response.content)).convert("RGBA")

    # 2. Fetch the Weather Layer (OpenWeatherMap)
    owm_url = f"https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png"
    params = {"appid": api_key}
    
    owm_response = requests.get(owm_url, params=params)
    if owm_response.status_code == 200:
        foreground = Image.open(io.BytesIO(owm_response.content)).convert("RGBA")

        # 3. Merge them (Alpha Composite)
        # This properly handles the transparency of the cloud layer
        combined = Image.alpha_composite(background, foreground)
        
        # Save the result
        combined.save("weather_map_composite.png")
        print("Map merged and saved successfully!")
    else:
        print(f"Error: {owm_response.status_code}")

def main():
    # Determine directory
    if len(sys.argv) > 0:
        main_dir_path = Path(sys.argv[0]).resolve().parent
    else: 
        main_dir_path = Path('.').resolve()
    # Get secret
    secret_dir_path = main_dir_path.joinpath("secret")
    secret_key_path = secret_dir_path.joinpath("key")
    with open(secret_key_path, 'r') as _f:
        secret_key = _f.read().strip()
    # Request
    get_merged_map(2, 1, 1, secret_key)
    # Success
    return 0

if __name__ == "__main__":
    sys.exit(main())


#    # URL = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png"
#    URL = "https://tile.openweathermap.org/map/clouds_new/3/3/2.png"
#    params = { 'appid': secret_key }
#    response = requests.get(URL, params=params)
#    if response.status_code == 200:
#        image_path = main_dir_path.joinpath("weather_tile.png")
#        with open(image_path, "wb") as f:
#            f.write(response.content)
#    else:
#        print(f"Error: {response.status_code}")