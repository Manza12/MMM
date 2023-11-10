import numpy as np
import matplotlib.pyplot as plt


# Data
N = 1000
f_center = 440
n_octaves = 2
f = np.logspace(np.log2(f_center/2**n_octaves), np.log2(f_center*2**n_octaves), N, base=2)
p = np.log2(f/f_center) * 12 + 69

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
plt.plot(f, p)

# Set colors
fig.patch.set_facecolor('white')
fig.patch.set_alpha(0.)

ax.patch.set_facecolor('white')

n_lim = 2

plt.xlabel('Frequency (Hz)')
plt.ylabel('Pitch')

plt.xlim(f_center/2**n_lim, f_center*2**n_lim)
plt.ylim(69-n_lim*12, 69+n_lim*12)

plt.xticks([])
plt.yticks([])

# plt.tight_layout()
plt.savefig('logarithmic_pitches_0.svg')

plt.xticks([440])
plt.yticks([69], ['A4'])
ax.yaxis.grid(linestyle='dashed')
ax.xaxis.grid(linestyle='dashed')
plt.grid(True)

# plt.tight_layout()
plt.savefig('logarithmic_pitches_1.svg')

plt.xticks(2.**np.arange(-n_octaves, n_octaves+1) * f_center)
plt.yticks(np.arange(-n_octaves, n_octaves+1) * 12 + 69, ['A' + str(i+4) for i in range(-n_octaves, n_octaves+1)])

# plt.tight_layout()
plt.savefig('logarithmic_pitches_2.svg')

# ax.yaxis.grid(linestyle='dashed')
# ax.xaxis.grid(linestyle='dashed')
# plt.grid(True)

ax.yaxis.set_minor_locator(plt.MultipleLocator(1))

# plt.tight_layout()
plt.savefig('logarithmic_pitches_3.svg')

plt.show()
