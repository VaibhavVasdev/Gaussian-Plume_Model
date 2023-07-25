import requests

#Enter location Ids

location_ID = ["221227","8118"]

# Enter your OpenAQ API key
api_Key = "de74a6abd9e7b7bc774ebba2ac998902db6bf85ba45d57da4df7f97afd7a2302"
api_key_1 = api_Key.strip()

#Build URL
for location_id in location_ID:
    url = f"https://api.openaq.org/v2/latest?location_id={location_id}&limit=10000"


url = "https://api.openaq.org/v2/latest/221227?limit=10"

# Set the Authorization header with the API key
headers = {"X-API-Key": api_key_1}

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
        print(f"Last updated for parameter '{parameter_to_extract}': {last_updated_value}")
    else:
        print(f"No data found for parameter '{parameter_to_extract}'")
else:
    print("Failed to fetch data. Status code:", response.status_code)







