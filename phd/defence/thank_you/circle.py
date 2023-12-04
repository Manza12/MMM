import numpy as np
from scipy.io.wavfile import write
import scipy.signal.windows as windows
import matplotlib.pyplot as plt

volume = 0.1

fs = 44100
duration = 1.5
t = np.arange(0, duration, 1/fs)

t_c = 0.5
f_c = 10000

t_r = 0.25
f_r = 5000

t_0 = t_c - t_r
t_1 = t_c + t_r

n_0 = int(t_0*fs)
n_1 = int(t_1*fs)

f = np.zeros(len(t))
f[:n_0] = f_c
f[n_1:] = f_c
f[n_0:n_1] = f_c + f_r * np.sqrt(1 - ((t[n_0:n_1] - t_c) / t_r)**2)
s = volume * np.sin(2*np.pi*np.cumsum(f)/fs)

plt.plot(t, f)
plt.show()

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
write('C.wav', fs, x_smooth)

plt.plot(t, x)
plt.plot(t, x_smooth)
plt.show()
