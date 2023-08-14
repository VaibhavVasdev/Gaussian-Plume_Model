import requests
from datetime import datetime, timedelta
from .DateTimeMechanism import smallest_date, location_ID, api_key
import numpy as np
from scipy.optimize import lsq_linear
from scipy.special import erfc
import tkinter as tk
from tkinter import simpledialog

def get_measurement_data():
    # Manually enter the parameters
    location_ids = location_ID  
    
    # Set the date_from and date_to variables
    date_to = datetime.fromisoformat(smallest_date)
    date_from = date_to - timedelta(hours=24)
    
    # Format the date strings
    date_to_str = date_to.isoformat()
    date_from_str = date_from.isoformat()


    # Initialize an empty list to store the data
    measurement_data = []

    # Iterate over the location IDs
    for location_id in location_ids:
        # Build the URL with the provided parameters
        url = f"https://api.openaq.org/v2/measurements?location_id={location_id}&parameter=pm25&date_from={date_from_str}&date_to={date_to_str}&limit=10000"

        # Set the Authorization header with the API key
        headers = {"X-API-Key": api_key}

        # Send the GET request to the OpenAQ API
        res = requests.get(url, headers=headers)

        # Check the response status code
        if res.status_code == 200:
            data = res.json()
            # Append the measurement data to the list
            measurement_data.append(data)
        else:
            print(f"Error: Request failed for location ID {location_id} with status code", res.status_code)

    return measurement_data


# Call the function to get the measurement data from OpenAQ API
measurement_data = get_measurement_data()

# Create an empty list to store the relevant information
stored_results = []

# Iterate over the measurement data and store the relevant information
for data in measurement_data:
    # Extract the results
    results = data['results']
    if len(results) > 0:
        for result in results:
            location = result['location']
            latitude = result['coordinates']['latitude']
            longitude = result['coordinates']['longitude']
            parameter = result['parameter']
            value = result['value']
            unit = result['unit']
            stored_results.append({
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'parameter': parameter,
                'value': value,
                'unit': unit
            })
            
print(measurement_data)



#Below is the code for receptor data for Receptor Data used for the calculation of Ermak's solution

measurement_data = get_measurement_data()

recept = {}
recept['n'] = len(measurement_data)
recept['x'] = np.zeros(recept['n'])
recept['y'] = np.zeros(recept['n'])
recept['z'] = np.zeros(recept['n'])
recept['label'] = []
recept['last_value'] = []  # Add a new list to store the last value for each receptor

# Lists to store latitude and longitude
latitude_list = []
longitude_list = []

for i, data in enumerate(measurement_data):
    results = data['results']
    if len(results) > 0:
        last_result = results[-1]  # Get the last result in the list
        latitude = last_result['coordinates']['latitude']
        longitude = last_result['coordinates']['longitude']
        value = last_result['value']  # Get the last value for the measurement location
        recept['x'][i] = longitude
        recept['y'][i] = latitude
        recept['z'][i] = 0
        recept['label'].append(last_result['location'])
        recept['last_value'].append(value)  # Append the last value to the list

        # Append latitude and longitude to their respective lists
        latitude_list.append(latitude)
        longitude_list.append(longitude)
    else:
        # If no results are available, set latitude, longitude, and value to None or any other placeholder value
        latitude = None
        longitude = None
        value = None
        recept['x'][i] = None
        recept['y'][i] = None
        recept['z'][i] = 0
        recept['label'].append(None)
        recept['last_value'].append(None)  # Append None or placeholder value to the list

    # Print the output for each measurement location (receptor)
    print(f"Receptor {i+1}:")
    print(f"  Latitude: {latitude}")
    print(f"  Longitude: {longitude}")
    print(f"  Last Value: {value:.1f}")   # Print the last value for the measurement location with one decimal place
    print(f"  Location: {last_result['location']}")
    print("-----------")

# Convert the 'last_value' list to a NumPy array
last_values_array = np.array(recept['last_value'], dtype=float)

# Convert latitude and longitude lists to NumPy arrays
recept_y = np.array(latitude_list)
recept_x = np.array(longitude_list)

# Save the number of receptors as a variable (Nr)
Nq = recept['n']

# Calculate dynamic z-coordinates based on the total number of receptors (Nr)
recept_z = np.arange(1, Nq + 1)

# Print the array of all the last values
print("\nArray of all the last values:")
print(last_values_array)



#Below is the code for sources data being used to calculate Ermak's solution

source = {}
source['n'] = 4
source['x'] = np.array([285, 310, 900, 1095])
source['y'] = np.array([80, 205, 290, 190])
source['z'] = np.array([15, 35, 15, 15])
source['label'] = [' S1', ' S2', ' S3', ' S4']

def get_custom_source_data():
    num_sources = simpledialog.askinteger("Custom Source Data", "Enter the number of custom sources:")
    if num_sources is None or num_sources <= 0:
        return 0, [], [], []

    custom_source_x = []
    custom_source_y = []
    custom_source_z = []
    for i in range(num_sources):
        x = simpledialog.askfloat("Custom Source Data", f"Enter X-coordinate of Source {i+1}:")
        y = simpledialog.askfloat("Custom Source Data", f"Enter Y-coordinate of Source {i+1}:")
        z = simpledialog.askfloat("Custom Source Data", f"Enter Z-coordinate of Source {i+1}:")
        custom_source_x.append(x)
        custom_source_y.append(y)
        custom_source_z.append(z)

    return num_sources, custom_source_x, custom_source_y, custom_source_z

# Prompt the user for custom source data or use default values
root = tk.Tk()
root.withdraw()

custom_source = simpledialog.askstring("Custom Source Data", "Do you want to provide custom source data? (yes/no):").lower().strip() == "yes"

if custom_source:
    num_sources, custom_source_x, custom_source_y, custom_source_z = get_custom_source_data()

    # Replace default source data with custom data
    source['n'] = num_sources
    source['x'] = np.array(custom_source_x)
    source['y'] = np.array(custom_source_y)
    source['z'] = np.array(custom_source_z)
else:
    # Use default source data
    source['n'] = 4
    source['x'] = np.array([285, 310, 900, 1095])
    source['y'] = np.array([80, 205, 290, 190])
    source['z'] = np.array([15, 35, 15, 15])
    source['label'] = [' S1', ' S2', ' S3', ' S4']


Nd = source['n']
loc_x = source['x']
loc_y = source['y']
loc_z = source['z']
s_label = source['label']
