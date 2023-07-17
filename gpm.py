import numpy as np
import matplotlib.pyplot as plt
from API_Access import get_measurement_data
from OpenWeatherMapAPI import wind_data

grav = 9.8
mu = 1.8e-5
rho = 1000
R = 1e-6
Wdep = 0.0062
Wset = 2 * rho * grav * R**2 / (9 * mu)

dia = 0.162
A = np.pi * (dia/2)**2

source = {}
source['n'] = 4
source['x'] = np.array([285, 310, 900, 1095])
source['y'] = np.array([80, 205, 290, 190])
source['z'] = np.array([15, 35, 15, 15])
source['label'] = [' S1', ' S2', ' S3', ' S4']
tpy2kgps = 1.0 / 31536
source['Q'] = np.array([35, 80, 5, 5]) * tpy2kgps

measurement_data = get_measurement_data()

recept = {}
recept['n'] = len(measurement_data)
recept['x'] = np.zeros(recept['n'])
recept['y'] = np.zeros(recept['n'])
recept['z'] = np.zeros(recept['n'])
recept['label'] = []

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

def gplume(x, y, z, H, Q, U):
    Umin = 0.0
    ay = 0.34
    by = 0.82
    az = 0.275
    bz = 0.82
    sigmay = ay * np.abs(x)**by * (x > 0)
    sigmaz = az * np.abs(x)**bz * (x > 0)

    if U < Umin:
        C = np.zeros_like(z)
    else:
        C = Q / (2 * np.pi * U * sigmay * sigmaz) * np.exp(-0.5 * y**2 / sigmay**2) * (
                np.exp(-0.5 * (z - H)**2 / sigmaz**2) + np.exp(-0.5 * (z + H)**2 / sigmaz**2))
        C[np.isnan(C) | np.isinf(C)] = 0
    return C

def forward_atmospheric_dispersion(Uwind):
    nx = 100
    ny = nx
    xlim = [0, 2000]
    ylim = [-100, 400]
    x0 = np.linspace(xlim[0], xlim[1], nx + 1)[:-1]
    y0 = np.linspace(ylim[0], ylim[1], ny + 1)[:-1]
    xmesh, ymesh = np.meshgrid(x0, y0)
    smallfont = 14

    glc = np.zeros((ny, nx))
    for i in range(source['n']):
        glc += gplume(xmesh - source['x'][i], ymesh - source['y'][i], 0.0,
                      source['z'][i], source['Q'][i], Uwind)

    clist = [0.001, 0.01, 0.02, 0.05, 0.1]
    glc2 = glc * 1e6
    plt.figure(1)
    plt.contourf(xmesh, ymesh, glc2, levels=clist)
    plt.colorbar()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'PM2.5 concentration (μg/m^3), max = {np.max(glc2):.2f}')

    plt.plot(recept['x'], recept['y'], 'bo', markeredgecolor='k', markerfacecolor='b')
    for i, label in enumerate(recept['label']):
        plt.text(recept['x'][i], recept['y'][i], label, fontsize=smallfont, fontweight='bold')

    plt.grid(True)
    plt.show()

if len(wind_data) > 0:
    for location in wind_data:
        speed = location['speed']
        direction = location['direction']
        forward_atmospheric_dispersion(Uwind=speed)
else:
    print("Failed to retrieve wind data. Please check your API key or network connection.")