import requests
import datetime
import dateutil.parser
from dateutil import tz
import tkinter as tk
from tkinter import simpledialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Get user input for location IDs
location_ids_input = simpledialog.askstring("Input", "Enter the OpenAQ Location IDs (separated by commas): ")
location_ID = location_ids_input.split(",")

# Get user input for OpenAQ API key
api_key = simpledialog.askstring("Input", "Enter your OpenAQ API key: ").strip()

# Initialize lists to store longitude and latitude for each location
longitudes = []
latitudes = []

# Initialize a list to store all the ISO 8601 format dates
all_dates = []

# Build URL and fetch data for each location
for location_id in location_ID:
    url = f"https://api.openaq.org/v2/latest?location_id={location_id}&limit=100"

    # Set the Authorization header with the API key
    headers = {"X-API-Key": api_key}

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Convert the response to a JSON object

        # Extract the lastUpdated value for a specific measurement parameter (e.g., "pm")
        parameter_to_extract = "pm25"
        last_updated_value = None

        for measurement in data["results"][0]["measurements"]:
            if measurement["parameter"] == parameter_to_extract:
                last_updated_value = measurement["lastUpdated"]
                break

        if last_updated_value:
            # Helper function to convert date to ISO 8601 format
            def convert_to_iso8601(date_str):
                parsed_date = dateutil.parser.parse(date_str)
                iso8601_date = parsed_date.astimezone(tz.tzutc()).isoformat()
                return iso8601_date

            # Convert the last_updated_value to ISO 8601 format
            iso8601_date = convert_to_iso8601(last_updated_value)

            print(f"Last updated for parameter '{parameter_to_extract}': {iso8601_date}")

            # Append the ISO 8601 format date to the list
            all_dates.append(iso8601_date)

            # Extract longitude and latitude for the current location
            longitude = data["results"][0]["coordinates"]["longitude"]
            latitude = data["results"][0]["coordinates"]["latitude"]
            longitudes.append(longitude)
            latitudes.append(latitude)
        else:
            print(f"No data found for parameter '{parameter_to_extract}'")
    else:
        print("Failed to fetch data. Status code:", response.status_code)

# Find the smallest date using the min function
if all_dates:
    smallest_date = min(all_dates)
    print(f"The smallest date among all locations: {smallest_date}")
else:
    print("No dates found.")

# Get user input for OpenWeatherMap API key
api_key_weather = simpledialog.askstring("Input", "Enter your OpenWeatherMap API key: ")

# Below code is for OpenWeatherMapsAPI's date and time

def get_city_name(latitude, longitude, api_key):
    url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&appid={api_key_weather}'
    response = requests.get(url)

    if response.status_code == 200:
        location_data = response.json()
        city_name = location_data[0]['state']
        return city_name
    else:
        print(f"Failed to retrieve city name for coordinates ({latitude}, {longitude}).")
        return None

def get_weather_data(latitude, longitude, api_key_weather):
    # Get city name based on latitude and longitude
    city_name = get_city_name(latitude, longitude, api_key)

    if city_name:
        # API endpoint for weather data
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_weather}'

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
    else:
        print(f"Failed to retrieve city name for coordinates ({latitude}, {longitude}).")
        return None

# Process weather data for each location
for i in range(len(location_ID)):
    latitude = latitudes[i]
    longitude = longitudes[i]

    # Get weather data based on latitude and longitude
    weather_data = get_weather_data(latitude, longitude, api_key_weather)

    # Process the weather data as needed
    if weather_data:
        # Extract the relevant information from the data dictionary
        wind = weather_data['wind']
        wind_speed = wind['speed']
        wind_direction = wind['deg']
        timestamp = weather_data['dt']  # Extract the Unix timestamp

        # Convert the timestamp to ISO 8601 format
        def convert_to_iso8601(date_str):
            parsed_date = dateutil.parser.parse(date_str)
            iso8601_date = parsed_date.astimezone(tz.tzutc()).isoformat()
            return iso8601_date

        if timestamp:
            # Convert the timestamp to ISO 8601 format
            iso8601_date = convert_to_iso8601(datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"))

            print(f"Date for Location ID '{location_ID[i]}': {iso8601_date}")
        else:
            print(f"Date for Location ID '{location_ID[i]}': Not available")
    else:
        print(f"Failed to retrieve weather data for Location ID '{location_ID[i]}'. Please check your API key or network connection.")
