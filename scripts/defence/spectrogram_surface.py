# Import libraries
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION
from mmm.spectrograms.procedures.io import load_pickle

plt.style.use('dark_background')

# Parameters
name = 'anastasia'

# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')
animations_folder = project_path / Path('phd') / Path('defence') / Path('animations')
animations_folder.mkdir(parents=True, exist_ok=True)

spectrogram_path = defence_folder / Path(name + '_spectrogram_stft.pickle')
TIME_RESOLUTION /= 10

# Load
spectrogram_tensor = load_pickle(spectrogram_path)
# spectrogram = np.load(str(spectrogram_path), allow_pickle=True)
spectrogram = spectrogram_tensor.cpu().numpy()

t = np.arange(spectrogram.shape[1]) * TIME_RESOLUTION
f = np.arange(spectrogram.shape[0]) * FREQUENCY_PRECISION

# Creating figure
fig = plt.figure(figsize=(8, 4.5))
ax = plt.axes(projection='3d')
ax.invert_yaxis()

# Creating plot
t_0, t_1 = 0., 0.5  # seconds
n_0, n_1 = int(t_0 / TIME_RESOLUTION), int(t_1 / TIME_RESOLUTION)
f_0, f_1 = 0, 1000  # Hz
m_0, m_1 = int(f_0 / FREQUENCY_PRECISION), int(f_1 / FREQUENCY_PRECISION)
x = np.outer(f[m_0:m_1], np.ones(len(t[n_0:n_1])))
y = np.outer(np.ones(len(f[m_0:m_1])), t[n_0:n_1])
z = spectrogram[m_0:m_1, n_0:n_1]
surf = ax.plot_surface(x, y, z,
                       cmap='afmhot',
                       edgecolor='none')


# fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
# ax.set_title('3D Spectrogram')
plt.axis('off')

# show plot
plt.show()
