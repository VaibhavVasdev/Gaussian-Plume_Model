## Gaussian Plume Model

This repository contains a Python implementation of the Gaussian Plume Model for atmospheric dispersion of contaminants. The code calculates the contaminant concentration at receptor locations based on emission rates and wind conditions. The model assumes a single source and multiple receptors.

### Dependencies

The code requires the following dependencies:

- `numpy` (Numerical Python) library
- `matplotlib` library for data visualization

Make sure these dependencies are installed before running the code.

### Code Description

The main code file is `gpm.py`, which includes the following components:

1. Contaminant Parameters: Set the parameters related to the contaminant being modeled, such as gravitational acceleration, dynamic viscosity of air, density of the contaminant, diameter of particles, deposition velocity, and molar mass of the contaminant.

2. Source and Receptor Data: Define the locations and characteristics of the emission source and receptors where deposition measurements are made. This includes the number of sources, x-y-z coordinates, labels, and emission rates.

3. `gplume` Function: This function computes the contaminant concentration (in kg/m^3) at a given set of receptor locations using the standard Gaussian plume solution. It takes into account the source characteristics, receptor locations, and wind speed.

4. `forward_atmospheric_dispersion` Function: This function calculates and plots the ground-level contaminant concentration contours based on the Gaussian Plume Model. It takes the wind speed as an input and calls the `gplume` function to calculate the concentrations. The resulting contours are displayed using the `matplotlib` library.

### Usage

To use this code, follow these steps:

1. Ensure that the required dependencies (`numpy` and `matplotlib`) are installed.

2. Open the `gpm.py` file in a Python environment (e.g., Jupyter Notebook, Python IDE, or command line).

3. Modify the contaminant parameters, source data, and receptor data according to your specific scenario.

4. Call the `forward_atmospheric_dispersion` function and provide the wind speed (Uwind) as an argument.

5. The code will calculate the contaminant concentration contours and display the plot showing the distribution of concentrations at the receptor locations.

### Output

The code generates a plot showing the contours of ground-level contaminant concentration in mg/m^3. The maximum concentration value is displayed in the plot title. The source locations are marked with red circles, and their corresponding labels are shown next to them.

### Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to create a pull request or submit an issue on the GitHub repository.


---
