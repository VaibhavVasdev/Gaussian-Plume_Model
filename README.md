# GPlume

This repository contains a Python implementation of the Gaussian Plume Model for atmospheric dispersion of contaminants (PM2.5), along with an inverse modeling approach to estimate emission rates from receptor measurements. The model calculates the contaminant concentration at receptor locations based on emission rates and wind conditions. It assumes 4 sources, which can be customized according to the code that generates an input box. This code works for multiple sources and multiple receptors.


## Code Description

The main code file `gpm.py` includes the following components:

1. Contaminant Parameters: Set the parameters related to the contaminant being modeled, such as gravitational acceleration, dynamic viscosity of air, density of the contaminant, diameter of particles, deposition velocity, and molar mass of the contaminant.

2. Source and Receptor Data: Define the locations and characteristics of the emission source and receptors where deposition measurements are made. This includes the number of sources, x-y-z coordinates, labels, and emission rates.

3. `gplume` Function: This function computes the contaminant concentration (in kg/m^3) at a given set of receptor locations using the standard Gaussian plume solution. It takes into account the source characteristics, receptor locations, and wind speed.

4. `forward_atmospheric_dispersion` Function: This function calculates and plots the ground-level contaminant concentration contours based on the Gaussian Plume Model. It takes the wind speed as an input and calls the `gplume` function to calculate the concentrations. The resulting contours are displayed using the `matplotlib` library.



The `inverse.py` file introduces an inverse modeling approach to estimate emission rates from observed contaminant concentrations at receptor locations. The key components in this file are:

1. `ermak` Function: This function computes the contaminant concentration at receptor locations using the Ermak dispersion model. It takes into account the emission rates, wind speed, and other parameters.

2. Objective Function: The `objective_function` calculates the difference between predicted and observed contaminant concentrations based on the Ermak model. It sets up an optimization problem to find the optimal emission rates that minimize this difference.

3. Optimization: The `minimize` function from the `scipy.optimize` module is used to find the optimal emission rates that best fit the observed receptor measurements.


## Installing

Install and update from PyPI using an installer such as pip:

```python
$ pip install -U gplume
```

## A Simple Example

```python
# Compute and plot forward modeling
from gplume import gpm
```

```python
# Compute and plot inverse modeling
from gplume import inverse
```

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to create a pull request or submit an issue on the GitHub repository. https://github.com/VaibhavVasdev/Gaussian-Plume_Model

## Contact

For any inquiries or questions, please contact Vaibhav Vasdev at vaibhavvasdev63@gmail.com.