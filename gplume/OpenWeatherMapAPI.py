import requests
from .API_Access import stored_results
from .DateTimeMechanism import api_key_weather

def get_city_name(latitude, longitude, api_key_2):
    # API endpoint for reverse geocoding
    url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&appid={api_key_2}'

    # Send request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract city name from the response
        location_data = response.json()
        city_name = location_data[0]['state']
        return city_name
    else:
        print(f"Failed to retrieve city name for coordinates ({latitude}, {longitude}).")
        return None

def get_weather_data(city_name, api_key_2):
    # API endpoint for weather data
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_2}'

    # Send request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract weather data from the response
        weather_data = response.json()
        return weather_data
    else:
        print(f"Failed to retrieve weather data for city name: {city_name}.")
        return None

# Example usage
api_key_2 =  api_key_weather  # Replace with your OpenWeatherMap API key

# Iterate over the stored_results and get weather data for each location
weather_data = []
for location in stored_results:
    latitude = location['latitude']
    longitude = location['longitude']

    # Get city name based on latitude and longitude
    city_name = get_city_name(latitude, longitude, api_key_2)
    if city_name:
        # Get weather data based on city name
        data = get_weather_data(city_name, api_key_2)
        if data:
            weather_data.append(data)

# Process the weather data as needed
wind_data = []
if len(weather_data) > 0:
    for data in weather_data:
        # Extract the relevant information from the data dictionary
        wind = data['wind']
        wind_speed = wind['speed']
        wind_direction = wind['deg']

        # Store the wind data in a dictionary
        wind_info = {
            'speed': wind_speed,
            'direction': wind_direction
        }
        wind_data.append(wind_info)

# Example access of wind data for a specific location
if len(wind_data) > 0:
    first_location = wind_data[0]
    speed = first_location['speed']
    direction = first_location['direction']
    print(f"Wind Speed: {speed} m/s")
    print(f"Wind Direction: {direction} degrees")
else:
    print("Failed to retrieve wind data. Please check your API key or network connection.")
