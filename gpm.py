import numpy as np
import matplotlib.pyplot as plt
from API_Access import get_measurement_data

# Contaminant parameters (PM2.5):
grav = 9.8           # gravitational acceleration (m/s^2)
mu = 1.8e-5          # dynamic viscosity of air (kg/m.s)
rho = 1000           # density of PM2.5 (kg/m^3)
R = 1e-6             # diameter of PM2.5 particles (m)
Wdep = 0.0062        # PM2.5 deposition velocity (m/s), in the range [5e-4,1e-2]
Wset = 2 * rho * grav * R**2 / (9 * mu)  # settling velocity (m/s): Stokes law

# Other parameters:
dia = 0.162          # receptor diameter (m)
A = np.pi * (dia/2)**2  # receptor area (m^2)

# Stack emission source data:
source = {}
source['n'] = 4                        # # of sources
source['x'] = np.array([285, 310, 900, 1095])  # x-location (m)
source['y'] = np.array([80, 205, 290, 190])     # y-location (m)
source['z'] = np.array([15, 35, 15, 15])         # height (m)
source['label'] = [' S1', ' S2', ' S3', ' S4']
tpy2kgps = 1.0 / 31536                 # conversion factor (tonne/yr to kg/s)
source['Q'] = np.array([35, 80, 5, 5]) * tpy2kgps  # emission rate (kg/s)

# Call the function to get the measurement data from OpenAQ API
measurement_data = get_measurement_data()

# Process the collected measurement data as needed
recept = {}
recept['n'] = len(measurement_data)  # Number of receptors
recept['x'] = np.zeros(recept['n'])
recept['y'] = np.zeros(recept['n'])
recept['z'] = np.zeros(recept['n'])
recept['label'] = []

for i, data in enumerate(measurement_data):
    # Extract relevant information from the OpenAQ API response
    measurements = data['results']
    if len(measurements) > 0:
        # Use the first measurement data for the receptor location
        measurement = measurements[0]
        if 'parameters' in measurement:
            parameters = measurement['parameters']
            if len(parameters) > 0:
                recept['z'][i] = parameters[0]['value']
                recept['label'].append(measurement['location'])

def gplume(x, y, z, H, Q, U):
    # GPLUME: Compute contaminant concentration (kg/m^3) at a given
    # set of receptor locations using the standard Gaussian plume
    # solution. This code handles a single source (located at the
    # origin) and multiple receptors.

    # First, define the cut-off velocity, below which concentration = 0.
    Umin = 0.0

    # Determine the sigma coefficients based on stability class C --
    # slightly unstable (3-5 m/s).
    ay = 0.34
    by = 0.82
    az = 0.275
    bz = 0.82
    sigmay = ay * np.abs(x)**by * (x > 0)
    sigmaz = az * np.abs(x)**bz * (x > 0)

    # Calculate the contaminant concentration (kg/m^3) using Ermak's formula.
    if U < Umin:
        C = np.zeros_like(z)
    else:
        C = Q / (2 * np.pi * U * sigmay * sigmaz) * np.exp(-0.5 * y**2 / sigmay**2) * (
                np.exp(-0.5 * (z - H)**2 / sigmaz**2) + np.exp(-0.5 * (z + H)**2 / sigmaz**2))
        C[np.isnan(C) | np.isinf(C)] = 0  # Set all NaN or inf values to zero.
    return C


def forward_atmospheric_dispersion(Uwind):
    # Set plotting parameters.
    nx = 100
    ny = nx
    xlim = [0, 2000]
    ylim = [-100, 400]
    x0 = np.linspace(xlim[0], xlim[1], nx + 1)[:-1]  # distance along wind direction (m)
    y0 = np.linspace(ylim[0], ylim[1], ny + 1)[:-1]  # cross-wind distance (m)
    xmesh, ymesh = np.meshgrid(x0, y0)  # mesh points for contour plot
    smallfont = 14

    glc = 0
    for i in range(source['n']):
        # Sum up ground-level PM2.5 concentrations from each source at all mesh points,
        # shifting the (x,y) coordinates so the source location is at the origin.
        glc += gplume(xmesh - source['x'][i], ymesh - source['y'][i], 0.0,
                      source['z'][i], source['Q'][i], Uwind)

    # Plot contours of ground-level PM2.5 concentration.
    clist = [0.001, 0.01, 0.02, 0.05, 0.1]
    glc2 = glc * 1e6  # convert concentration to μg/m^3
    plt.figure(1)
    plt.contourf(xmesh, ymesh, glc2, levels=clist)
    plt.colorbar()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title(f'PM2.5 concentration (μg/m^3), max = {np.max(glc2):.2f}')

    # Draw and label the source locations.
    plt.plot(source['x'], source['y'], 'ro', markeredgecolor='k', markerfacecolor='r')
    for i, label in enumerate(source['label']):
        plt.text(source['x'][i], source['y'][i], label, fontsize=smallfont, fontweight='bold')

    plt.grid(True)
    plt.show()


forward_atmospheric_dispersion(Uwind=5)