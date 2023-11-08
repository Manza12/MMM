import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from pathlib import Path
from mmm.spectrograms.plot import plot_cqt
from mmm.spectrograms.layers import create_cqt_layer
from mmm.spectrograms.parameters import TIME_RESOLUTION, MIN_DB

# Parameters
name = 'anastasia'
fps = 24
duration = 12.  # seconds
video_format = 'mp4'  # 'gif' or 'mp4'

# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')
animations_folder = project_path / Path('phd') / Path('defence') / Path('animations')
animations_folder.mkdir(parents=True, exist_ok=True)

spectrogram_path = defence_folder / Path(name + '_spectrogram_cqt.npy')

# Load
spectrogram = np.load(str(spectrogram_path))
current_spectrogram = np.zeros_like(spectrogram) + MIN_DB
current_spectrogram = current_spectrogram[0]

figure, ax = plt.subplots(figsize=(8., 4.))

cqt_layer = create_cqt_layer()

plot_cqt(spectrogram, cqt_layer, MIN_DB, 0, ax=ax, colorbar=False)

plt.axis('off')
plt.tight_layout()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

# Since plotting a single graph
im = ax.get_images()[0]


# Animation
def animation_function(frame):
    t = frame / fps
    n = int(t / TIME_RESOLUTION)
    current_spectrogram[:, :n] = spectrogram[0, :, :n]
    im.set_data(current_spectrogram)
    return im,


animation = FuncAnimation(figure,
                          func=animation_function,
                          frames=int(fps*duration),
                          interval=1/fps)

if video_format == 'gif':
    animation_path = animations_folder / Path('animation_spectrogram.gif')
    animation.save(str(animation_path),  writer='imagemagick', fps=fps)
elif video_format == 'mp4':
    FFwriter = FFMpegWriter(fps=fps)
    animation_path = animations_folder / Path('animation_spectrogram.mp4')
    animation.save(str(animation_path), writer=FFwriter)
else:
    raise ValueError('Unknown video format: ' + video_format)
