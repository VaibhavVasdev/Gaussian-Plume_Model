import requests
from datetime import datetime, timedelta

def get_measurement_data():
    # Manually enter the parameters
    location_ids = ["", ""]  # Enter as many receptor Ids with "," as a delimiter
    
    # Set the date_from and date_to variables
    date_to = datetime.now()
    date_from = date_to - timedelta(hours=1)
    
    # Format the date strings
    date_to_str = date_to.isoformat()
    date_from_str = date_from.isoformat()

    # Enter your OpenAQ API key
    api_key = " "

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
