from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from mmm.spectrograms.plot import plot_stft

stack = np.load('spectrogram_reconstruction_stack.pickle', allow_pickle=True)

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

animation.save('animation.gif',  writer='imagemagick', fps=10)

# plt.show()
