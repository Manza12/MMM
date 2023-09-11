from mmm import *
from mmm.spectrograms.layers import create_stft_layer, apply_stft_layer
from mmm.spectrograms.procedures.io import read_wav, load_or_compute
from mmm.spectrograms.plot import plot_stft
from mmm.spectrograms.parameters import FS


# Parameters
phd = True
name = 'gong'

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = data_folder / Path('audio')

output_folder = project_folder / Path('phd') / Path('introduction')
output_folder.mkdir(parents=True, exist_ok=True)

# Read wav file
print('Getting input...')

file_path = audio_folder / (name + '.wav')

t_0 = 1.  # 50.2
t_1 = 1.3  # 51.6
n_0 = int(t_0 * FS)
n_1 = int(t_1 * FS)
x = read_wav(file_path)
x = x[n_0:n_1]

# Load STFT layer
objects_folder = data_folder / Path('objects')
stft_layer = load_or_compute('stft_layer', objects_folder, {'stft_layer': True}, create_stft_layer)

# Apply STFT layer
spectrogram = apply_stft_layer(x, stft_layer)
spectrogram_numpy = spectrogram.cpu().numpy()
spectrogram_numpy = spectrogram_numpy[:100, :]

# Plot STFT
plot_stft(spectrogram_numpy, -120, 0, fig_size=(5., 4.))
plt.savefig(output_folder / (name + '_spectrogram.pdf'))

plt.show()
