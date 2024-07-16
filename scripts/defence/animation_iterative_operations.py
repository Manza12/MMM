from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from pathlib import Path
from mmm.spectrograms.plot import plot_stft
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION, MIN_DB

# Parameters
name = 'anastasia_excerpt'
video_format = 'mp4'
fps = 3
n_frames = 10
save_frames = False

operation = 'horizontal_thinning'
input_name = 'spectrogram_' + operation + '_stack.pickle'
output_name = name + '_animation_' + operation

t_start = 0.
t_end = 3.
f_start = 0.
f_end = 2000.

# Paths
project_folder = Path('..') / Path('..')
defence_folder = project_folder / Path('phd') / Path('defence')
results_folder = defence_folder / Path('results')
output_folder = results_folder / Path(name + '_%dms_%dHz' % (TIME_RESOLUTION * 1000, FREQUENCY_PRECISION))
arrays_folder = output_folder / Path('arrays')
animations_folder = defence_folder / Path('animations')

# Load
load_path = arrays_folder / Path(input_name)
stack = np.load(str(load_path), allow_pickle=True)
n_frames = min(n_frames, stack.shape[0])

# Plot
figure, ax = plt.subplots(figsize=(10, 4), dpi=300)

plot_stft(stack[0, :, :], v_min=MIN_DB, v_max=0, ax=ax)

# Since plotting a single graph
im = ax.get_images()[0]

# Limits
ax.set_xlim(t_start // TIME_RESOLUTION, t_end // TIME_RESOLUTION)
ax.set_ylim(f_start // FREQUENCY_PRECISION, f_end // FREQUENCY_PRECISION)


def animation_function(frame):
    im.set_data(stack[frame, :, :])
    if save_frames:
        output_frame_path = animations_folder / Path(output_name + '_%d' % frame + '.svg')
        plt.savefig(str(output_frame_path))
    return im,


animation = FuncAnimation(figure,
                          func=animation_function,
                          frames=n_frames,
                          interval=50)

# Save
output_path = animations_folder / Path(output_name + '.' + video_format)
if video_format == 'mp4':
    FFwriter = FFMpegWriter(fps=fps)
    animation.save(str(output_path), writer=FFwriter)
elif video_format == 'gif':
    animation.save(str(output_path),  writer='imagemagick', fps=fps)
else:
    raise ValueError('Unknown video format.')