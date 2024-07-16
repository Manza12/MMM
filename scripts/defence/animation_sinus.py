import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from pathlib import Path

# Parameters
fps = 60
duration = 3.  # seconds
video_format = 'mp4'  # 'gif' or 'mp4'

# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')
animations_folder = project_path / Path('phd') / Path('defence') / Path('animations')
animations_folder.mkdir(parents=True, exist_ok=True)

# Compute sinusoid
f = 440.  # Hz
extent = 3 / f  # seconds
t = np.linspace(0, extent, int(fps*duration))
sinusoid = np.sin(2 * np.pi * f * t)

figure, ax = plt.subplots(figsize=(8., 2))

# # Since plotting a single graph
# im = ax.get_images()[0]
line, = ax.plot([], [], lw=2, color='black')
plt.xlim(0, extent)
plt.ylim(-1.1, 1.1)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.savefig(defence_folder / 'sinusoid_background.svg', transparent=True)
# ax.set_facecolor((1.0, 0.47, 0.42))

plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

# Animation
def animation_function(frame):
    line.set_data(t[:frame], sinusoid[:frame])
    return line,


animation = FuncAnimation(figure,
                          func=animation_function,
                          frames=int(fps*duration),
                          interval=1/fps)

if video_format == 'gif':
    animation_path = animations_folder / Path('animation_sinusoid.gif')
    animation.save(str(animation_path),  writer='imagemagick', fps=fps)
elif video_format == 'mp4':
    FFwriter = FFMpegWriter(fps=fps)
    animation_path = animations_folder / Path('animation_sinusoid.mp4')
    animation.save(str(animation_path), writer=FFwriter)
else:
    raise ValueError('Unknown video format: ' + video_format)
