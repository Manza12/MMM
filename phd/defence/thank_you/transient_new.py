import numpy as np
from scipy.io.wavfile import write
import scipy.signal.windows as windows
import matplotlib.pyplot as plt

volume = 0.1

fs = 44100
duration = 2.5
t = np.arange(0, duration, 1/fs)
t_0 = 0.25
f_0 = t_0 * (fs / 2) / duration
s = volume * np.sin(2*np.pi*f_0*t)

f_0 = 1000
t_0 = f_0 * duration / (fs / 2)
n_0 = int(t_0*fs)
f_1 = 5000
t_1 = f_1 * duration / (fs / 2)
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

x_transient = np.fft.fft(x_smooth, n=int(2*duration*fs)).real[:int(duration*fs)] / fs * 128

x_transient = x_transient.astype(np.float32)
write('T.wav', fs, x_transient)

plt.plot(t, x_transient)
plt.show()
