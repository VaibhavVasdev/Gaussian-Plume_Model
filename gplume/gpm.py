# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Import custom modules for API access and calculations
from .API_Access import get_measurement_data, Nd, loc_x, loc_y, loc_z, s_label, source
from .OpenWeatherMapAPI import wind_data
from .inverse import optimal_emission_rates

# Define constants related to atmospheric dispersion
grav = 9.8
mu = 1.8e-5
rho = 1000
R = 1e-6
Wdep = 0.0062
Wset = 2 * rho * grav * R**2 / (9 * mu)

dia = 0.162
A = np.pi * (dia/2)**2

# Populate source dictionary with emission source data
source['n'] = Nd
source['x'] = loc_x
source['y'] = loc_y
source['z'] = loc_z
source['label'] = s_label
source['Q'] = np.array(optimal_emission_rates)/1000

# Retrieve measurement data from the API
measurement_data = get_measurement_data()

# Initialize the receptor dictionary
recept = {}
recept['n'] = len(measurement_data)
recept['x'] = np.zeros(recept['n'])
recept['y'] = np.zeros(recept['n'])
recept['z'] = np.zeros(recept['n'])
recept['label'] = []

# Populate the receptor dictionary with measurement locations
for i, data in enumerate(measurement_data):
    results = data['results']
    if len(results) > 0:
        measurement = results[0]
        latitude = measurement['coordinates']['latitude']
        longitude = measurement['coordinates']['longitude']
        recept['x'][i] = longitude
        recept['y'][i] = latitude
        recept['z'][i] = 0
        recept['label'].append(measurement['location'])

# Define the Gaussian plume dispersion model function
def gplume(x, y, z, H, Q, U):
    Umin = 0.0
    ay = 0.34
    by = 0.82
    az = 0.275
    bz = 0.82
    sigmay = ay * np.abs(x)**by * (x > 0)
    sigmaz = az * np.abs(x)**bz * (x > 0)

    # Calculate plume concentration
    if U < Umin:
        C = np.zeros_like(z)
    else:
        C = Q / (2 * np.pi * U * sigmay * sigmaz) * np.exp(-0.5 * y**2 / sigmay**2) * (
                np.exp(-0.5 * (z - H)**2 / sigmaz**2) + np.exp(-0.5 * (z + H)**2 / sigmaz**2))
        C[np.isnan(C) | np.isinf(C)] = 0
    return C


# Function to calculate Euclidean distance between two points
def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Function to adjust dot positions to avoid overlap
def adjust_dot_positions(x, y, min_distance=30):
    n = len(x)
    adjusted_x, adjusted_y = x.copy(), y.copy()

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(x[i], y[i], x[j], y[j])
            if dist < min_distance:
                avg_x = (x[i] + x[j]) / 2
                avg_y = (y[i] + y[j]) / 2
                adjusted_x[i] = avg_x - min_distance / 2
                adjusted_y[i] = avg_y + min_distance / 2
                adjusted_x[j] = avg_x + min_distance / 2
                adjusted_y[j] = avg_y - min_distance / 2

    return adjusted_x, adjusted_y

# Function to visualize atmospheric dispersion and measurement locations
def forward_atmospheric_dispersion(Uwind):
    nx = 100
    ny = nx
    xlim = [0, 2000]
    ylim = [-100, 400]
    x0 = np.linspace(xlim[0], xlim[1], nx + 1)[:-1]
    y0 = np.linspace(ylim[0], ylim[1], ny + 1)[:-1]
    xmesh, ymesh = np.meshgrid(x0, y0)
    smallfont = 14

    # Initialize concentration grid and Calculate plume concentration from multiple sources
    glc = np.zeros((ny, nx))
    for i in range(source['n']):
        glc += gplume(xmesh - source['x'][i], ymesh - source['y'][i], 0.0,
                      source['z'][i], source['Q'][i], Uwind)

    # Contour levels for concentration visualization
    clist = [0.001, 0.01, 0.02, 0.05, 0.1]
    glc2 = glc * 1e6

    # Create a contour plot of concentration
    plt.figure(1)
    cmap = plt.cm.get_cmap('tab10')
    cs = plt.contour(xmesh, ymesh, glc2, levels=clist, cmap=cmap, extend='both')
    plt.clabel(cs, inline=True, fontsize=8, colors='k')

    # Plot emission sources as red stars
    plt.scatter(source['x'], source['y'], marker='*', c='red', s=100, label='Sources')

    # Label emission sources with their labels
    for i in range(source['n']):
        plt.text(source['x'][i], source['y'][i], source['label'][i], fontsize=10,
                 fontweight='bold', color='red', va='bottom', ha='right')

    # Adjust receptor positions to avoid overlap
    adjusted_x, adjusted_y = adjust_dot_positions(recept['x'], recept['y'])
    plt.scatter(adjusted_x, adjusted_y, c='blue', edgecolors='black', s=50, picker=5)

    # Function to label measurement locations upon clicking
    def onpick(event):
        ind = event.ind
        if len(ind) > 0:
            x = adjusted_x[ind[0]]
            y = adjusted_y[ind[0]]
            label = recept['label'][ind[0]]
            plt.gca().text(x, y, label, fontsize=10, fontweight='bold', color='red')
            plt.draw()

    # Connect the click event to the label function
    plt.gcf().canvas.mpl_connect('pick_event', onpick)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'PM2.5 concentration (μg/m^3), max = {np.max(glc2):.2f}')
    plt.grid(True)
    plt.legend()
    plt.show()

# Check if wind data is available and visualize dispersion for each location
if len(wind_data) > 0:
    for location in wind_data:
        speed = location['speed']
        direction = location['direction']
        forward_atmospheric_dispersion(Uwind=speed)
else:
    print("Failed to retrieve wind data. Please check your API key or network connection.")
