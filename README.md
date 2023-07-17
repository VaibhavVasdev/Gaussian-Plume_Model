## Gaussian Plume Model

This repository contains a Python implementation of the Gaussian Plume Model for atmospheric dispersion of contaminants for current time. The code calculates the contaminant concentration at receptor locations based on emission rates and wind conditions. The model assumes a single source and multiple receptors.

### Prerequisites

Before running the code, make sure you have the following dependencies installed:

- `numpy` (Numerical Python) library
- `matplotlib` library for data visualization

You can install the dependencies using `pip`:

```bash
pip install numpy matplotlib
```

### Code Description

The main code file is `gpm.py`, which includes the following components:

1. Contaminant Parameters: Set the parameters related to the contaminant being modeled, such as gravitational acceleration, dynamic viscosity of air, density of the contaminant, diameter of particles, deposition velocity, and molar mass of the contaminant.

2. Source and Receptor Data: Define the locations and characteristics of the emission source and receptors where deposition measurements are made. This includes the number of sources, x-y-z coordinates, labels, and emission rates.

3. `gplume` Function: This function computes the contaminant concentration (in kg/m^3) at a given set of receptor locations using the standard Gaussian plume solution. It takes into account the source characteristics, receptor locations, and wind speed.

4. `forward_atmospheric_dispersion` Function: This function calculates and plots the ground-level contaminant concentration contours based on the Gaussian Plume Model. It takes the wind speed as an input and calls the `gplume` function to calculate the concentrations. The resulting contours are displayed using the `matplotlib` library.

### Usage

To use this code, follow these steps:

1. Ensure that the required dependencies (`numpy` and `matplotlib`) are installed, alongside you have genereated your API keys for both "OpenAQ" and "openweathermap".

2. Modify the contaminant parameters, source data, and receptor data according to your specific scenario i.e in "API_Access.py" input location_ids in line 6 & api_key in line 17. In "OpenWeatherMapAPI.py" input your API key in line 38.

3. Open the `gpm.py` file in a Python environment (e.g., Jupyter Notebook, Python IDE, or command line).

5. Call the `forward_atmospheric_dispersion` function and provide the wind speed (Uwind) as an argument.

6. The code will calculate the contaminant concentration contours and display the plot showing the distribution of concentrations at the receptor locations.

7. If openweathermap API fails, the code assumes a static wind speed and direction, which you can edit in line 71 & 72 of the OpenWeatherMapAPI.py file 

### Output

The code generates a plot showing the contours of ground-level contaminant concentration in mg/m^3. The maximum concentration value is displayed in the plot title. 

### Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to create a pull request or submit an issue on the GitHub repository.

### Contact

For any inquiries or questions, please contact Vaibhav Vasdev, mail to: vaibhavvasdev63@gmail.com  
