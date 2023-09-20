from pathlib import Path
import numpy as np
import scipy.io.wavfile as wav
from mmm.spectrograms.parameters import FS


duration = 0.5  # seconds
f_0 = 200  # Hertz
f_1 = 220  # Hertz

s_1 = 0.1 * np.sin(2 * np.pi * f_0 * np.linspace(0, duration, int(duration * FS)))
s_2 = 0.1 * np.sin(2 * np.pi * f_1 * np.linspace(0, duration, int(duration * FS)))

s = s_1 + s_2

file_path = Path('..') / Path('..') / Path('data') / Path('audio') / Path('interferences.wav')
wav.write(file_path, FS, s)
