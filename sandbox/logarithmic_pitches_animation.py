import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Data
N = 1000
f_center = 440
n_octaves = 5
f = np.logspace(np.log2(f_center/2**n_octaves), np.log2(f_center*2**n_octaves), N, base=2)
p = np.log2(f/f_center) * 12 + 69

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
plt.plot(f, p)

# Set colors
fig.patch.set_facecolor([227/255, 232/255, 237/255])
ax.patch.set_facecolor('white')

n_lim = 2

plt.xlim(f_center/2**n_lim, f_center*2**n_lim)
plt.ylim(69-2*12, 69+2*12)

plt.xlabel('Frequency (Hz)')
plt.ylabel('Pitch')

plt.xticks(2.**np.arange(-n_octaves, n_octaves+1) * f_center)
plt.yticks(np.arange(-n_octaves, n_octaves+1) * 12 + 69, ['A' + str(i+4) for i in range(-n_octaves, n_octaves+1)])

ax.yaxis.grid(linestyle='dashed')
ax.xaxis.grid(linestyle='dashed')
plt.grid(True)

ax.yaxis.set_minor_locator(plt.MultipleLocator(1))

# plt.tight_layout()

# Animation
fps = 24
speed = 1
duration = 3.
frames = int(duration * fps)


def update(frame):
    new_lim = n_lim + frame * speed / fps
    ax.set_xlim(f_center/2**new_lim, f_center*2**new_lim)
    ax.set_ylim(69-new_lim*12, 69+new_lim*12)
    return plt


anim = FuncAnimation(fig, update, frames=frames, interval=1000/fps)

# Save animation
anim.save('logarithmic_pitches_animation.mp4', fps=fps)
