import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from pathlib import Path
from mmm.spectrograms.procedures.io import load_pickle
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION


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

# Creating data
t_0, t_1 = 0., 0.5  # seconds
n_0, n_1 = int(t_0 / TIME_RESOLUTION), int(t_1 / TIME_RESOLUTION)
f_0, f_1 = 0, 1000  # Hz
m_0, m_1 = int(f_0 / FREQUENCY_PRECISION), int(f_1 / FREQUENCY_PRECISION)
x = np.outer(f[m_0:m_1], np.ones(len(t[n_0:n_1])))
y = np.outer(np.ones(len(f[m_0:m_1])), t[n_0:n_1])
z = spectrogram[m_0:m_1, n_0:n_1]

# Plot image
plt.figure(figsize=(6, 6))
plt.imshow(z, cmap='afmhot', aspect='auto', origin='lower')
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
plt.savefig(animations_folder / Path('animation_spectrogram_image.png'))

# Animation
n_frames = 30
fps = 30
video_format = 'mp4'  # 'gif' or 'mp4'
zoom = 1.2

# Creating 3D figure
fig = plt.figure(figsize=(6, 6))
ax = plt.axes(projection='3d')
ax.invert_yaxis()
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
ax.set_box_aspect(aspect=None, zoom=zoom)
ax.set_facecolor((227/255, 232/255, 237/255, 1))


poly = ax.plot_surface(x, y, z, cmap='afmhot', edgecolor='none')

# cb = plt.colorbar()
# canvas = FigureCanvasTkAgg(figure, root)


def animate(frame, verbose=True):
    if frame < 30:
        poly.set_clims(-100-frame, -frame)

        # # Update plot
        # canvas.flush_events()
        # canvas.draw()
    else:
        pass

    # Print percentage
    if verbose:
        if frame % 5 == 0:
            print("Progress: {:.0f}%".format(frame / n_frames * 100))

    return fig,


# Animate
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=20, blit=True)

# Save
if video_format == 'mp4':
    FFwriter = animation.FFMpegWriter(fps=fps)
    animation_path = animations_folder / Path('animation_spectrogram_up_down.mp4')
    anim.save(str(animation_path), writer=FFwriter)
elif video_format == 'gif':
    animation_path = animations_folder / Path('animation_spectrogram_up_down.gif')
    anim.save(str(animation_path),  writer='imagemagick', fps=24)
else:
    raise ValueError('Unknown video format.')
