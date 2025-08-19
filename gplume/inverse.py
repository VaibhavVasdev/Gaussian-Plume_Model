# Import necessary libraries and custom modules
import numpy as np
from scipy.optimize import minimize
from scipy.special import erfc
from .DateTimeMechanism import location_ID
from .API_Access import Nq, Nd, recept_z, recept_y, recept_x, last_values_array

# Define the Ermak-Mulvihill atmospheric dispersion model function
def ermak(x, y, z, H, U, Wset, Wdep):
    Umin = 0.0
    ay = 0.34
    by = 0.82
    az = 0.275
    bz = 0.82
    sigmay = ay * np.abs(x) ** by * (x > 0)
    sigmaz = az * np.abs(x) ** bz * (x > 0)
    Kz = 0.5 * az * bz * U * np.abs(x) ** (bz - 1) * (x > 0)

    # Calculate the plume concentration using the Ermak-Mulvihill model
    if U < Umin:
        Q = np.zeros_like(z)
    else:
        Wo = Wdep - 0.5 * Wset
        Q = (2 * np.pi * U * sigmay * sigmaz) * np.exp(-0.5 * y ** 2 / sigmay ** 2) * \
            np.exp(-0.5 * Wset * (z - H) / Kz - Wset ** 2 * sigmaz ** 2 / 8. / Kz ** 2) * \
            (np.exp(-0.5 * (z - H) ** 2 / sigmaz ** 2) +
             np.exp(-0.5 * (z + H) ** 2 / sigmaz ** 2) - np.sqrt(2 * np.pi) * Wo * sigmaz / Kz * \
             np.exp(Wo * (z + H) / Kz + 0.5 * Wo ** 2 * sigmaz ** 2 / Kz ** 2) * \
             erfc(Wo * sigmaz / np.sqrt(2) / Kz + (z + H) / np.sqrt(2) / sigmaz))
        Q[np.isnan(Q) | np.isinf(Q)] = 0
    return Q

# Define variables related to the dispersion model and measurements
Ns = Nd
Nr =  Nq  # Replace this with the actual number of receptors
Uwind = 5.0
dtime = 30 * 24 * 60 * 60
recept_PM25 = np.array(last_values_array)  # Replace this with actual measurements

# Define physical constants for dispersion calculations
grav = 9.8
mu = 1.8e-5
rho = 1000
R = 1e-6
Wdep = 0.0062
Wset = 2 * rho * grav * R**2 / (9 * mu)

# Extract receptor locations from the API
recept_xt = np.array(recept_x)  # Replace with actual receptor longitudes
recept_yt = np.array(recept_y)  # Replace with actual receptor latitudes
recept_zt = np.array(recept_z)  # Replace with actual receptor z-coordinates

# Define the objective function for optimization
def objective_function(emission_rates):
    Glsq = np.zeros((Nr, Ns))
    for is_ in range(Ns):
        Glsq[:, is_] = ermak(recept_xt - 150, recept_yt - 0, recept_zt, 0, Uwind, Wset, Wdep).T

    # Calculate the predicted PM2.5 concentrations
    dia = 0.162
    A = np.pi * (dia / 2) ** 2
    rhs = recept_PM25 / (A * dtime * Wdep)

    # Calculate the difference between predicted and observed PM2.5 concentrations
    predicted_PM25 = np.dot(Glsq, emission_rates)
    diff = predicted_PM25 - rhs
    return np.sum(diff**2)

# Generate random initial guesses for the emission rates
np.random.seed(123)  # For reproducibility
initial_guesses = np.random.rand(Ns)

# Use scipy's minimize function to optimize the emission rates
result = minimize(objective_function, initial_guesses, constraints=None)

# Extract the optimal emission rates from the optimization result
optimal_emission_rates = result.x

# Print the optimal emission rates
print("Optimal Emission Rates:")
print(optimal_emission_rates)
