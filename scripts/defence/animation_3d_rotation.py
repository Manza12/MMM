# First import everthing you need
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from pathlib import Path
from mmm.spectrograms.procedures.io import load_pickle
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

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
fig = plt.figure(figsize=(6, 6))
ax = plt.axes(projection='3d')
ax.invert_yaxis()
plt.axis('off')

# Creating plot
t_0, t_1 = 0., 0.5  # seconds
n_0, n_1 = int(t_0 / TIME_RESOLUTION), int(t_1 / TIME_RESOLUTION)
f_0, f_1 = 0, 1000  # Hz
m_0, m_1 = int(f_0 / FREQUENCY_PRECISION), int(f_1 / FREQUENCY_PRECISION)
x = np.outer(f[m_0:m_1], np.ones(len(t[n_0:n_1])))
y = np.outer(np.ones(len(f[m_0:m_1])), t[n_0:n_1])
z = spectrogram[m_0:m_1, n_0:n_1]

# Animation
n_frames = 90
fps = 30
video_format = 'gif'  # 'gif' or 'mp4'


def init():
    ax.plot_surface(x, y, z, cmap='afmhot', edgecolor='none')
    ax.view_init(elev=90, azim=0)
    plt.savefig(animations_folder / Path('animation_spectrogram_start.png'))
    return fig,


def animate(frame, verbose=False):
    if frame < 15:
        elev = 90
        azim = 0
    elif frame < 75:
        elev = 90 - (frame - 15)
        azim = frame - 15
    else:
        elev = 30
        azim = 60
    ax.view_init(elev=elev, azim=azim)

    # Print percentage
    if frame % 5 == 0:
        print("Progress: {:.0f}%".format(frame / n_frames * 100))
    if verbose:
        print(frame, elev, azim)
    return fig,


# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=20, blit=True)

# Save
if video_format == 'mp4':
    FFwriter = animation.FFMpegWriter(fps=fps)
    animation_path = animations_folder / Path('animation_spectrogram.mp4')
    anim.save(str(animation_path), writer=FFwriter)
elif video_format == 'gif':
    animation_path = animations_folder / Path('animation_spectrogram.gif')
    anim.save(str(animation_path),  writer='imagemagick', fps=24)
else:
    raise ValueError('Unknown video format.')

plt.savefig(animations_folder / Path('animation_spectrogram_end.png'))

