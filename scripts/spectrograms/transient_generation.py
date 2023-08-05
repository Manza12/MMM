from pathlib import Path
import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

from paths import CHAPTER_3_FOLDER

# Path
main_folder = Path('..') / Path('..')
output_folder = main_folder / CHAPTER_3_FOLDER / Path('transient_generation')
output_folder.mkdir(exist_ok=True)

# Sinus
fs = 1000
f_0 = 240
d = 3
t = np.arange(-3, 3, 1 / fs)
a = np.ones(len(t)//2)
a[:len(a)//6] *= 0
a[len(a)//6:] *= np.exp(- 0.003 * np.arange(len(a[len(a)//6:])))
a[len(a)*2//3:] *= np.exp(- 0.01 * np.arange(len(a[len(a)*2//3:])))
gauss = signal.windows.gaussian(500, 20)
a = np.convolve(a, gauss, mode='same')
a = np.concatenate((np.flip(a), a))


plt.figure()
plt.plot(t, a)

# a = np.convolve(a, 1 / (2 * np.pi * 1j * t), mode='same')
A = np.fft.fft(a)
r = 0.000
A[len(A)//2:] *= np.exp(-r * np.arange(len(A)//2)) / np.exp(r * len(A)//2)
a = np.fft.ifft(A)
A = np.fft.fft(a)

f = np.fft.fftfreq(len(t), 1 / fs)

plt.figure()
plt.plot(f, A.real)
plt.plot(f, A.imag)

plt.figure()
plt.plot(t, a.real)
plt.plot(t, a.imag)

# plt.figure()
# plt.plot(gauss)

x_1 = a * (np.exp(-1j * 2 * np.pi * (t - d/2) * f_0))
# x_2 = np.flip(a) * (np.exp(-1j * 2 * np.pi * (t - d/2) * f_0))
x = x_1  # + x_2
x /= np.max(np.abs(x))*2

y = np.fft.fft(x)

# STFT - x
nperseg = 256

omega, tau, Zxx = signal.stft(x, fs, return_onesided=False, nperseg=nperseg)
Zxx = np.fft.fftshift(Zxx, axes=0)

# STFT - y
omega_y, tau_y, Zyy = signal.stft(y, fs, return_onesided=False, nperseg=nperseg)
# Zyy = np.fft.fftshift(Zyy, axes=0)

# Write to file
wavfile.write(output_folder / 'transient.wav', fs, (y.real / y.real.max()).astype(np.float32))

# Plot
plt.figure(figsize=(4, 3))
plt.plot(t, y.real)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()

extent = [-np.max(tau_y)/2, np.max(tau_y)/2, np.min(omega_y), np.max(omega_y)]

plt.figure(figsize=(4, 3))
plt.imshow(20*np.log10(np.abs(Zxx+1e-7)), aspect='auto', origin='lower', cmap='afmhot', extent=extent,
           vmin=-100, vmax=0)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cb = plt.colorbar()
cb.set_label('Magnitude (dB)')
plt.tight_layout()
plt.savefig(output_folder / 'sinusoid.eps')

plt.figure(figsize=(4, 3))
plt.imshow(20*np.log10(np.abs(Zyy+1e-7) / 32), aspect='auto', origin='lower', cmap='afmhot', extent=extent,
           vmin=-100, vmax=0)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cb = plt.colorbar()
cb.set_label('Magnitude (dB)')
plt.tight_layout()
plt.savefig(output_folder / 'transient.eps')

plt.show()
