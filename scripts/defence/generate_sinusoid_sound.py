import numpy as np
import scipy.io.wavfile as wav
from pathlib import Path

# Parameters
fs = 44100
t = np.linspace(0, 3, 3*fs)
f = 440
x = 0.2 * np.sin(2 * np.pi * f * t)

# Paths
project_path = Path('..') / Path('..')
defence_folder = project_path / Path('phd') / Path('defence')

wav.write('sinusoid_440.wav', fs, x)
