import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from pathlib import Path


# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')
animations_folder = project_path / Path('phd') / Path('defence') / Path('animations')
animations_folder.mkdir(parents=True, exist_ok=True)

# Creating data
sigma = 0.4
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
x, y = np.meshgrid(x, y)
z = np.exp(-(x**2 + y**2) / (2 * sigma**2))

# Plot image
plt.figure(figsize=(6, 6))
plt.imshow(z, cmap='Greys', aspect='auto', origin='lower')
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
plt.savefig(animations_folder / Path('gaussian.png'))

# Animation
n_frames = 90
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
ax.set_facecolor((227 / 255, 232 / 255, 237 / 255, 1))

ax.plot_surface(x, y, z, cmap='Greys', edgecolor='none')

ax.view_init(elev=90, azim=0)
plt.savefig(animations_folder / Path('gaussian_start.png'), transparent=True)


def init():
    ax.plot_surface(x, y, z, cmap='Greys', edgecolor='none')

    ax.view_init(elev=90, azim=0)

    # plt.savefig(animations_folder / Path('animation_spectrogram_start.png'))
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
    animation_path = animations_folder / Path('animation_gaussian.mp4')
    anim.save(str(animation_path), writer=FFwriter)
elif video_format == 'gif':
    animation_path = animations_folder / Path('animation_gaussian.gif')
    anim.save(str(animation_path),  writer='imagemagick', fps=24)
else:
    raise ValueError('Unknown video format.')

plt.savefig(animations_folder / Path('gaussian_end.png'), transparent=True)
