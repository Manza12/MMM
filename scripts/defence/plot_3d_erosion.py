import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from scipy.ndimage.morphology import grey_erosion


# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')

# Create data
sigma = 0.4
x = np.linspace(-0.6, 1, 100)
y = np.linspace(-1, 1, 100)
x, y = np.meshgrid(x, y)
z = np.sin(2 * np.pi * 0.5 * x)**2 * np.sin(2 * np.pi * 0.5 * y)**2 + \
    np.exp(-(x**2 + y**2) / (2 * sigma**2)) + \
    np.exp(-x*0.5-y*0.5)
# z = np.exp(-(x**2 + y**2) / (2 * sigma**2))
# z += np.exp(-((x-0.5)**2 + (y-0.1)**2) / (2 * sigma**2))
# z *= np.sin(2 * np.pi * x)**2 * np.sin(0.5 * np.pi * 2 * y)**2
# z += np.exp(-((x+0.7)**2 + (y+0.3)**2) / (2 * sigma**2))

# Structuring element
offset = 1
sigma = 0.8
x_b = np.linspace(-1, 1, 25)
y_b = np.linspace(-1, 1, 25)
x_b, y_b = np.meshgrid(x_b, y_b)
b = np.exp(-(x_b**2 + y_b**2) / (2 * sigma**2))
m = np.max(b)

# Erosion
z_ero = grey_erosion(z, structure=b)

plt.figure(figsize=(6, 6))
plt.imshow(z, cmap='Greys', aspect='auto', origin='lower')

plt.figure(figsize=(6, 6))
plt.imshow(z_ero, cmap='Greys', aspect='auto', origin='lower')

# Creating 3D figure
zoom = 1.2
fig = plt.figure(figsize=(6, 6))
ax = plt.axes(projection='3d')
ax.view_init(elev=45, azim=-30)

ax.invert_yaxis()
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
ax.set_box_aspect(aspect=None, zoom=zoom)
# ax.set_facecolor((227 / 255, 232 / 255, 237 / 255, 1))

r = 10
# ax.plot_surface(x, y, z, cmap='Greys', edgecolor='none')
ax.quiver(x[::r, ::r], y[::r, ::r], np.zeros_like(z_ero)[::r, ::r]+m,
          np.zeros_like(x)[::r, ::r], np.zeros_like(y)[::r, ::r], z_ero[::r, ::r])
ax.set_zlim(np.min(z), np.max(z))

plt.savefig(defence_folder / Path('quiver_surface.png'), transparent=True)

plt.show()
