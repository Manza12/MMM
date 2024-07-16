import numpy as np
import scipy.io.wavfile as wav
from pathlib import Path

FS = 44100
t = np.arange(0, 2, 1/FS)
f_0 = 440
f_1 = 554.37
f_2 = 659.25
f_3 = 880

x = np.sin(2*np.pi*f_0*t) + np.sin(2*np.pi*f_1*t) + np.sin(2*np.pi*f_2*t) + np.sin(2*np.pi*f_3*t)
x = x / np.max(np.abs(x))
x = x * 0.2

# Smooth start and end
x[:int(0.1*FS)] = x[:int(0.1*FS)] * np.linspace(0, 1, int(0.1*FS))
x[-int(0.1*FS):] = x[-int(0.1*FS):] * np.linspace(1, 0, int(0.1*FS))

file_path = Path('..') / Path('..') / Path('phd') / Path('defence') / Path('sinusoids.wav')
wav.write(file_path, FS, x)

