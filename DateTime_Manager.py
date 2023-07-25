import requests
from API_Access import stored_results
import datetime

def get_city_name(latitude, longitude, api_key):
    url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        location_data = response.json()
        city_name = location_data[0]['state']
        return city_name
    else:
        print(f"Failed to retrieve city name for coordinates ({latitude}, {longitude}).")
        return None

def get_weather_data(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        dt_timestamp = weather_data['dt']
        return dt_timestamp
    else:
        print(f"Failed to retrieve weather data for city name: {city_name}.")
        return None

# Example usage
api_key = "5c8f85cf6fedfff9a436b78a32060f40"  # Replace with your OpenWeatherMap API key

weather_data = []
for location in stored_results:
    latitude = location['latitude']
    longitude = location['longitude']

    city_name = get_city_name(latitude, longitude, api_key)
    if city_name:
        dt_timestamp = get_weather_data(city_name, api_key)
        if dt_timestamp:
            weather_data.append(dt_timestamp)

if len(weather_data) > 0:
    first_location_dt = weather_data[0]
    print(f"Timestamp (dt): {first_location_dt}")
else:
    print("Failed to retrieve weather data. Please check your API key or network connection.")

def unix_timestamp_to_iso(unix_timestamp):
    try:
        timestamp = int(unix_timestamp)
        # Convert Unix timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)

        # Convert datetime object to ISO 8601 formatted string
        iso_format = dt_object.isoformat()
        return iso_format
    except ValueError:
        return "Invalid Unix timestamp"

# Example usage:
unix_timestamp = first_location_dt
iso_format_time = unix_timestamp_to_iso(unix_timestamp)
print(iso_format_time)