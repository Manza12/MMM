import numpy as np
from scipy.io.wavfile import write
import scipy.signal.windows as windows
import matplotlib.pyplot as plt

volume = 0.1

fs = 44100
duration = 1
t = np.arange(0, duration, 1/fs)
f_0 = 1000
s = volume * np.sin(2*np.pi*f_0*t)

t_0 = 0.5
n_0 = int(t_0*fs)
t_1 = 0.75
n_1 = int(t_1*fs)
a = np.ones(len(t))
a[:n_0] = 0
a[n_1:] = 0

t_smooth = 0.01
n_smooth = int(t_smooth*fs)
g = windows.hann(n_smooth)
g = g / np.sum(g)
a_smooth = np.convolve(a, g, mode='same')
a_smooth = a_smooth.astype(np.float32)

x = s * a
x_smooth = s * a_smooth

x_smooth = x_smooth.astype(np.float32)
write('S.wav', fs, x_smooth)

plt.plot(t, x)
plt.plot(t, x_smooth)
plt.show()
