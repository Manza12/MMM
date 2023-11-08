from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from pathlib import Path
from mmm.spectrograms.plot import plot_stft
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

# Parameters
name = 'anastasia'
fps = 10
direction = 'horizontal'

# Paths
project_path = Path('..') / Path('..')
results_folder = project_path / Path('phd') / Path('defence') / Path('results')
animations_folder = project_path / Path('phd') / Path('defence') / Path('animations')
animations_folder.mkdir(parents=True, exist_ok=True)
output_folder = results_folder / Path(name + '_%dms_%dHz' % (TIME_RESOLUTION * 1000, FREQUENCY_PRECISION))
stack_path = output_folder / Path('arrays') / Path('spectrogram_' + direction + '_thinning_stack.pickle')

# Load
stack = np.load(str(stack_path), allow_pickle=True)

figure, ax = plt.subplots()

plot_stft(stack[0, :, :], v_min=-120, v_max=0, ax=ax)

# Since plotting a single graph
im = ax.get_images()[0]

# Limits
TIME_RESOLUTION = 0.001
FREQUENCY_PRECISION = 5
ax.set_xlim(0.1 // TIME_RESOLUTION, 0.5 // TIME_RESOLUTION)
ax.set_ylim(0 // FREQUENCY_PRECISION, 1000 // FREQUENCY_PRECISION)


def animation_function(t):
    # i = int(t * 100)
    im.set_data(stack[t, :, :])
    return im,


animation = FuncAnimation(figure,
                          func=animation_function,
                          frames=np.arange(40),
                          interval=50)

animation_path = animations_folder / Path('animation_' + direction + '_thinning.gif')
animation.save(str(animation_path),  writer='imagemagick', fps=10)
