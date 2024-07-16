import numpy as np
from scipy.io.wavfile import write
import scipy.signal.windows as windows
import matplotlib.pyplot as plt

volume = 0.1

fs = 44100
duration = 1.5
t = np.arange(0, duration, 1/fs)

f_0 = 5000
f_1 = 10000
t_0 = 1.
t_1 = 1.5

n_0 = int(t_0*fs)
n_1 = int(t_1*fs)

f = np.zeros(len(t))
f[:n_0] = f_0
f[n_1:] = f_1
f[n_0:n_1] = np.linspace(f_0, f_1, n_1-n_0)
s = volume * np.sin(2*np.pi*np.cumsum(f)/fs)

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
write('L.wav', fs, x_smooth)

plt.plot(t, x)
plt.plot(t, x_smooth)
plt.show()
