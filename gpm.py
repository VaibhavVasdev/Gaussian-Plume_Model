import numpy as np
import folium
from folium import plugins
from API_Access import get_measurement_data

# Call the function to get the measurement data from OpenAQ API
measurement_data = get_measurement_data()

# Process the collected measurement data as needed
recept = {}
recept['n'] = len(measurement_data)  # Number of receptors based on location_ids
recept['x'] = np.zeros(recept['n'])
recept['y'] = np.zeros(recept['n'])
recept['z'] = np.zeros(recept['n'])
recept['label'] = []

for i, data in enumerate(measurement_data):
    # Extract relevant information from the OpenAQ API response
    results = data['results']
    if len(results) > 0:
        # Use the first measurement data for the receptor location
        measurement = results[0]
        latitude = measurement['coordinates']['latitude']
        longitude = measurement['coordinates']['longitude']
        recept['x'][i] = longitude
        recept['y'][i] = latitude
        recept['z'][i] = 0  # Assuming receptors are at ground level
        recept['label'].append(measurement['location'])

# Receptor array analysis
def receptor_array_analysis(receptor_locations):
    # Calculate the centroid of the receptor array
    centroid = np.mean(receptor_locations, axis=0)

    # Determine the distance of each receptor from the centroid
    distances = np.linalg.norm(receptor_locations - centroid, axis=1)

    # Identify the receptor closest to the centroid as the estimated source location
    estimated_source_location = receptor_locations[np.argmin(distances)]

    return estimated_source_location

# Estimate the source location using receptor array analysis
estimated_source_location = receptor_array_analysis(np.column_stack((recept['x'], recept['y'])))

# Create a map object using folium
m = folium.Map(location=[recept['y'].mean(), recept['x'].mean()], zoom_start=10)

# Add markers for receptor locations
for i in range(recept['n']):
    folium.Marker([recept['y'][i], recept['x'][i]], popup=recept['label'][i]).add_to(m)

# Add a marker for the estimated source location
folium.Marker([estimated_source_location[1], estimated_source_location[0]], 
              popup='Estimated Source', icon=folium.Icon(color='red')).add_to(m)

# Save the map as an HTML file
m.save('map.html')